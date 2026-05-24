"""
WickAI Market Intelligence
Fetches live market context from free sources and injects it into every
AI analysis so Gemini reasons about patterns with full market awareness.
"""

import json
import logging
import time
import urllib.request
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)

_CACHE: dict = {}
_CACHE_TTL = 60   # 1 minute — trading zones can change every few minutes


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
        "trading_zone":  _get_trading_zone(),
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


# ── Red / Yellow / Green trading zones (Raghee Horner system, ET times) ──────

# EDT = UTC-4 (summer), EST = UTC-5 (winter). Using fixed -4 offset (May–Nov).
_ET = timezone(timedelta(hours=-4))

# (start_min, end_min, zone, label, advice)
_ZONE_SCHEDULE = [
    (9*60+30,  9*60+35,  "red",    "Opening Danger",
     "First 5 min: erratic stops and whipsaws — no new entries"),
    (9*60+35,  9*60+50,  "green",  "Green Window",
     "Strong momentum window — A+ setups have high follow-through here"),
    (9*60+50,  10*60+10, "yellow", "Yellow Zone",
     "Volatility spike risk 9:50–10:10 AM — wait for clear structure before entering"),
    (10*60+10, 10*60+35, "green",  "Green Window",
     "Mid-morning green zone — trend continuation trades work well"),
    (10*60+35, 10*60+45, "red",    "10:35 Reversal",
     "Classic 10:35 reversal window — trends often stall or flip direction here"),
    (10*60+45, 14*60+10, "green",  "Green Window",
     "Longest green zone — highest probability window for trend and breakout trades"),
    (14*60+10, 14*60+20, "red",    "2:15 Danger Zone",
     "2:15 PM reversal zone — afternoon trend reversals are common, tighten stops"),
    (14*60+20, 15*60+0,  "green",  "Green Window",
     "Pre-close setup window — momentum trades can still work with tight risk"),
    (15*60+0,  15*60+40, "yellow", "Yellow Zone",
     "3:00–3:40 PM choppy zone — position squaring creates noise, avoid new entries"),
    (15*60+40, 15*60+50, "green",  "Green Window",
     "Brief green window before close — scalps only, very tight stops"),
    (15*60+50, 16*60+0,  "red",    "Close Danger",
     "Final 10 min: erratic — close positions, do not open new ones"),
]


def _get_trading_zone() -> dict:
    """Return Red/Yellow/Green zone for current US ET time."""
    now_et = datetime.now(_ET)
    weekday = now_et.weekday()
    t = now_et.hour * 60 + now_et.minute
    et_str = now_et.strftime("%I:%M %p ET").lstrip("0")

    if weekday >= 5:
        return {"zone": "closed", "color": "#566a85", "label": "Weekend",
                "advice": "Markets closed. Next session Monday 9:30 AM ET.", "et_time": et_str}

    for start, end, zone, label, advice in _ZONE_SCHEDULE:
        if start <= t < end:
            colors = {"red": "#e74c3c", "yellow": "#f0a500", "green": "#2ecc71"}
            return {"zone": zone, "color": colors[zone], "label": label,
                    "advice": advice, "et_time": et_str}

    # Outside 9:30–16:00 ET
    return {"zone": "closed", "color": "#566a85", "label": "Market Closed",
            "advice": "US market is closed. Next session opens at 9:30 AM ET.", "et_time": et_str}


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

    tz = ctx.get("trading_zone")
    if tz and tz["zone"] != "closed":
        zone_color_word = {"red": "RED", "yellow": "YELLOW", "green": "GREEN"}.get(tz["zone"], "")
        lines.append(
            f"- Trading Zone (Raghee Horner system): {zone_color_word} — {tz['label']} ({tz['et_time']})\n"
            f"  Context: {tz['advice']}"
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
        "- Trading Zone RED: Lower confidence — add specific warning in risk_warning about timing danger.",
        "- Trading Zone YELLOW: Moderate caution — note choppy conditions, recommend waiting for confirmation.",
        "- Trading Zone GREEN: Higher conviction — note favourable timing as confluence for the setup.",
        "- Always integrate session, sentiment, and trading zone into your analysis_summary naturally as prose.",
    ]

    return "\n".join(lines)
