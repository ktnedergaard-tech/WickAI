"""
WickAI Market Scanner
Uses TradingView Screener API as primary data source (no API key needed).
Falls back to yfinance if TradingView is unavailable.
Results cached for 15 minutes per market+interval.
"""

import logging
import time
from datetime import datetime, timezone
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)

# ── Market definitions ─────────────────────────────────────────────────────────

MARKETS = {
    "US": {"label": "S&P 500",  "flag": "🇺🇸", "tv_market": "america"},
    "UK": {"label": "FTSE 100", "flag": "🇬🇧", "tv_market": "uk"},
    "EU": {"label": "DAX/CAC",  "flag": "🇪🇺", "tv_market": "germany"},
}

# TradingView interval mapping  (our interval → TV column suffix)
_TV_INTERVAL = {
    "15m": "|15",
    "30m": "|30",
    "1h":  "|60",
    "4h":  "|240",
    "1d":  "|1D",
}

# ── Cache ──────────────────────────────────────────────────────────────────────
_SCAN_CACHE: dict = {}
_CACHE_TTL  = 15 * 60   # 15 minutes

# ── TradingView Screener scan ──────────────────────────────────────────────────

def _tv_scan(market: str, interval: str = "1h", limit: int = 50) -> list[dict]:
    """
    Query TradingView's screener for the top setups in a market.
    Returns a list of setup dicts ready to return from the API.
    """
    from tradingview_screener import Query, Column

    tv_market = MARKETS[market]["tv_market"]
    sfx = _TV_INTERVAL.get(interval, "|60")

    # TradingView candlestick pattern columns (value: 1=bullish, -1=bearish, 0=none)
    pattern_cols = [
        f"Candle.Hammer{sfx}",
        f"Candle.ShootingStar{sfx}",
        f"Candle.Doji{sfx}",
        f"Candle.Engulf{sfx}",
        f"Candle.Harami{sfx}",
        f"Candle.MorningStar{sfx}",
        f"Candle.EveningStar{sfx}",
        f"Candle.3WhiteSoldiers{sfx}",
        f"Candle.3BlackCrows{sfx}",
        f"Candle.AbandonedBaby{sfx}",
        f"Candle.PiercingLine{sfx}",
        f"Candle.DarkCloudCover{sfx}",
    ]

    cols = [
        "name", "description",
        f"close{sfx}", f"change{sfx}", f"volume{sfx}",
        f"RSI{sfx}", f"EMA20{sfx}", f"EMA50{sfx}",
        f"High.1M{sfx}", f"Low.1M{sfx}",
        f"ATR{sfx}",
        f"Recommend.All{sfx}",
    ] + pattern_cols

    # Build filter: at least one pattern must be non-zero
    pattern_filters = [Column(p) != 0 for p in pattern_cols]
    filter_clause = pattern_filters[0]
    for f in pattern_filters[1:]:
        filter_clause = filter_clause | f

    try:
        _, df = (
            Query()
            .set_markets(tv_market)
            .select(*cols)
            .where(
                filter_clause,
                Column("market_cap_basic") > 500_000_000,
                Column(f"volume{sfx}") > 100_000,
            )
            .order_by(f"volume{sfx}", ascending=False)
            .limit(limit)
            .get_scanner_data()
        )
    except Exception as e:
        logger.warning(f"TradingView screener failed [{market}/{interval}]: {e}")
        return []

    setups = []
    for _, row in df.iterrows():
        try:
            setup = _tv_row_to_setup(row, market, interval, sfx, pattern_cols)
            if setup:
                setups.append(setup)
        except Exception as e:
            logger.debug(f"TV row parse error: {e}")

    return setups


_TV_PATTERN_NAMES = {
    "Candle.Hammer":           "Hammer",
    "Candle.ShootingStar":     "Shooting Star",
    "Candle.Doji":             "Doji",
    "Candle.Engulf":           "Engulfing",
    "Candle.Harami":           "Harami",
    "Candle.MorningStar":      "Morning Star",
    "Candle.EveningStar":      "Evening Star",
    "Candle.3WhiteSoldiers":   "Three White Soldiers",
    "Candle.3BlackCrows":      "Three Black Crows",
    "Candle.AbandonedBaby":    "Abandoned Baby",
    "Candle.PiercingLine":     "Piercing Line",
    "Candle.DarkCloudCover":   "Dark Cloud Cover",
}

_BULLISH_PATTERNS = {"Hammer", "Morning Star", "Three White Soldiers",
                     "Abandoned Baby", "Piercing Line", "Engulfing"}
_BEARISH_PATTERNS = {"Shooting Star", "Evening Star", "Three Black Crows",
                     "Dark Cloud Cover", "Engulfing"}


