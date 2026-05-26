"""
WickAI - AI Chart Analysis
Supports two free vision AI providers:
  1. Groq  (GROQ_API_KEY)   — Llama 4 Vision, free at console.groq.com
  2. Gemini (GEMINI_API_KEY) — Gemini 2.0 Flash, free at aistudio.google.com
Falls back to demo mode if neither key is set.
"""

import base64
import json
import os
import random
import re
import time
import logging

from patterns import get_system_prompt_patterns
from market_intel import get_market_context, format_context_for_prompt

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY   = os.getenv("GROQ_API_KEY")

DEMO_RESPONSES = [
    {
        "pattern_name": "Bullish Engulfing",
        "pattern_type": "bullish",
        "trend": "bullish",
        "trend_strength": "strong",
        "support_levels": ["18,250", "18,100"],
        "resistance_levels": ["18,600", "18,800"],
        "trade_direction": "LONG",
        "entry": "near 18,420",
        "stop_loss": "18,200 – below engulfing candle low",
        "take_profit_1": "18,600",
        "take_profit_2": "18,750",
        "take_profit_3": "18,900",
        "risk_reward_ratio": "1:2.8",
        "confidence": 8,
        "pattern_explanation": "A Bullish Engulfing pattern forms when a large green candle completely 'engulfs' the previous red candle. This signals that buyers have overwhelmed sellers and momentum is shifting upward. It is most powerful when appearing after a downtrend or at key support.",
        "analysis_summary": "Price has been in a short-term pullback within a larger uptrend. The bullish engulfing candle at the 18,250 support zone suggests buyers are stepping in aggressively. Volume confirmation and the higher-low structure add confluence to this long setup. Risk is well-defined below the pattern low.",
        "risk_warning": "Setup is invalidated if price closes below 18,200. Watch for resistance at 18,600 – a rejection there could signal a double-top.",
        "timeframe_detected": "15-minute",
        "instrument_detected": "NQ (Nasdaq Futures)",
        "demo_mode": True,
    },
    {
        "pattern_name": "Bearish Shooting Star",
        "pattern_type": "bearish",
        "trend": "bearish",
        "trend_strength": "moderate",
        "support_levels": ["4,200", "4,150"],
        "resistance_levels": ["4,320", "4,400"],
        "trade_direction": "SHORT",
        "entry": "near 4,295",
        "stop_loss": "4,340 – above shooting star high",
        "take_profit_1": "4,240",
        "take_profit_2": "4,200",
        "take_profit_3": "4,150",
        "risk_reward_ratio": "1:2.1",
        "confidence": 7,
        "pattern_explanation": "A Shooting Star has a small body near the low and a long upper wick, showing that buyers pushed price up but sellers took control and rejected the move. It signals potential reversal when appearing after an uptrend or at resistance.",
        "analysis_summary": "Price rallied into the 4,320 resistance zone and printed a shooting star, indicating strong selling pressure at this level. The upper wick rejection combined with the prior resistance makes this a high-probability short setup. The trend structure shows lower highs forming.",
        "risk_warning": "A close above 4,340 invalidates the pattern. If broader market sentiment turns bullish, resistance could break — wait for confirmation before entering.",
        "timeframe_detected": "1-hour",
        "instrument_detected": "ES (S&P 500 Futures)",
        "demo_mode": True,
    },
    {
        "pattern_name": "Doji at Support",
        "pattern_type": "neutral",
        "trend": "ranging",
        "trend_strength": "weak",
        "support_levels": ["42,800", "42,500"],
        "resistance_levels": ["43,500", "44,000"],
        "trade_direction": "WAIT",
        "entry": "Wait for confirmation candle",
        "stop_loss": "Define after direction confirmed",
        "take_profit_1": "43,500 if long",
        "take_profit_2": "44,000 if long",
        "take_profit_3": "42,500 if short",
        "risk_reward_ratio": "TBD",
        "confidence": 5,
        "pattern_explanation": "A Doji forms when open and close are nearly equal, creating a cross shape. It signals indecision between buyers and sellers. At support it can precede a bullish reversal, but confirmation is required before trading.",
        "analysis_summary": "Price is consolidating at a key support level with a doji candle showing indecision. The market is in a ranging phase with no clear directional bias. Wait for the next candle to confirm direction before committing to a trade.",
        "risk_warning": "Do not trade the doji alone — wait for a strong follow-through candle. A break below 42,500 support could trigger a sharper move down.",
        "timeframe_detected": "4-hour",
        "instrument_detected": "BTC/USD",
        "demo_mode": True,
    },
]

