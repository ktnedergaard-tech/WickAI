"""
WickAI - FastAPI Backend
Serves the frontend and provides the /api/analyze endpoint for chart analysis.
"""

import asyncio
import logging
import os
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from analyzer import analyze_chart, get_analysis_error_response
from patterns import get_pattern_names

_scan_executor = ThreadPoolExecutor(max_workers=3)

# Load environment variables from .env file if present
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Validate that at least one vision API key is set
_gemini_key = os.getenv("GEMINI_API_KEY")
_groq_key   = os.getenv("GROQ_API_KEY")
if not _gemini_key and not _groq_key:
    logger.warning(
        "No vision API key set — running in demo mode. "
        "Set GROQ_API_KEY (free: console.groq.com) or GEMINI_API_KEY (free: aistudio.google.com)"
    )
elif _groq_key:
    logger.info("Vision provider: Groq (Llama 4 Vision) — free tier")
else:
    logger.info("Vision provider: Google Gemini 2.0 Flash — free tier")

# Max upload size: 10 MB
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB in bytes

# Allowed image MIME types
ALLOWED_MIME_TYPES = {
    "image/jpeg": "image/jpeg",
    "image/jpg": "image/jpeg",
    "image/png": "image/png",
    "image/gif": "image/gif",
    "image/webp": "image/webp",
}

# Paths
BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"

# Initialize FastAPI app
app = FastAPI(
    title="WickAI",
    description="AI-Powered Candlestick Chart Analysis Platform",
    version="1.0.0",
)

# Enable CORS — allow all origins for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", include_in_schema=False)
async def serve_frontend():
    """Serve the main frontend HTML file."""
    index_path = STATIC_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Frontend not found")
    return FileResponse(str(index_path), media_type="text/html")


@app.get("/patterns", include_in_schema=False)
async def serve_patterns():
    p = STATIC_DIR / "patterns.html"
    if not p.exists():
        raise HTTPException(status_code=404, detail="Page not found")
    return FileResponse(str(p), media_type="text/html")


@app.get("/api/strategies")
async def get_strategies():
    names = get_pattern_names()
    return {"count": len(names), "strategies": names}


@app.get("/api/patterns-full")
async def get_patterns_full():
    """Return all patterns with full descriptions and trade guidance."""
    from patterns import CANDLESTICK_PATTERNS
    return {
        "count": len(CANDLESTICK_PATTERNS),
        "patterns": [
            {"key": k, **v}
            for k, v in CANDLESTICK_PATTERNS.items()
        ],
    }


@app.get("/api/prices")
async def get_prices():
    """Return live prices for popular trading instruments using yfinance."""
    import yfinance as yf
    symbols = {
        "NQ": "NQ=F",
        "ES": "ES=F",
        "BTC": "BTC-USD",
        "Gold": "GC=F",
        "EUR/USD": "EURUSD=X",
        "Oil": "CL=F",
    }
    prices = {}
    for name, ticker in symbols.items():
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period="2d", interval="1m")
            if not hist.empty:
                current = float(hist["Close"].iloc[-1])
                prev_close = float(hist["Close"].iloc[0])
                change_pct = ((current - prev_close) / prev_close) * 100
                prices[name] = {
                    "price": round(current, 2),
                    "change_pct": round(change_pct, 2),
                    "ticker": ticker,
                }
        except Exception:
            pass
    return {"prices": prices, "updated": __import__("datetime").datetime.utcnow().isoformat()}


@app.post("/api/scrape")
async def trigger_scrape(secret: str = ""):
    """
    Manually trigger the pattern scraper.
    Pass ?secret=YOUR_SCRAPE_SECRET to authenticate.
    """
    scrape_secret = os.getenv("SCRAPE_SECRET", "")
    if scrape_secret and secret != scrape_secret:
        raise HTTPException(status_code=403, detail="Invalid secret")
    if not ANTHROPIC_API_KEY:
        raise HTTPException(status_code=503, detail="ANTHROPIC_API_KEY not set")

    def run_scraper():
        try:
            from scraper import run
            added = run()
            logger.info(f"Scraper finished: {added} new patterns added")
        except Exception as e:
            logger.error(f"Scraper error: {e}")

    thread = threading.Thread(target=run_scraper, daemon=True)
    thread.start()
    return {"status": "started", "message": "Scraper is running in the background"}


