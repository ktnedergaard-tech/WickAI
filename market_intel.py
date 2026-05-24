"""
WickAI Market Intelligence
Fetches live market context from free sources and injects it into every
AI analysis so Gemini reasons about patterns with full market awareness.
"""

import json
import logging
import time
import urllib.request
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

_CACHE: dict = {}
_CACHE_TTL = 300  # 5 minutes — avoids hammering free APIs


def get_market_context() -> dict:
    """Return current market context. Cached for 5 minutes."""
    now = time.time()
    if "data" in _CACHE and now - _CACHE.get("ts", 0) < _CACHE_TTL:
        return _CACHE["data"]

    ctx = {
        "session":       _get_trading_session(),
        "session_notes": _get_session_notes(),
        "day":           datetime.now(timezone.utc).strftime("%A"),
        "utc_hour":      datetime.now(timezone.utc).hour,
        "fear_greed":    _get_fear_greed(),
    }

    _CACHE["data"] = ctx
    _CACHE["ts"] = now
    logger.info(
        f"Market context: {ctx['session']} | "
        f"F&G: {ctx['fear_greed']['value'] if ctx['fear_greed'] else 'N/A'}"
    )
    return ctx


# ── Session detection ──────────────────────────────────────────────────────────

def _get_trading_session() -> str:
    hour = datetime.now(timezone.utc).hour
    us   = 13 <= hour < 20   # 9:30 AM–4:00 PM ET (EDT) ≈ 13:30–20:00 UTC
    eu   = 7  <= hour < 16   # London 8:00 AM–5:00 PM GMT
    asia = hour < 7 or hour >= 23

    if us and eu:
        return "London/NY Overlap"
    if us:
        return "US Market Hours"
    if eu:
        return "European Session"
    if asia:
        return "Asian Session"
    return "Pre-Market / After Hours"


def _get_session_notes() -> str:
    session = _get_trading_session()
    hour    = datetime.now(timezone.utc).hour
    day     = datetime.now(timezone.utc).strftime("%A")
    notes   = []

    session_map = {
        "London/NY Overlap":       "Peak liquidity — highest probability of sustained breakouts and institutional moves",
        "US Market Hours":         "US equities and futures are primary; index futures, tech stocks lead",
        "European Session":        "EUR/USD and European indices are most active; US futures may trend ahead of NY open",
        "Asian Session":           "JPY pairs and Asian indices dominate; US instruments often range before London opens",
        "Pre-Market / After Hours": "Low liquidity — stop hunts and false breakouts are common before next session",
    }
    notes.append(session_map.get(session, ""))

    # Critical time zones
    if 13 <= hour < 14:
        notes.append("US open zone: first 30 min often volatile with stop hunts before true direction is set")
    elif 19 <= hour < 21:
        notes.append("US close approaching: position squaring can reverse intraday trends")
    if 7 <= hour < 8:
        notes.append("London open: sharp moves often start here — watch for direction-setting candle")

    # Day-of-week patterns
    day_notes = {
        "Monday": "Monday: gaps from weekend news — first candle direction often holds into mid-week",
        "Wednesday": "Mid-week: highest liquidity day on average, trend moves most reliable",
        "Friday": "Friday: traders close positions before weekend — late fades common after 3 PM ET",
    }
    if day in day_notes:
        notes.append(day_notes[day])

    return ". ".join(n for n in notes if n)


# ── Fear & Greed (alternative.me — free, no API key) ──────────────────────────

def _get_fear_greed() -> dict | None:
    try:
        req = urllib.request.Request(
            "https://api.alternative.me/fng/?limit=1",
            headers={"User-Agent": "WickAI/1.0"},
        )
        with urllib.request.urlopen(req, timeout=4) as resp:
            raw  = json.loads(resp.read().decode("utf-8"))
            fg   = raw["data"][0]
            val  = int(fg["value"])
            label = fg["value_classification"]

            if val < 25:
                ctx = "Extreme Fear — historically a contrarian buy zone; capitulation reversals at major supports carry high reward potential"
            elif val < 45:
                ctx = "Fear — sentiment oversold; quality bullish reversals at support have elevated success probability"
            elif val < 55:
                ctx = "Neutral — no sentiment edge; trade the pattern structure strictly"
            elif val < 75:
                ctx = "Greed — momentum favours longs but chasing extended moves is risky; tighten stops"
            else:
                ctx = "Extreme Greed — historically a contrarian sell zone; bearish reversals at resistance carry elevated probability"

            return {"value": val, "label": label, "context": ctx}
    except Exception as e:
        logger.debug(f"Fear & Greed API unavailable: {e}")
        return None


# ── Prompt builder ─────────────────────────────────────────────────────────────

def format_context_for_prompt(ctx: dict) -> str:
    lines = [
        "## Live Market Intelligence",
        f"- Trading Session: {ctx['session']}",
        f"  Context: {ctx['session_notes']}",
        f"- Day of Week: {ctx['day']}",
    ]

    fg = ctx.get("fear_greed")
    if fg:
        lines.append(
            f"- Market Sentiment: {fg['label']} ({fg['value']}/100)\n"
            f"  Implication: {fg['context']}"
        )

    lines += [
        "",
        "## How to Apply This Context",
        "You MUST factor the above live conditions into your analysis:",
        "- Fear (<45): Weight bullish reversals at key supports more heavily. Mention oversold sentiment as confluence.",
        "- Greed (>55): Weight bearish reversals at resistance more heavily. Note stretched sentiment as warning.",
        "- Extreme readings (<25 or >75): Flag this prominently in analysis_summary as a contrarian signal.",
        "- London/NY Overlap or US Market Hours: Patterns forming now have higher follow-through probability.",
        "- Pre-market/After-Hours: Add a caution about lower liquidity in risk_warning.",
        "- Day-of-week context: Mention briefly in analysis_summary when relevant (Monday gap, Friday fade).",
        "- Always integrate session and sentiment into your analysis_summary naturally — not as a list, as prose.",
    ]

    return "\n".join(lines)
