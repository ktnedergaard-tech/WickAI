"""
WickAI Pattern Scraper
Automatically discovers new candlestick patterns from trading education sites
and appends them to patterns.py. Safe to run repeatedly — skips duplicates.

Usage:
  python scraper.py                  # run once
  python scraper.py --dry-run        # preview without writing
"""

import argparse
import json
import logging
import os
import re
import time
import urllib.request
import urllib.error
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# ── Sources to scrape ──────────────────────────────────────────────────────────
SOURCES = [
    "https://school.stockcharts.com/doku.php?id=chart_analysis:introduction_to_candlesticks",
    "https://www.investopedia.com/articles/active-trading/092315/5-most-powerful-candlestick-patterns.asp",
    "https://www.babypips.com/learn/forex/candlestick-cheat-sheet",
    "https://analyzingalpha.com/candlestick-patterns",
    "https://www.candlescanner.com/candlestick-patterns/",
    "https://www.quantifiedstrategies.com/candlestick-patterns/",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

EXTRACTION_PROMPT = """You are a candlestick pattern expert. Below is raw HTML/text from a trading education page.

Extract ALL candlestick pattern names mentioned in this text. For each pattern, return a JSON array where each item has:
- "name": exact pattern name (e.g. "Bullish Engulfing", "Doji", "Hammer")
- "type": "bullish", "bearish", or "neutral"
- "reliability": integer 1-10 based on how reliable the source describes it
- "description": 2-3 sentence description of what the pattern looks like and what it signals
- "trade_guidance": 1-2 sentences on entry, stop-loss placement

Return ONLY a valid JSON array. No markdown, no extra text.

Page content:
{content}
"""

DEDUP_PROMPT = """You are reviewing a list of candlestick patterns to add to a trading platform.

EXISTING patterns (do NOT include these or any variations of them):
{existing}

NEW CANDIDATES (from scraping):
{candidates}

Return ONLY the patterns from NEW CANDIDATES that are genuinely different from all EXISTING patterns.
Minor name variations of the same pattern should be excluded (e.g. "Bullish Engulfing Candle" = "Bullish Engulfing").
Return as a JSON array using the same structure. Return [] if nothing new.
"""


def fetch_page(url: str, timeout: int = 15) -> str:
    """Fetch a URL and return stripped text content."""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            html = resp.read().decode("utf-8", errors="replace")
        # Strip HTML tags
        text = re.sub(r"<[^>]+>", " ", html)
        text = re.sub(r"\s+", " ", text).strip()
        logger.info(f"Fetched {url} ({len(text)} chars)")
        return text[:8000]
    except Exception as e:
        logger.warning(f"Failed to fetch {url}: {e}")
        return ""


def _gemini_call(prompt: str) -> str:
    """Call Gemini flash with a text prompt and return the response text."""
    import google.generativeai as genai
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    raw = response.text.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return raw


def extract_patterns_from_text(client, text: str) -> list[dict]:
    """Ask Gemini to extract pattern data from raw page text."""
    if not text:
        return []
    try:
        raw = _gemini_call(EXTRACTION_PROMPT.format(content=text))
        return json.loads(raw)
    except Exception as e:
        logger.warning(f"Pattern extraction failed: {e}")
        return []


def deduplicate(client, existing_names: list[str], candidates: list[dict]) -> list[dict]:
    """Use Gemini to filter out patterns that already exist."""
    if not candidates:
        return []
    try:
        raw = _gemini_call(DEDUP_PROMPT.format(
            existing="\n".join(f"- {n}" for n in existing_names),
            candidates=json.dumps(candidates, indent=2)
        ))
        return json.loads(raw)
    except Exception as e:
        logger.warning(f"Deduplication failed: {e}")
        return []


def pattern_to_key(name: str) -> str:
    """Convert a pattern name to a Python dict key."""
    key = name.lower()
    key = re.sub(r"[^a-z0-9]+", "_", key)
    key = key.strip("_")
    return key


def pattern_to_python(key: str, p: dict) -> str:
    """Format a single pattern as a Python dict entry."""
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
    """Load existing pattern names from patterns.py."""
    try:
        import sys
        sys.path.insert(0, os.path.dirname(__file__))
        from patterns import get_pattern_names
        return get_pattern_names()
    except Exception as e:
        logger.error(f"Could not load existing patterns: {e}")
        return []


def append_to_patterns_file(new_patterns: list[dict], patterns_path: str) -> int:
    """Append new patterns to patterns.py, before the closing }."""
    with open(patterns_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the closing brace of CANDLESTICK_PATTERNS
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


def run(dry_run: bool = False) -> int:
    """Main scraper loop. Returns number of new patterns added."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY not set — scraper requires AI for extraction")
        return 0

    client = anthropic.Anthropic(api_key="placeholder")  # unused, kept for compat
    existing_names = get_existing_names()
    logger.info(f"Currently {len(existing_names)} patterns in database")

    all_candidates: list[dict] = []

    for url in SOURCES:
        logger.info(f"Scraping: {url}")
        text = fetch_page(url)
        if not text:
            continue
        patterns = extract_patterns_from_text(client, text)
        logger.info(f"  → Extracted {len(patterns)} pattern candidates")
        all_candidates.extend(patterns)
        time.sleep(1)  # polite delay between requests

    if not all_candidates:
        logger.info("No candidates found — nothing to add")
        return 0

    logger.info(f"Total candidates across all sources: {len(all_candidates)}")

    # Deduplicate against existing patterns
    new_patterns = deduplicate(client, existing_names, all_candidates)
    logger.info(f"New unique patterns after deduplication: {len(new_patterns)}")

    if not new_patterns:
        logger.info("No new patterns found — database is up to date")
        return 0

    for p in new_patterns:
        logger.info(f"  + {p.get('name')} ({p.get('type')}, reliability {p.get('reliability')})")

    if dry_run:
        logger.info("Dry-run mode — not writing to patterns.py")
        return len(new_patterns)

    patterns_path = os.path.join(os.path.dirname(__file__), "patterns.py")
    added = append_to_patterns_file(new_patterns, patterns_path)
    logger.info(f"Added {added} new patterns to {patterns_path}")
    return added


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WickAI Pattern Scraper")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()
    count = run(dry_run=args.dry_run)
    print(f"\nResult: {count} new patterns {'found (dry-run)' if args.dry_run else 'added'}")
