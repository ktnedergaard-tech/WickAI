# WickAI — AI-Powered Day Trading Analysis

WickAI lets you upload a screenshot of any candlestick chart (NinjaTrader, TradingView, ThinkOrSwim, etc.) and instantly receive a detailed trade analysis with entry, stop-loss, and take-profit recommendations — powered by Claude Vision AI.

## Features

- **Drag-and-drop chart upload** — JPEG, PNG, WebP, GIF up to 10 MB
- **Claude Vision analysis** — identifies candlestick patterns, trend direction, support/resistance
- **Specific trade levels** — Entry, Stop Loss, TP1/TP2/TP3, Risk/Reward ratio
- **Confidence meter** — 1–10 scale with visual bar
- **Pattern education** — explains the psychology behind each pattern
- **Prompt caching** — system prompt cached via Anthropic's `ephemeral` cache to reduce API costs
- **Modern dark UI** — no build step required, single HTML file

## Project Structure

```
WickAI/
├── main.py              # FastAPI backend (API + static file serving)
├── analyzer.py          # Claude Vision AI analysis logic
├── patterns.py          # Candlestick pattern reference data (20 patterns)
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment variables
├── static/
│   └── index.html       # Frontend UI (single file, no build step)
└── README.md
```

## Quick Start

### 1. Install dependencies

```bash
cd /home/user/WickAI
pip install -r requirements.txt
```

### 2. Set your API key

```bash
cp .env.example .env
# Edit .env and add your Anthropic API key:
# ANTHROPIC_API_KEY=sk-ant-...
```

### 3. Run the server

```bash
python main.py
# or:
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Open the app

Visit [http://localhost:8000](http://localhost:8000) in your browser.

## API Endpoints

| Method | Path          | Description                              |
|--------|---------------|------------------------------------------|
| GET    | `/`           | Serves the frontend HTML                 |
| GET    | `/health`     | Health check (returns API key status)    |
| POST   | `/api/analyze`| Analyze a chart image (multipart/form-data, field: `file`) |

### POST /api/analyze

**Request:** `multipart/form-data` with a single `file` field containing the image.

**Response (200):**
```json
{
  "pattern_name": "Bullish Engulfing",
  "pattern_type": "bullish",
  "trend": "bullish",
  "trend_strength": "moderate",
  "support_levels": ["4,250", "4,220"],
  "resistance_levels": ["4,310", "4,340"],
  "trade_direction": "LONG",
  "entry": "near 4,285",
  "stop_loss": "4,250 - below pattern low",
  "take_profit_1": "4,310",
  "take_profit_2": "4,340",
  "take_profit_3": "4,380",
  "risk_reward_ratio": "1:2.5",
  "confidence": 8,
  "pattern_explanation": "...",
  "analysis_summary": "...",
  "risk_warning": "...",
  "timeframe_detected": "5-minute",
  "instrument_detected": "NQ"
}
```

## Supported Candlestick Patterns

WickAI's system prompt references all 20 major patterns:

| Pattern | Type | Reliability |
|---------|------|-------------|
| Doji | Neutral | 7/10 |
| Hammer | Bullish | 8/10 |
| Shooting Star | Bearish | 8/10 |
| Bullish Engulfing | Bullish | 9/10 |
| Bearish Engulfing | Bearish | 9/10 |
| Morning Star | Bullish | 9/10 |
| Evening Star | Bearish | 9/10 |
| Bullish Harami | Bullish | 6/10 |
| Bearish Harami | Bearish | 6/10 |
| Piercing Line | Bullish | 7/10 |
| Dark Cloud Cover | Bearish | 7/10 |
| Three White Soldiers | Bullish | 9/10 |
| Three Black Crows | Bearish | 9/10 |
| Hanging Man | Bearish | 7/10 |
| Inverted Hammer | Bullish | 7/10 |
| Spinning Top | Neutral | 5/10 |
| Marubozu | Bullish/Bearish | 8/10 |
| Tweezer Tops | Bearish | 7/10 |
| Tweezer Bottoms | Bullish | 7/10 |
| Three Inside Up/Down | Bullish/Bearish | 8/10 |

## Cost Optimization

The system prompt is marked with `cache_control: {type: "ephemeral"}` — after the first request, Anthropic's prompt caching will serve the system prompt from cache, significantly reducing input token costs for repeated analyses.

## Disclaimer

WickAI provides AI-generated technical analysis for **educational purposes only**. This is not financial advice. Always conduct your own due diligence, use proper risk management, and only risk capital you can afford to lose.
