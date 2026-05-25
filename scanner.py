"""
WickAI Market Scanner
Scans US, UK, and EU stocks for candlestick patterns using free yfinance data.
No extra API key required. Results cached for 15 minutes per market.
"""

import logging
import time
from datetime import datetime, timezone
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)

# ── Ticker universes ───────────────────────────────────────────────────────────

US_TICKERS = [
    "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "LLY", "AVGO", "TSLA",
    "WMT", "JPM", "V", "UNH", "XOM", "ORCL", "MA", "COST", "HD", "PG",
    "JNJ", "BAC", "ABBV", "CRM", "KO", "CVX", "MRK", "NFLX", "AMD",
    "PEP", "TMO", "ACN", "MCD", "ADBE", "WFC", "GE", "PM", "NOW",
    "TXN", "AMGN", "CAT", "SPGI", "ISRG", "INTU", "BKNG", "AXP",
    "IBM", "DHR", "LIN", "QCOM", "UBER",
]

UK_TICKERS = [
    "AZN.L", "SHEL.L", "HSBA.L", "ULVR.L", "RIO.L", "BP.L", "GSK.L",
    "LSEG.L", "REL.L", "NG.L", "DGE.L", "BAE.L", "NWG.L", "LLOY.L",
    "VOD.L", "BARC.L", "IMB.L", "SSE.L", "RKT.L", "EXPN.L",
    "WPP.L", "IAG.L", "STAN.L", "PRU.L", "BATS.L", "BHP.L",
    "SGE.L", "CNA.L", "ABF.L", "HLN.L",
]

EU_TICKERS = [
    # DAX
    "SAP.DE", "SIE.DE", "ALV.DE", "MBG.DE", "BMW.DE", "BAS.DE",
    "BAYN.DE", "DTE.DE", "EOAN.DE", "ADS.DE", "DB1.DE", "RWE.DE",
    "MUV2.DE", "VOW3.DE", "HEN3.DE",
    # CAC
    "MC.PA", "OR.PA", "TTE.PA", "BNP.PA", "SAN.PA", "AIR.PA",
    "SU.PA", "RI.PA", "AI.PA", "DG.PA", "ENGI.PA", "SGO.PA",
    "VIE.PA", "CAP.PA", "RNO.PA",
]

MARKETS = {
    "US": {"tickers": US_TICKERS, "label": "S&P 500",  "flag": "🇺🇸", "tz": "US/Eastern"},
    "UK": {"tickers": UK_TICKERS, "label": "FTSE 100", "flag": "🇬🇧", "tz": "Europe/London"},
    "EU": {"tickers": EU_TICKERS, "label": "DAX/CAC",  "flag": "🇪🇺", "tz": "Europe/Berlin"},
}

# ── Cache ──────────────────────────────────────────────────────────────────────
_SCAN_CACHE: dict = {}
_CACHE_TTL  = 15 * 60   # 15 minutes


# ── OHLCV fetching ─────────────────────────────────────────────────────────────

def _get_ohlcv(ticker: str, interval: str = "1h", period: str = "5d") -> Optional[pd.DataFrame]:
    try:
        import yfinance as yf
        df = yf.download(ticker, interval=interval, period=period,
                         progress=False, auto_adjust=True)
        if df is None or len(df) < 6:
            return None
        # yfinance ≥0.2 returns MultiIndex columns even for single tickers
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [col[0].lower() for col in df.columns]
        else:
            df.columns = [c.lower() for c in df.columns]
        return df.dropna()
    except Exception as e:
        logger.debug(f"yfinance {ticker}: {e}")
        return None


# ── Candle helpers ─────────────────────────────────────────────────────────────

def _f(val) -> float:
    """Safe float extraction from pandas scalar or Series."""
    try:
        return float(val.iloc[0]) if hasattr(val, "iloc") else float(val)
    except Exception:
        return 0.0

def _body(r) -> float:   return abs(_f(r["close"]) - _f(r["open"]))
def _uw(r)   -> float:   return _f(r["high"]) - max(_f(r["open"]), _f(r["close"]))
def _lw(r)   -> float:   return min(_f(r["open"]), _f(r["close"])) - _f(r["low"])
def _rng(r)  -> float:   return _f(r["high"]) - _f(r["low"])
def _bull(r) -> bool:    return _f(r["close"]) > _f(r["open"])
def _bear(r) -> bool:    return _f(r["close"]) < _f(r["open"])