def _tv_row_to_setup(row, market: str, interval: str, sfx: str,
                     pattern_cols: list) -> Optional[dict]:
    def g(col):
        return row.get(col, row.get(col.replace(sfx, ""), None))

    ticker = str(row.get("name", "")).replace(":", "").strip()
    if not ticker:
        return None

    price      = float(g(f"close{sfx}") or 0)
    change_pct = float(g(f"change{sfx}") or 0)
    hi20       = float(g(f"High.1M{sfx}") or price * 1.05)
    lo20       = float(g(f"Low.1M{sfx}") or price * 0.95)
    atr        = float(g(f"ATR{sfx}") or price * 0.01)
    recommend  = float(g(f"Recommend.All{sfx}") or 0)
    rsi        = float(g(f"RSI{sfx}") or 50)

    # Find active patterns
    active_patterns = []
    for col in pattern_cols:
        val = g(col)
        if val and val != 0:
            base = col.replace(sfx, "")
            name = _TV_PATTERN_NAMES.get(base, base.split(".")[-1])
            direction = "bullish" if val > 0 else "bearish"
            active_patterns.append((name, direction, int(val)))

    if not active_patterns:
        return None

    # Pick the best pattern (prefer multi-candle)
    multi = [p for p in active_patterns if p[0] in
             {"Morning Star", "Evening Star", "Three White Soldiers",
              "Three Black Crows", "Abandoned Baby", "Engulfing"}]
    chosen_name, chosen_dir, _ = (multi[0] if multi else active_patterns[0])

    # Determine trade direction
    if chosen_dir == "bullish":
        trade_dir = "LONG"
        pattern_type = "bullish"
    elif chosen_dir == "bearish":
        trade_dir = "SHORT"
        pattern_type = "bearish"
    else:
        trade_dir = "WAIT"
        pattern_type = "neutral"

    # Score 1–10 based on recommendation strength, RSI positioning, pattern quality
    score = 5
    score += min(3, int(abs(recommend) * 3))   # TV's own signal strength
    if trade_dir == "LONG"  and rsi < 40: score += 1   # oversold
    if trade_dir == "SHORT" and rsi > 60: score += 1   # overbought
    if chosen_name in {"Morning Star", "Evening Star",
                       "Three White Soldiers", "Three Black Crows",
                       "Abandoned Baby"}:
        score += 1   # stronger multi-candle patterns
    score = min(10, score)

    # Trend from RSI direction
    if   recommend > 0.2:  trend = "up"
    elif recommend < -0.2: trend = "down"
    else:                  trend = "sideways"

    return {
        "ticker":        ticker,
        "market":        market,
        "interval":      interval,
        "pattern_name":  chosen_name,
        "pattern_type":  pattern_type,
        "trade_direction": trade_dir,
        "score":         score,
        "trend":         trend,
        "strength":      "strong" if score >= 8 else "moderate",
        "price":         round(price, 4),
        "change_pct":    round(change_pct, 2),
        "resistance":    round(hi20, 4),
        "support":       round(lo20, 4),
        "atr":           round(atr, 4),
        "scanned_at":    datetime.now(timezone.utc).isoformat(),
    }


# ── yfinance fallback ──────────────────────────────────────────────────────────

_YF_TICKERS = {
    "US": [
        "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA", "JPM",
        "V", "XOM", "JNJ", "WMT", "PG", "MA", "HD", "BAC", "ABBV", "CVX",
        "NFLX", "AMD", "KO", "PEP", "MCD", "ADBE", "CRM", "ORCL", "QCOM",
    ],
    "UK": [
        "AZN.L", "SHEL.L", "HSBA.L", "BP.L", "GSK.L", "RIO.L", "ULVR.L",
        "LSEG.L", "BAE.L", "NWG.L", "LLOY.L", "VOD.L", "BARC.L",
    ],
    "EU": [
        "SAP.DE", "SIE.DE", "ALV.DE", "MBG.DE", "BMW.DE", "BAS.DE",
        "MC.PA", "OR.PA", "TTE.PA", "BNP.PA", "AIR.PA", "SU.PA",
    ],
}


def _make_yf_session():
    import requests
    s = requests.Session()
    s.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        ),
    })
    try:
        s.get("https://finance.yahoo.com", timeout=5)
    except Exception:
        pass
    return s


