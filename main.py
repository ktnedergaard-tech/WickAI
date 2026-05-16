"""
WickAI - FastAPI Backend
Serves the frontend and provides the /api/analyze endpoint for chart analysis.
"""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from analyzer import analyze_chart, get_analysis_error_response

# Load environment variables from .env file if present
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Validate that the API key is set
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    logger.warning(
        "ANTHROPIC_API_KEY is not set. The /api/analyze endpoint will fail. "
        "Copy .env.example to .env and add your key."
    )

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


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    api_key_set = bool(ANTHROPIC_API_KEY)
    return {
        "status": "ok",
        "service": "WickAI",
        "version": "1.0.0",
        "api_key_configured": api_key_set,
    }


@app.post("/api/analyze")
async def analyze_chart_endpoint(file: UploadFile = File(...)):
    """
    Analyze a candlestick chart image using Claude Vision AI.

    Accepts a multipart/form-data image upload and returns a structured
    JSON analysis with trade recommendations.
    """
    # Check API key
    if not ANTHROPIC_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="ANTHROPIC_API_KEY is not configured. Please set it in your .env file.",
        )

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