# ── Pattern detection ──────────────────────────────────────────────────────────

def detect_patterns(df: pd.DataFrame) -> list[dict]:
    """Detect candlestick patterns. Returns list of found patterns with scores."""
    if len(df) < 5:
        return []

    c0, c1, c2 = df.iloc[-1], df.iloc[-2], df.iloc[-3]
    b0, b1, b2 = _body(c0), _body(c1), _body(c2)
    uw0, lw0   = _uw(c0), _lw(c0)
    r0         = _rng(c0)

    tail      = df.iloc[-20:]
    avg_body  = tail.apply(lambda r: _body(r), axis=1).mean()
    avg_range = (df["high"] - df["low"]).iloc[-20:].apply(_f).mean()

    # ── Trend (last 20 candles) ────────────────────────────────────────────────
    closes = df["close"].iloc[-20:].apply(_f)
    if closes.iloc[-1] > closes.iloc[-5] and closes.iloc[-5] > closes.iloc[-10]:
        trend = "up"
    elif closes.iloc[-1] < closes.iloc[-5] and closes.iloc[-5] < closes.iloc[-10]:
        trend = "down"
    else:
        trend = "sideways"

    # ── Position in 20-candle range ────────────────────────────────────────────
    hi20   = df["high"].iloc[-20:].apply(_f).max()
    lo20   = df["low"].iloc[-20:].apply(_f).min()
    rng20  = hi20 - lo20
    pos    = (_f(c0["close"]) - lo20) / rng20 if rng20 > 0 else 0.5
    at_sup = pos < 0.25
    at_res = pos > 0.75

    found: list[dict] = []

    def add(name, ptype, direction, score, strength="moderate"):
        found.append({
            "pattern_name":   name,
            "pattern_type":   ptype,
            "trade_direction": direction,
            "score":          min(int(score), 10),
            "trend":          trend,
            "strength":       strength,
        })

    # ── Single-candle ──────────────────────────────────────────────────────────

    # Doji
    if b0 < avg_range * 0.08 and r0 > avg_range * 0.4:
        add("Doji", "neutral", "WAIT", 5 + (1 if at_sup or at_res else 0))

    # Hammer  (long lower wick, small body, no upper wick, at bottom)
    if b0 > 0 and lw0 >= b0 * 2 and uw0 <= b0 * 0.5 and r0 > avg_range * 0.4:
        s = 6 + (2 if trend == "down" else 0) + (1 if at_sup else 0)
        add("Hammer", "bullish", "LONG", s, "strong" if s >= 8 else "moderate")

    # Shooting Star  (long upper wick, small body, at top)
    if b0 > 0 and uw0 >= b0 * 2 and lw0 <= b0 * 0.5 and r0 > avg_range * 0.4:
        s = 6 + (2 if trend == "up" else 0) + (1 if at_res else 0)
        add("Shooting Star", "bearish", "SHORT", s, "strong" if s >= 8 else "moderate")

    # Inverted Hammer  (at bottom, needs confirmation — still bullish bias)
    if b0 > 0 and uw0 >= b0 * 2 and lw0 <= b0 * 0.5 and trend == "down" and at_sup:
        add("Inverted Hammer", "bullish", "LONG", 6)

    # Hanging Man  (at top)
    if b0 > 0 and lw0 >= b0 * 2 and uw0 <= b0 * 0.5 and trend == "up" and at_res:
        add("Hanging Man", "bearish", "SHORT", 6)

    # Marubozu  (full body, almost no wicks — pure momentum)
    if b0 > avg_body * 1.8 and uw0 < b0 * 0.05 and lw0 < b0 * 0.05:
        if _bull(c0):
            s = 7 + (1 if trend == "up" else 0)
            add("Bullish Marubozu", "bullish", "LONG", s, "strong")
        else:
            s = 7 + (1 if trend == "down" else 0)
            add("Bearish Marubozu", "bearish", "SHORT", s, "strong")

    # Pin Bar  (any direction — large wick relative to total range)
    if r0 > avg_range * 0.6:
        dominant_wick = max(uw0, lw0)
        if dominant_wick > r0 * 0.6 and b0 < r0 * 0.25:
            if lw0 > uw0:
                s = 7 + (1 if trend == "down" else 0) + (1 if at_sup else 0)
                add("Bullish Pin Bar", "bullish", "LONG", s, "strong" if s >= 8 else "moderate")
            else:
                s = 7 + (1 if trend == "up" else 0) + (1 if at_res else 0)
                add("Bearish Pin Bar", "bearish", "SHORT", s, "strong" if s >= 8 else "moderate")

    # ── Two-candle ─────────────────────────────────────────────────────────────

    # Bullish Engulfing
    if (_bear(c1) and _bull(c0)
            and _f(c0["open"]) <= _f(c1["close"])
            and _f(c0["close"]) >= _f(c1["open"])
            and b0 > b1):
        s = 7 + (1 if trend == "down" else 0) + (1 if at_sup else 0)
        add("Bullish Engulfing", "bullish", "LONG", s, "strong" if s >= 8 else "moderate")

    # Bearish Engulfing
    if (_bull(c1) and _bear(c0)
            and _f(c0["open"]) >= _f(c1["close"])
            and _f(c0["close"]) <= _f(c1["open"])
            and b0 > b1):
        s = 7 + (1 if trend == "up" else 0) + (1 if at_res else 0)
        add("Bearish Engulfing", "bearish", "SHORT", s, "strong" if s >= 8 else "moderate")

    # Bullish Harami  (small candle inside prior bearish)
    if (_bear(c1) and _bull(c0)
            and _f(c0["open"]) > _f(c1["close"])
            and _f(c0["close"]) < _f(c1["open"])
            and b0 < b1 * 0.6):
        add("Bullish Harami", "bullish", "LONG", 6 + (1 if trend == "down" else 0))

    # Bearish Harami
    if (_bull(c1) and _bear(c0)
            and _f(c0["open"]) < _f(c1["close"])
            and _f(c0["close"]) > _f(c1["open"])
            and b0 < b1 * 0.6):
        add("Bearish Harami", "bearish", "SHORT", 6 + (1 if trend == "up" else 0))

    # Tweezer Bottom  (same low, after down-move)
    if (abs(_f(c0["low"]) - _f(c1["low"])) < avg_range * 0.03
            and trend == "down" and at_sup):
        add("Tweezer Bottom", "bullish", "LONG", 7, "moderate")

    # Tweezer Top  (same high, after up-move)
    if (abs(_f(c0["high"]) - _f(c1["high"])) < avg_range * 0.03
            and trend == "up" and at_res):
        add("Tweezer Top", "bearish", "SHORT", 7, "moderate")

    # ── Three-candle ───────────────────────────────────────────────────────────

    # Morning Star
    if (_bear(c2) and b2 > avg_body
            and b1 < avg_body * 0.5
            and _bull(c0) and b0 > avg_body
            and _f(c0["close"]) > (_f(c2["open"]) + _f(c2["close"])) / 2):
        s = 8 + (1 if trend == "down" else 0)
        add("Morning Star", "bullish", "LONG", s, "strong")

    # Evening Star
    if (_bull(c2) and b2 > avg_body
            and b1 < avg_body * 0.5
            and _bear(c0) and b0 > avg_body
            and _f(c0["close"]) < (_f(c2["open"]) + _f(c2["close"])) / 2):
        s = 8 + (1 if trend == "up" else 0)
        add("Evening Star", "bearish", "SHORT", s, "strong")

    # Three White Soldiers
    if len(df) >= 4:
        last3 = [df.iloc[-i] for i in range(1, 4)]
        if (all(_bull(c) for c in last3)
                and all(_body(c) > avg_body * 0.8 for c in last3)
                and _f(df.iloc[-1]["close"]) > _f(df.iloc[-2]["close"]) > _f(df.iloc[-3]["close"])):
            add("Three White Soldiers", "bullish", "LONG", 8, "strong")

    # Three Black Crows
    if len(df) >= 4:
        last3 = [df.iloc[-i] for i in range(1, 4)]
        if (all(_bear(c) for c in last3)
                and all(_body(c) > avg_body * 0.8 for c in last3)
                and _f(df.iloc[-1]["close"]) < _f(df.iloc[-2]["close"]) < _f(df.iloc[-3]["close"])):
            add("Three Black Crows", "bearish", "SHORT", 8, "strong")

    return found