@app.get("/api/scan")
async def scan_endpoint(
    market: str = "ALL",
    interval: str = "1h",
    watchlist: str = "",
):
    """
    Scan US/UK/EU stocks for candlestick patterns.
    market:   ALL | US | UK | EU
    interval: 15m | 1h | 4h | 1d
    watchlist: comma-separated extra tickers (e.g. AAPL,TSLA)
    """
    from scanner import scan_market, scan_all, MARKETS, market_status

    wl = [t.strip().upper() for t in watchlist.split(",") if t.strip()]
    allowed_intervals = {"15m", "30m", "1h", "4h", "1d"}
    if interval not in allowed_intervals:
        interval = "1h"

    loop = asyncio.get_event_loop()

    if market == "ALL":
        raw = await loop.run_in_executor(
            _scan_executor, lambda: scan_all(interval, wl)
        )
        # Flatten + sort for the "All" view (top 30 cross-market)
        all_setups = []
        for ms in raw.values():
            all_setups.extend(ms)
        all_setups.sort(key=lambda s: s["score"], reverse=True)
        return {
            "market": "ALL",
            "interval": interval,
            "setups": all_setups[:30],
            "by_market": {
                m: {"setups": raw[m][:10], "status": market_status(m), **MARKETS[m]}
                for m in MARKETS
            },
            "scanned_at": __import__("datetime").datetime.utcnow().isoformat(),
        }
    elif market in MARKETS:
        setups = await loop.run_in_executor(
            _scan_executor, lambda: scan_market(market, interval, wl)
        )
        return {
            "market": market,
            "interval": interval,
            "setups": setups,
            "status": market_status(market),
            **MARKETS[market],
            "scanned_at": __import__("datetime").datetime.utcnow().isoformat(),
        }
    else:
        raise HTTPException(status_code=400, detail="market must be ALL, US, UK, or EU")


@app.get("/api/scan/status")
async def scan_status():
    """Return open/closed status for all three markets."""
    from scanner import market_status, MARKETS
    return {
        m: {"status": market_status(m), "label": MARKETS[m]["label"], "flag": MARKETS[m]["flag"]}
        for m in MARKETS
    }


@app.get("/api/market-context")
async def get_market_context_endpoint():
    """Return live market context: session, Fear & Greed, session notes."""
    from market_intel import get_market_context
    return get_market_context()


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    gemini = bool(os.getenv("GEMINI_API_KEY"))
    groq   = bool(os.getenv("GROQ_API_KEY"))
    if groq:
        provider = "groq"
    elif gemini:
        provider = "gemini"
    else:
        provider = "demo"
    return {
        "status":   "ok",
        "service":  "WickAI",
        "version":  "1.0.0",
        "provider": provider,
        "analysis_ready": groq or gemini,
    }


@app.post("/api/analyze")
async def analyze_chart_endpoint(file: UploadFile = File(...)):
    """
    Analyze a candlestick chart image using Claude Vision AI.

    Accepts a multipart/form-data image upload and returns a structured
    JSON analysis with trade recommendations.
    """
    # Validate content type
    content_type = file.content_type or ""
    # Normalize content type (some browsers send image/jpg instead of image/jpeg)
    normalized_mime = ALLOWED_MIME_TYPES.get(content_type.lower())
    if not normalized_mime:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {content_type}. Allowed types: JPEG, PNG, GIF, WebP.",
        )

    # Read file contents
    image_bytes = await file.read()

    # Validate file size
    if len(image_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    if len(image_bytes) > MAX_FILE_SIZE:
        size_mb = len(image_bytes) / (1024 * 1024)
        raise HTTPException(
            status_code=413,
            detail=f"File too large: {size_mb:.1f}MB. Maximum allowed size is 10MB.",
        )

    logger.info(
        f"Received chart for analysis: {file.filename!r}, "
        f"{normalized_mime}, {len(image_bytes) / 1024:.1f}KB"
    )

    # Perform analysis
    try:
        analysis = analyze_chart(image_bytes, normalized_mime)
        logger.info(
            f"Analysis complete: pattern={analysis.get('pattern_name')!r}, "
            f"direction={analysis.get('trade_direction')!r}, "
            f"confidence={analysis.get('confidence')}"
        )
        return JSONResponse(content=analysis)

    except ValueError as e:
        # Known, handled errors from the analyzer
        logger.error(f"Analysis error: {e}")
        error_response = get_analysis_error_response(str(e))
        return JSONResponse(content=error_response, status_code=422)

    except Exception as e:
        # Unexpected errors
        logger.exception(f"Unexpected error during chart analysis: {e}")
        error_response = get_analysis_error_response(
            "An unexpected error occurred. Please try again."
        )
        return JSONResponse(content=error_response, status_code=500)


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info",
    )