def _get_ohlcv(ticker: str, interval: str = "1h", period: str = "5d"):
    import yfinance as yf
    session = _make_yf_session()
    try:
        t = yf.Ticker(ticker, session=session)
        df = t.history(interval=interval, period=period,
                       auto_adjust=True, raise_errors=False)
        if df is not None and len(df) >= 6:
            df.columns = [c.lower() for c in df.columns]
            return df.dropna()
    except Exception:
        pass
    try:
        df = yf.download(ticker, interval=interval, period=period,
                         progress=False, auto_adjust=True, session=session)
        if df is not None and len(df) >= 6:
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = [col[0].lower() for col in df.columns]
            else:
                df.columns = [c.lower() for c in df.columns]
            return df.dropna()
    except Exception as e:
        logger.debug(f"yfinance {ticker}: {e}")
    return None


def _f(val) -> float:
    try:
        return float(val.iloc[0]) if hasattr(val, "iloc") else float(val)
    except Exception:
        return 0.0

def _body(r): return abs(_f(r["close"]) - _f(r["open"]))
def _uw(r):   return _f(r["high"]) - max(_f(r["open"]), _f(r["close"]))
def _lw(r):   return min(_f(r["open"]), _f(r["close"])) - _f(r["low"])
def _rng(r):  return _f(r["high"]) - _f(r["low"])
def _bull(r): return _f(r["close"]) > _f(r["open"])
def _bear(r): return _f(r["close"]) < _f(r["open"])


def _detect_patterns_yf(df: pd.DataFrame) -> list[dict]:
    if len(df) < 5:
        return []
    c0, c1, c2 = df.iloc[-1], df.iloc[-2], df.iloc[-3]
    b0, b1, b2 = _body(c0), _body(c1), _body(c2)
    uw0, lw0, r0 = _uw(c0), _lw(c0), _rng(c0)
    avg_body  = df.iloc[-20:].apply(_body, axis=1).mean()
    avg_range = (df["high"].apply(_f) - df["low"].apply(_f)).iloc[-20:].mean()
    closes    = df["close"].iloc[-20:].apply(_f)
    trend     = ("up"   if closes.iloc[-1] > closes.iloc[-5] > closes.iloc[-10] else
                 "down" if closes.iloc[-1] < closes.iloc[-5] < closes.iloc[-10] else
                 "sideways")
    hi20 = df["high"].iloc[-20:].apply(_f).max()
    lo20 = df["low"].iloc[-20:].apply(_f).min()
    pos  = (_f(c0["close"]) - lo20) / (hi20 - lo20) if (hi20 - lo20) > 0 else 0.5
    at_sup, at_res = pos < 0.25, pos > 0.75
    found = []

    def add(name, ptype, direction, score):
        found.append({"pattern_name": name, "pattern_type": ptype,
                      "trade_direction": direction, "score": min(int(score), 10),
                      "trend": trend, "strength": "strong" if score >= 8 else "moderate"})

    if b0 < avg_range * 0.08 and r0 > avg_range * 0.4:
        add("Doji", "neutral", "WAIT", 5)
    if b0 > 0 and lw0 >= b0*2 and uw0 <= b0*0.5 and r0 > avg_range*0.4:
        add("Hammer", "bullish", "LONG", 6 + (2 if trend=="down" else 0) + (1 if at_sup else 0))
    if b0 > 0 and uw0 >= b0*2 and lw0 <= b0*0.5 and r0 > avg_range*0.4:
        add("Shooting Star", "bearish", "SHORT", 6 + (2 if trend=="up" else 0) + (1 if at_res else 0))
    if b0 > avg_body*1.8 and uw0 < b0*0.05 and lw0 < b0*0.05:
        if _bull(c0): add("Bullish Marubozu", "bullish", "LONG",  7 + (1 if trend=="up" else 0))
        else:         add("Bearish Marubozu", "bearish", "SHORT", 7 + (1 if trend=="down" else 0))
    if r0 > avg_range*0.6:
        dw = max(uw0, lw0)
        if dw > r0*0.6 and b0 < r0*0.25:
            if lw0 > uw0: add("Bullish Pin Bar", "bullish", "LONG",  7 + (1 if trend=="down" else 0) + (1 if at_sup else 0))
            else:          add("Bearish Pin Bar", "bearish", "SHORT", 7 + (1 if trend=="up"   else 0) + (1 if at_res else 0))
    if _bear(c1) and _bull(c0) and _f(c0["open"]) <= _f(c1["close"]) and _f(c0["close"]) >= _f(c1["open"]) and b0 > b1:
        add("Bullish Engulfing", "bullish", "LONG", 7 + (1 if trend=="down" else 0) + (1 if at_sup else 0))
    if _bull(c1) and _bear(c0) and _f(c0["open"]) >= _f(c1["close"]) and _f(c0["close"]) <= _f(c1["open"]) and b0 > b1:
        add("Bearish Engulfing", "bearish", "SHORT", 7 + (1 if trend=="up" else 0) + (1 if at_res else 0))
    if (_bear(c2) and b2 > avg_body and b1 < avg_body*0.5 and _bull(c0) and b0 > avg_body
            and _f(c0["close"]) > (_f(c2["open"]) + _f(c2["close"])) / 2):
        add("Morning Star", "bullish", "LONG", 8 + (1 if trend=="down" else 0))
    if (_bull(c2) and b2 > avg_body and b1 < avg_body*0.5 and _bear(c0) and b0 > avg_body
            and _f(c0["close"]) < (_f(c2["open"]) + _f(c2["close"])) / 2):
        add("Evening Star", "bearish", "SHORT", 8 + (1 if trend=="up" else 0))
    return found