SYSTEM_PROMPT = f"""You are WickAI, an expert day trading analyst specializing in candlestick chart analysis. You have deep knowledge of technical analysis, price action, and candlestick patterns. Your role is to analyze trading chart screenshots and provide specific, actionable trade recommendations.

## Your Expertise
You are trained on the following candlestick patterns and more:

{get_system_prompt_patterns()}

## Analysis Framework
When analyzing a chart, you must:
1. Identify all visible candlestick patterns
2. Determine the current trend (bullish/bearish/neutral/ranging)
3. Identify key support and resistance levels from the visible price history
4. Assess market structure (higher highs/lows for uptrend, lower highs/lows for downtrend)
5. Consider volume if visible
6. Look for confluence of signals before recommending a trade

## Response Format
You MUST respond with a valid JSON object (no markdown fences, no extra text — pure JSON only) with this exact structure:

{{
  "pattern_name": "Primary pattern name",
  "pattern_type": "bullish | bearish | neutral",
  "trend": "bullish | bearish | neutral | ranging",
  "trend_strength": "strong | moderate | weak",
  "support_levels": ["price level or description"],
  "resistance_levels": ["price level or description"],
  "trade_direction": "LONG | SHORT | WAIT",
  "entry": "Specific price or range",
  "stop_loss": "Specific price with brief reason",
  "take_profit_1": "First target price",
  "take_profit_2": "Second target price",
  "take_profit_3": "Third target price (more aggressive)",
  "risk_reward_ratio": "e.g. '1:2.5'",
  "confidence": 7,
  "pattern_explanation": "2-4 sentences explaining WHY this pattern matters",
  "analysis_summary": "3-5 sentences covering trend, key levels, and trade rationale",
  "risk_warning": "1-2 sentences about what could invalidate this setup",
  "timeframe_detected": "e.g. '15-minute' or 'Unknown'",
  "instrument_detected": "e.g. 'NQ' or 'Unknown'"
}}

## Important Rules
- Always provide specific prices when visible on the chart
- Confidence scale: 1-3 (avoid), 4-6 (moderate), 7-8 (good), 9-10 (high conviction)
- If no clear pattern, set trade_direction to "WAIT"
- Never invent prices not visible in the chart
- Respond with ONLY the JSON object, no extra text
"""


def analyze_chart(image_bytes: bytes, media_type: str) -> dict:
    """
    Analyse a chart image.
    Priority: Groq (free) → Gemini (free) → demo mode.
    """
    market_ctx    = get_market_context()
    context_block = format_context_for_prompt(market_ctx)
    enriched_prompt = SYSTEM_PROMPT + "\n\n" + context_block

    def attach_ctx(result: dict) -> dict:
        result["market_context"] = {
            "session":    market_ctx["session"],
            "day":        market_ctx["day"],
            "fear_greed": market_ctx.get("fear_greed"),
        }
        return result

    if GROQ_API_KEY:
        return attach_ctx(_analyze_groq(image_bytes, media_type, enriched_prompt))

    if GEMINI_API_KEY:
        return attach_ctx(_analyze_gemini(image_bytes, media_type, enriched_prompt))

    logger.info("No API key set — returning demo analysis")
    return random.choice(DEMO_RESPONSES)


def _analyze_groq(image_bytes: bytes, media_type: str, prompt: str) -> dict:
    """Call Groq Llama Vision (free tier at console.groq.com)."""
    from groq import Groq
    client = Groq(api_key=GROQ_API_KEY)
    b64 = base64.b64encode(image_bytes).decode("utf-8")

    for attempt in range(3):
        try:
            resp = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": [
                        {"type": "text",
                         "text": "Analyse this candlestick chart and return the JSON trade recommendation."},
                        {"type": "image_url",
                         "image_url": {"url": f"data:{media_type};base64,{b64}"}},
                    ]},
                ],
                temperature=0.2,
                max_tokens=1024,
            )
            text = resp.choices[0].message.content.strip()
            logger.info(f"Groq response received ({len(text)} chars)")
            return validate_and_normalize(parse_json_response(text))

        except Exception as e:
            err_str = str(e)
            if "429" in err_str or "rate_limit" in err_str.lower():
                delay = 30
                logger.warning(f"Groq rate limited (attempt {attempt+1}/3). Waiting {delay}s…")
                if attempt < 2:
                    time.sleep(delay)
                    continue
                raise ValueError(
                    f"RATE_LIMIT:{delay}:Groq free tier quota reached. "
                    "Please wait a moment and try again."
                )
            logger.error(f"Groq error: {e}")
            raise ValueError(f"Analysis failed: {e}")

    raise ValueError("Groq analysis failed after retries")