# ── Enrich setup with price context ───────────────────────────────────────────

def _enrich(patterns: list[dict], df: pd.DataFrame, ticker: str, market: str, interval: str) -> dict | None:
    if not patterns:
        return None
    best = max(patterns, key=lambda p: p["score"])
    last  = df.iloc[-1]
    prev  = df.iloc[-2]
    hi20  = float(df["high"].iloc[-20:].apply(_f).max())
    lo20  = float(df["low"].iloc[-20:].apply(_f).min())
    atr   = float((df["high"] - df["low"]).iloc[-14:].apply(
                lambda r: _f(r["high"]) - _f(r["low"]) if hasattr(r, "__iter__") else r,
            ).mean()) if False else float(
                (df["high"].apply(_f) - df["low"].apply(_f)).iloc[-14:].mean()
            )

    price      = round(_f(last["close"]), 4)
    prev_price = round(_f(prev["close"]), 4)
    change_pct = round((price - prev_price) / prev_price * 100, 2) if prev_price else 0.0

    return {
        **best,
        "ticker":     ticker,
        "market":     market,
        "interval":   interval,
        "price":      price,
        "change_pct": change_pct,
        "resistance": round(hi20, 4),
        "support":    round(lo20, 4),
        "atr":        round(atr, 4),
        "scanned_at": datetime.now(timezone.utc).isoformat(),
    }


