"""
WickAI Pattern Scraper
Automatically discovers new candlestick patterns from trading education sites
and appends them to patterns.py. Safe to run repeatedly — skips duplicates.

Free-tier optimised:
  - Enforces ≥5 s between Gemini calls (free tier = 15 RPM max)
  - Auto-retries on 429 with the delay Gemini suggests
  - Local name-based pre-dedup before the expensive AI dedup call
  - Batches large candidate lists into chunks of 40 for AI dedup
  - Saves a resume cache (scraper_cache.json) so a crash loses no work
  - Auto-commits new patterns to git after writing

Usage:
  python scraper.py                  # run and commit new patterns
  python scraper.py --dry-run        # preview without writing or committing
  python scraper.py --no-commit      # write patterns.py but skip git commit
"""

import argparse
import json
import logging
import os
import re
import subprocess
import time
import urllib.request
import urllib.error
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# ── Gemini rate-limit guard ────────────────────────────────────────────────────
_GEMINI_MIN_INTERVAL = 5.0   # seconds between calls — keeps us well under 15 RPM
_last_gemini_ts: float = 0.0

# ── Resume cache path ──────────────────────────────────────────────────────────
_CACHE_PATH = os.path.join(os.path.dirname(__file__), "scraper_cache.json")

# ── Sources to scrape ──────────────────────────────────────────────────────────
SOURCES = [
    # ── Core candlestick education ────────────────────────────────────────────
    "https://school.stockcharts.com/doku.php?id=chart_analysis:introduction_to_candlesticks",
    "https://school.stockcharts.com/doku.php?id=chart_analysis:chart_patterns",
    "https://school.stockcharts.com/doku.php?id=chart_analysis:candlestick_pattern_dictionary",
    "https://www.investopedia.com/articles/active-trading/092315/5-most-powerful-candlestick-patterns.asp",
    "https://www.investopedia.com/trading/candlestick-charting-what-is-it/",
    "https://www.babypips.com/learn/forex/candlestick-cheat-sheet",
    "https://www.babypips.com/learn/forex/japanese-candlestick-cheat-sheet",
    "https://analyzingalpha.com/candlestick-patterns",
    "https://analyzingalpha.com/chart-patterns",
    "https://www.candlescanner.com/candlestick-patterns/",
    "https://www.quantifiedstrategies.com/candlestick-patterns/",
    "https://www.quantifiedstrategies.com/chart-patterns/",

    # ── Barchart education ────────────────────────────────────────────────────
    "https://www.barchart.com/education/candlestick-patterns",
    "https://www.barchart.com/education/chart-patterns",

    # ── Finviz ────────────────────────────────────────────────────────────────
    "https://finviz.com/candlestick-patterns.ashx",

    # ── Investing.com education ───────────────────────────────────────────────
    "https://www.investing.com/education/candlestick-patterns",
    "https://www.investing.com/education/chart-patterns",

    # ── Smart Money / ICT / SMC ───────────────────────────────────────────────
    "https://www.babypips.com/learn/forex/smart-money-concepts",
    "https://analyzingalpha.com/order-block",
    "https://www.quantifiedstrategies.com/smart-money-concepts/",

    # ── Harmonic patterns ─────────────────────────────────────────────────────
    "https://www.investopedia.com/terms/h/harmonics.asp",
    "https://analyzingalpha.com/harmonic-patterns",

    # ── Elliott Wave & Wyckoff ────────────────────────────────────────────────
    "https://www.investopedia.com/terms/e/elliottwavetheory.asp",
    "https://www.investopedia.com/articles/trading/07/wyckoff.asp",
    "https://school.stockcharts.com/doku.php?id=market_analysis:the_wyckoff_method",

    # ── Volume & market structure ─────────────────────────────────────────────
    "https://analyzingalpha.com/volume-spread-analysis",
    "https://www.quantifiedstrategies.com/price-action-patterns/",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

EXTRACTION_PROMPT = """You are a candlestick and chart pattern expert. Below is raw text from a trading education page.

Extract ALL candlestick and chart pattern names mentioned. For each pattern return a JSON array item with:
- "name": exact pattern name (e.g. "Bullish Engulfing", "Head and Shoulders", "Order Block")
- "type": "bullish", "bearish", or "neutral"
- "reliability": integer 1-10 based on how reliable the source describes it
- "description": 2-3 sentence description of what the pattern looks like and what it signals
- "trade_guidance": 1-2 sentences on entry, stop-loss placement

Return ONLY a valid JSON array. No markdown, no extra text. Return [] if no patterns found.

Page content:
{content}
"""

DEDUP_PROMPT = """You are reviewing a list of candlestick/chart patterns to add to a trading platform.

EXISTING patterns (do NOT include these or any variations):
{existing}

NEW CANDIDATES:
{candidates}

Return ONLY the patterns from NEW CANDIDATES that are genuinely different from all EXISTING patterns.
Minor name variations of the same pattern should be excluded (e.g. "Bullish Engulfing Candle" = "Bullish Engulfing").
Return as a JSON array using the same structure. Return [] if nothing is new.
"""

DEDUP_BATCH_SIZE = 40   # max candidates per AI dedup call


# ── Gemini helper ──────────────────────────────────────────────────────────────

def _gemini_call(prompt: str, max_retries: int = 4) -> str:
    """Call Gemini flash with rate-limit respect and auto-retry on 429."""
    global _last_gemini_ts
    import google.generativeai as genai

    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")

    for attempt in range(max_retries):
        # Enforce minimum spacing between calls
        elapsed = time.time() - _last_gemini_ts
        if elapsed < _GEMINI_MIN_INTERVAL:
            time.sleep(_GEMINI_MIN_INTERVAL - elapsed)

        try:
            _last_gemini_ts = time.time()
            response = model.generate_content(prompt)
            raw = response.text.strip()
            raw = re.sub(r"^```(?:json)?\s*", "", raw)
            raw = re.sub(r"\s*```$", "", raw)
            return raw

        except Exception as e:
            err = str(e)
            if "429" in err:
                match = re.search(r"seconds:\s*(\d+)", err)
                delay = min(int(match.group(1)) if match else 65, 70)
                logger.warning(
                    f"Gemini rate limited (attempt {attempt+1}/{max_retries}). "
                    f"Sleeping {delay}s…"
                )
                if attempt < max_retries - 1:
                    time.sleep(delay)
                    continue
            raise


# ── Page fetching ──────────────────────────────────────────────────────────────

def fetch_page(url: str, timeout: int = 15) -> str:
    """Fetch a URL and return stripped text content (max 10 000 chars)."""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            html = resp.read().decode("utf-8", errors="replace")
        text = re.sub(r"<[^>]+>", " ", html)
        text = re.sub(r"\s+", " ", text).strip()
        logger.info(f"Fetched {url} ({len(text)} chars)")
        return text[:10_000]
    except Exception as e:
        logger.warning(f"Failed to fetch {url}: {e}")
        return ""


# ── Extraction & dedup ─────────────────────────────────────────────────────────

def extract_patterns_from_text(text: str) -> list[dict]:
    """Ask Gemini to extract pattern data from raw page text."""
    if not text:
        return []
    try:
        raw = _gemini_call(EXTRACTION_PROMPT.format(content=text))
        result = json.loads(raw)
        return result if isinstance(result, list) else []
    except Exception as e:
        logger.warning(f"Pattern extraction failed: {e}")
        return []


def _normalise_name(name: str) -> str:
    """Lowercase + strip punctuation for fuzzy name comparison."""
    return re.sub(r"[^a-z0-9]", "", name.lower())


def local_prededup(existing_names: list[str], candidates: list[dict]) -> list[dict]:
    """Fast local dedup: drop candidates whose normalised name matches an existing one."""
    existing_norm = {_normalise_name(n) for n in existing_names}
    out, seen = [], set()
    for p in candidates:
        norm = _normalise_name(p.get("name", ""))
        if norm and norm not in existing_norm and norm not in seen:
            out.append(p)
            seen.add(norm)
    return out


def ai_dedup_batch(existing_names: list[str], candidates: list[dict]) -> list[dict]:
    """AI dedup in batches of DEDUP_BATCH_SIZE to keep prompts manageable."""
    if not candidates:
        return []
    existing_str = "\n".join(f"- {n}" for n in existing_names)
    all_new: list[dict] = []
    known_after = list(existing_names)

    for i in range(0, len(candidates), DEDUP_BATCH_SIZE):
        batch = candidates[i: i + DEDUP_BATCH_SIZE]
        logger.info(
            f"AI dedup batch {i//DEDUP_BATCH_SIZE + 1}/"
            f"{(len(candidates)-1)//DEDUP_BATCH_SIZE + 1} "
            f"({len(batch)} candidates)"
        )
        try:
            raw = _gemini_call(DEDUP_PROMPT.format(
                existing="\n".join(f"- {n}" for n in known_after),
                candidates=json.dumps(batch, indent=2),
            ))
            result = json.loads(raw)
            if isinstance(result, list):
                all_new.extend(result)
                known_after.extend(p["name"] for p in result if "name" in p)
        except Exception as e:
            logger.warning(f"AI dedup batch failed: {e}")

    return all_new


# ── Resume cache ───────────────────────────────────────────────────────────────

def load_cache() -> dict:
    if os.path.exists(_CACHE_PATH):
        try:
            with open(_CACHE_PATH) as f:
                return json.load(f)
        except Exception:
            pass
    return {"scraped_urls": [], "candidates": []}


def save_cache(cache: dict) -> None:
    with open(_CACHE_PATH, "w") as f:
        json.dump(cache, f, indent=2)


def clear_cache() -> None:
    if os.path.exists(_CACHE_PATH):
        os.remove(_CACHE_PATH)


# ── patterns.py writer ─────────────────────────────────────────────────────────

def pattern_to_key(name: str) -> str:
    key = name.lower()
    key = re.sub(r"[^a-z0-9]+", "_", key)
    return key.strip("_")


def pattern_to_python(key: str, p: dict) -> str:
    name        = p.get("name", key)
    ptype       = p.get("type", "neutral")
    reliability = int(p.get("reliability", 6))
    description = p.get("description", "").replace('"', '\\"')
    guidance    = p.get("trade_guidance", "").replace('"', '\\"')
    return (
        f'    "{key}": {{\n'
        f'        "name": "{name}",\n'
        f'        "type": "{ptype}",\n'
        f'        "reliability": {reliability},\n'
        f'        "description": (\n'
        f'            "{description}"\n'
        f'        ),\n'
        f'        "trade_guidance": (\n'
        f'            "{guidance}"\n'
        f'        ),\n'
        f'    }},\n'
    )


def get_existing_names() -> list[str]:
    try:
        import sys, importlib
        sys.path.insert(0, os.path.dirname(__file__))
        import patterns as _p
        importlib.reload(_p)          # pick up any changes from current run
        return _p.get_pattern_names()
    except Exception as e:
        logger.error(f"Could not load existing patterns: {e}")
        return []


def append_to_patterns_file(new_patterns: list[dict], patterns_path: str) -> int:
    with open(patterns_path, "r", encoding="utf-8") as f:
        content = f.read()
    insert_pos = content.rfind("\n}")
    if insert_pos == -1:
        logger.error("Could not find closing brace in patterns.py")
        return 0
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    block = f"\n    # ── Auto-scraped {timestamp} ──\n"
    for p in new_patterns:
        key = pattern_to_key(p["name"])
        block += "\n" + pattern_to_python(key, p)
    new_content = content[:insert_pos] + block + content[insert_pos:]
    with open(patterns_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    return len(new_patterns)


# ── Git auto-commit ────────────────────────────────────────────────────────────

def git_commit_patterns(count: int) -> None:
    """Stage patterns.py and commit with a descriptive message."""
    try:
        patterns_path = os.path.join(os.path.dirname(__file__), "patterns.py")
        subprocess.run(["git", "add", patterns_path], check=True)
        msg = (
            f"scraper: add {count} new pattern{'s' if count != 1 else ''} "
            f"({datetime.utcnow().strftime('%Y-%m-%d')})"
        )
        subprocess.run(["git", "commit", "-m", msg], check=True)
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
        logger.info(f"Committed and pushed: {msg}")
    except subprocess.CalledProcessError as e:
        logger.warning(f"Git operation failed (patterns still saved): {e}")


# ── Main ───────────────────────────────────────────────────────────────────────

def run(dry_run: bool = False, no_commit: bool = False) -> int:
    """Main scraper loop. Returns number of new patterns added."""
    if not os.getenv("GEMINI_API_KEY"):
        logger.error("GEMINI_API_KEY not set — scraper requires Gemini for extraction")
        return 0

    existing_names = get_existing_names()
    logger.info(f"Currently {len(existing_names)} patterns in database")

    # Load resume cache
    cache = load_cache()
    already_done = set(cache["scraped_urls"])
    all_candidates: list[dict] = list(cache["candidates"])

    if already_done:
        logger.info(
            f"Resuming from cache: {len(already_done)} URLs already scraped, "
            f"{len(all_candidates)} candidates buffered"
        )

    # ── Scrape each source ────────────────────────────────────────────────────
    for url in SOURCES:
        if url in already_done:
            logger.info(f"Skipping (cached): {url}")
            continue

        logger.info(f"Scraping: {url}")
        text = fetch_page(url)
        if not text:
            already_done.add(url)
            continue

        patterns = extract_patterns_from_text(text)
        logger.info(f"  → Extracted {len(patterns)} pattern candidates")
        all_candidates.extend(patterns)
        already_done.add(url)

        # Save progress after every source
        cache["scraped_urls"] = list(already_done)
        cache["candidates"]   = all_candidates
        save_cache(cache)

        time.sleep(2)   # polite HTTP delay

    if not all_candidates:
        logger.info("No candidates found — nothing to add")
        clear_cache()
        return 0

    logger.info(f"Total raw candidates: {len(all_candidates)}")

    # ── Local pre-dedup (free, instant) ──────────────────────────────────────
    pre_filtered = local_prededup(existing_names, all_candidates)
    logger.info(
        f"After local name-dedup: {len(pre_filtered)} remain "
        f"(dropped {len(all_candidates) - len(pre_filtered)} obvious duplicates)"
    )

    if not pre_filtered:
        logger.info("No new patterns after local dedup — database is up to date")
        clear_cache()
        return 0

    # ── AI dedup (catches name variations and synonyms) ───────────────────────
    new_patterns = ai_dedup_batch(existing_names, pre_filtered)
    logger.info(f"New unique patterns after AI dedup: {len(new_patterns)}")

    if not new_patterns:
        logger.info("No new patterns after AI dedup — database is up to date")
        clear_cache()
        return 0

    for p in new_patterns:
        logger.info(f"  + {p.get('name')} ({p.get('type')}, reliability {p.get('reliability')})")

    if dry_run:
        logger.info("Dry-run mode — not writing to patterns.py")
        clear_cache()
        return len(new_patterns)

    patterns_path = os.path.join(os.path.dirname(__file__), "patterns.py")
    added = append_to_patterns_file(new_patterns, patterns_path)
    logger.info(f"Added {added} new patterns to {patterns_path}")

    clear_cache()   # fresh start next time

    if not no_commit:
        git_commit_patterns(added)

    return added


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WickAI Pattern Scraper")
    parser.add_argument("--dry-run",   action="store_true", help="Preview without writing")
    parser.add_argument("--no-commit", action="store_true", help="Write patterns.py but skip git commit")
    args = parser.parse_args()
    count = run(dry_run=args.dry_run, no_commit=args.no_commit)
    print(f"\nResult: {count} new patterns {'found (dry-run)' if args.dry_run else 'added'}")