def _analyze_gemini(image_bytes: bytes, media_type: str, prompt: str) -> dict:
    """Call Google Gemini 2.0 Flash (free tier at aistudio.google.com)."""
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=prompt,
    )
    image_part = {
        "mime_type": media_type,
        "data": base64.b64encode(image_bytes).decode("utf-8"),
    }

    for attempt in range(3):
        try:
            response = model.generate_content([
                image_part,
                "Analyse this candlestick chart and return the JSON trade recommendation.",
            ])
            text = response.text.strip()
            logger.info(f"Gemini response received ({len(text)} chars)")
            return validate_and_normalize(parse_json_response(text))

        except Exception as e:
            err_str = str(e)
            if "429" in err_str:
                match = re.search(r"seconds:\s*(\d+)", err_str)
                delay = min(int(match.group(1)) if match else 60, 65)
                logger.warning(f"Gemini rate limited (attempt {attempt+1}/3). Waiting {delay}s…")
                if attempt < 2:
                    time.sleep(delay)
                    continue
                raise ValueError(
                    f"RATE_LIMIT:{delay}:Gemini free tier quota reached. "
                    "Please wait about a minute and try again."
                )
            logger.error(f"Gemini error: {e}")
            raise ValueError(f"Analysis failed: {e}")

    raise ValueError("Gemini analysis failed after retries")


def parse_json_response(text: str) -> dict:
    """Parse JSON from AI response, handling markdown fences."""
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    raise ValueError(f"Could not parse JSON from AI response: {text[:200]}")


def validate_and_normalize(analysis: dict) -> dict:
    """Fill in defaults for missing fields and normalise values."""
    defaults = {
        "pattern_name": "Unidentified Pattern",
        "pattern_type": "neutral",
        "trend": "neutral",
        "trend_strength": "moderate",
        "support_levels": [],
        "resistance_levels": [],
        "trade_direction": "WAIT",
        "entry": "No clear entry",
        "stop_loss": "Define based on pattern",
        "take_profit_1": "Define based on resistance",
        "take_profit_2": "Define based on resistance",
        "take_profit_3": "Define based on resistance",
        "risk_reward_ratio": "N/A",
        "confidence": 5,
        "pattern_explanation": "Pattern analysis not available.",
        "analysis_summary": "Chart analysis completed.",
        "risk_warning": "Always use proper risk management.",
        "timeframe_detected": "Unknown",
        "instrument_detected": "Unknown",
    }
    for key, val in defaults.items():
        if key not in analysis:
            analysis[key] = val
    try:
        analysis["confidence"] = max(1, min(10, int(analysis["confidence"])))
    except (ValueError, TypeError):
        analysis["confidence"] = 5
    if analysis["pattern_type"] not in ("bullish", "bearish", "neutral"):
        analysis["pattern_type"] = "neutral"
    if analysis["trend"] not in ("bullish", "bearish", "neutral", "ranging"):
        analysis["trend"] = "neutral"
    if analysis["trade_direction"] not in ("LONG", "SHORT", "WAIT"):
        analysis["trade_direction"] = "WAIT"
    for field in ("support_levels", "resistance_levels"):
        if not isinstance(analysis[field], list):
            analysis[field] = [str(analysis[field])] if analysis[field] else []
    return analysis


def get_analysis_error_response(error_message: str) -> dict:
    """Return a structured error response."""
    return {
        "error": True,
        "error_message": error_message,
        "pattern_name": "Analysis Failed",
        "pattern_type": "neutral",
        "trend": "neutral",
        "trend_strength": "weak",
        "support_levels": [],
        "resistance_levels": [],
        "trade_direction": "WAIT",
        "entry": "N/A",
        "stop_loss": "N/A",
        "take_profit_1": "N/A",
        "take_profit_2": "N/A",
        "take_profit_3": "N/A",
        "risk_reward_ratio": "N/A",
        "confidence": 0,
        "pattern_explanation": "Analysis could not be completed.",
        "analysis_summary": f"Error: {error_message}",
        "risk_warning": "Always use proper risk management.",
        "timeframe_detected": "Unknown",
        "instrument_detected": "Unknown",
    }