# ── Market open check ──────────────────────────────────────────────────────────

def market_status(market: str) -> dict:
    """Return whether a market is currently open and session info."""
    now = datetime.now(timezone.utc)
    wd  = now.weekday()   # 0=Mon … 6=Sun
    t   = now.hour * 60 + now.minute

    if wd >= 5:
        return {"open": False, "label": "Weekend"}

    if market == "US":
        open_ = 13 * 60 + 30 <= t < 20 * 60
        return {"open": open_, "label": "Open" if open_ else "Pre/After-Market"}
    if market == "UK":
        open_ = 8 * 60 <= t < 16 * 60 + 30
        return {"open": open_, "label": "Open" if open_ else "Closed"}
    if market == "EU":
        open_ = 8 * 60 <= t < 17 * 60 + 30
        return {"open": open_, "label": "Open" if open_ else "Closed"}

    return {"open": True, "label": "Unknown"}


# ── Core scan function ─────────────────────────────────────────────────────────

def scan_market(market: str, interval: str = "1h",
                watchlist: list[str] | None = None) -> list[dict]:
    """
    Scan all tickers for a market (+ optional watchlist extras).
    Returns setups sorted by score desc, cached for _CACHE_TTL.
    """
    cache_key = f"{market}:{interval}"
    now = time.time()
    if cache_key in _SCAN_CACHE:
        c = _SCAN_CACHE[cache_key]
        if now - c["ts"] < _CACHE_TTL:
            logger.info(f"Cache hit: {market}/{interval} ({len(c['results'])} setups)")
            return c["results"]

    tickers = list(MARKETS[market]["tickers"])
    if watchlist:
        extras = [t.upper() for t in watchlist if t.upper() not in tickers]
        tickers = extras + tickers

    period = "5d" if interval in ("15m", "30m", "1h") else "30d"
    setups: list[dict] = []

    logger.info(f"Scanning {len(tickers)} tickers [{market}, {interval}]…")

    for ticker in tickers:
        try:
            df = _get_ohlcv(ticker, interval=interval, period=period)
            if df is None:
                continue
            patterns = detect_patterns(df)
            setup    = _enrich(patterns, df, ticker, market, interval)
            if setup and setup["score"] >= 6:
                setups.append(setup)
        except Exception as e:
            logger.debug(f"Skip {ticker}: {e}")
        time.sleep(0.15)   # polite delay — keeps yfinance happy

    setups.sort(key=lambda s: s["score"], reverse=True)
    _SCAN_CACHE[cache_key] = {"ts": now, "results": setups}
    logger.info(f"Scan done: {len(setups)} setups in {market}/{interval}")
    return setups


def scan_all(interval: str = "1h", watchlist: list[str] | None = None) -> dict:
    """Scan all three markets. Returns {market: [setups]}."""
    return {m: scan_market(m, interval=interval, watchlist=watchlist) for m in MARKETS}


def get_top_setups(n: int = 20, interval: str = "1h",
                   watchlist: list[str] | None = None) -> list[dict]:
    """Return top N setups across all markets, ranked by score."""
    all_s = []
    for ms in scan_all(interval=interval, watchlist=watchlist).values():
        all_s.extend(ms)
    all_s.sort(key=lambda s: s["score"], reverse=True)
    return all_s[:n]