def _yf_scan(market: str, interval: str = "1h",
             watchlist: list[str] | None = None) -> list[dict]:
    tickers = list(_YF_TICKERS.get(market, []))
    if watchlist:
        extras = [t.upper() for t in watchlist if t.upper() not in tickers]
        tickers = extras + tickers
    period = "5d" if interval in ("15m", "30m", "1h") else "30d"
    setups = []
    for ticker in tickers:
        try:
            df = _get_ohlcv(ticker, interval=interval, period=period)
            if df is None:
                continue
            patterns = _detect_patterns_yf(df)
            if not patterns:
                continue
            best = max(patterns, key=lambda p: p["score"])
            if best["score"] < 6:
                continue
            last = df.iloc[-1]
            prev = df.iloc[-2]
            price      = round(_f(last["close"]), 4)
            prev_price = round(_f(prev["close"]), 4)
            hi20 = float(df["high"].apply(_f).iloc[-20:].max())
            lo20 = float(df["low"].apply(_f).iloc[-20:].min())
            atr  = float((df["high"].apply(_f) - df["low"].apply(_f)).iloc[-14:].mean())
            setups.append({
                **best,
                "ticker":     ticker,
                "market":     market,
                "interval":   interval,
                "price":      price,
                "change_pct": round((price - prev_price) / prev_price * 100, 2) if prev_price else 0.0,
                "resistance": round(hi20, 4),
                "support":    round(lo20, 4),
                "atr":        round(atr, 4),
                "scanned_at": datetime.now(timezone.utc).isoformat(),
            })
        except Exception as e:
            logger.debug(f"Skip {ticker}: {e}")
        time.sleep(0.1)
    setups.sort(key=lambda s: s["score"], reverse=True)
    return setups


# ── Market open check ──────────────────────────────────────────────────────────

def market_status(market: str) -> dict:
    now = datetime.now(timezone.utc)
    wd  = now.weekday()
    t   = now.hour * 60 + now.minute
    if wd >= 5:
        return {"open": False, "label": "Weekend"}
    if market == "US":
        open_ = 13*60+30 <= t < 20*60
        return {"open": open_, "label": "Open" if open_ else "Pre/After-Market"}
    if market in ("UK", "EU"):
        open_ = 8*60 <= t < 17*60+30
        return {"open": open_, "label": "Open" if open_ else "Closed"}
    return {"open": True, "label": "Unknown"}


# ── Public scan functions ──────────────────────────────────────────────────────

def scan_market(market: str, interval: str = "1h",
                watchlist: list[str] | None = None) -> list[dict]:
    cache_key = f"{market}:{interval}"
    now = time.time()
    if cache_key in _SCAN_CACHE:
        c = _SCAN_CACHE[cache_key]
        if now - c["ts"] < _CACHE_TTL:
            logger.info(f"Cache hit: {market}/{interval} ({len(c['results'])} setups)")
            return c["results"]

    logger.info(f"Scanning {market}/{interval} via TradingView…")
    setups = _tv_scan(market, interval)

    if not setups:
        logger.info(f"TradingView returned 0 results, falling back to yfinance [{market}]")
        setups = _yf_scan(market, interval, watchlist)
    elif watchlist:
        # Merge watchlist tickers (yfinance for those specific tickers)
        wl_setups = _yf_scan("US", interval, watchlist)
        existing  = {s["ticker"] for s in setups}
        setups   += [s for s in wl_setups if s["ticker"] not in existing]

    setups.sort(key=lambda s: s["score"], reverse=True)
    _SCAN_CACHE[cache_key] = {"ts": now, "results": setups}
    logger.info(f"Scan done: {len(setups)} setups [{market}/{interval}]")
    return setups


def scan_all(interval: str = "1h", watchlist: list[str] | None = None) -> dict:
    return {m: scan_market(m, interval=interval, watchlist=watchlist) for m in MARKETS}
