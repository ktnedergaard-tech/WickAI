"""
WickAI - Claude Vision AI Analysis Logic
Encodes chart images and sends them to Claude claude-sonnet-4-6 with vision
for detailed candlestick pattern analysis and trade recommendations.
"""

import base64
import json
import os
import random
import re
import logging
from typing import Optional

import anthropic
from patterns import get_system_prompt_patterns

logger = logging.getLogger(__name__)

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Only initialize client if key is present
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else None

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

# The comprehensive system prompt — cached via cache_control for cost savings
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
  "pattern_name": "Primary pattern name (e.g., 'Bullish Engulfing', 'Doji at Support', 'Three White Soldiers')",
  "pattern_type": "bullish | bearish | neutral",
  "trend": "bullish | bearish | neutral | ranging",
  "trend_strength": "strong | moderate | weak",
  "support_levels": ["price level or description", "..."],
  "resistance_levels": ["price level or description", "..."],
  "trade_direction": "LONG | SHORT | WAIT",
  "entry": "Specific price or range (e.g., 'near 4,285' or '4,280-4,290')",
  "stop_loss": "Specific price with brief reason (e.g., '4,250 - below pattern low')",
  "take_profit_1": "First target price",
  "take_profit_2": "Second target price",
  "take_profit_3": "Third target price (more aggressive)",
  "risk_reward_ratio": "e.g., '1:2.5'",
  "confidence": 7,
  "pattern_explanation": "Educational explanation of the pattern(s) seen (2-4 sentences explaining WHY this pattern matters and what it signals about market psychology)",
  "analysis_summary": "Overall market context and trade rationale (3-5 sentences covering trend, key levels, and why this trade makes sense)",
  "risk_warning": "Specific risk warning for this trade setup (1-2 sentences about what could invalidate this setup)",
  "timeframe_detected": "e.g., '5-minute', '1-hour', 'Daily' - or 'Unknown' if not visible",
  "instrument_detected": "e.g., 'NQ', 'ES', 'AAPL', 'BTC/USD' - or 'Unknown' if not visible"
}}

## Important Rules
- Always provide specific prices when visible on the chart
- If prices are not visible, use descriptive terms like "near recent high", "at support zone"
- Confidence scale: 1-3 (low, avoid trading), 4-6 (moderate, trade smaller), 7-8 (good setup), 9-10 (high conviction)
- If no clear pattern or the chart is unclear, set trade_direction to "WAIT"
- Never invent prices that aren't visible or inferable from the chart
- The risk_warning must be specific to the current setup, not generic
- Always respond with ONLY the JSON object, no additional text before or after
"""


def encode_image(image_bytes: bytes, media_type: str) -> str:
    """Encode image bytes to base64 string."""
    return base64.standard_b64encode(image_bytes).decode("utf-8")


def analyze_chart(image_bytes: bytes, media_type: str) -> dict:
    """
    Analyze a candlestick chart image using Claude's vision capabilities.
    Falls back to demo mode if no API key is configured.

    Args:
        image_bytes: Raw bytes of the image file
        media_type: MIME type of the image (e.g., 'image/jpeg', 'image/png')

    Returns:
        dict: Structured analysis result with trade recommendation
    """
    if not ANTHROPIC_API_KEY:
        logger.info("No API key configured — returning demo analysis")
        return random.choice(DEMO_RESPONSES)

    # Encode image to base64
    image_data = encode_image(image_bytes, media_type)

    logger.info(f"Analyzing chart image ({media_type}, {len(image_bytes)} bytes)")

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            system=[
                {
                    "type": "text",
                    "text": SYSTEM_PROMPT,
                    # Cache the system prompt to reduce API costs
                    # The system prompt is large and stable — perfect for caching
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": (
                                "Please analyze this candlestick chart and provide a detailed "
                                "trade recommendation in the specified JSON format. Identify all "
                                "visible patterns, key levels, and give specific entry, stop-loss, "
                                "and take-profit targets based on what you see in the chart."
                            ),
                        },
                    ],
                }
            ],
        )

        # Log cache usage for cost monitoring
        usage = response.usage
        logger.info(
            f"API usage - Input: {usage.input_tokens}, Output: {usage.output_tokens}, "
            f"Cache read: {getattr(usage, 'cache_read_input_tokens', 0)}, "
            f"Cache write: {getattr(usage, 'cache_creation_input_tokens', 0)}"
        )

        # Extract the text response
        response_text = ""
        for block in response.content:
            if block.type == "text":
                response_text = block.text
                break

        if not response_text:
            raise ValueError("No text response received from Claude")

        # Parse JSON from response
        analysis = parse_json_response(response_text)

        # Validate and normalize the response
        analysis = validate_and_normalize(analysis)

        return analysis

    except anthropic.BadRequestError as e:
        logger.error(f"Bad request to Claude API: {e}")
        raise ValueError(f"Image analysis failed: {str(e)}")
    except anthropic.RateLimitError:
        logger.error("Rate limit exceeded")
        raise ValueError("API rate limit reached. Please try again in a moment.")
    except anthropic.AuthenticationError:
        logger.error("Authentication failed")
        raise ValueError("API authentication failed. Please check your API key.")
    except Exception as e:
        logger.error(f"Unexpected error during analysis: {e}")
        raise ValueError(f"Analysis failed: {str(e)}")


def parse_json_response(response_text: str) -> dict:
    """
    Parse JSON from Claude's response, handling common formatting issues.

    Args:
        response_text: Raw text from Claude

    Returns:
        dict: Parsed JSON object
    """
    text = response_text.strip()

    # Try direct JSON parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try to extract JSON from markdown code blocks
    # Match ```json ... ``` or ``` ... ```
    code_block_pattern = r"```(?:json)?\s*(\{.*?\})\s*```"
    match = re.search(code_block_pattern, text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # Try to find raw JSON object in the text
    json_pattern = r"\{.*\}"
    match = re.search(json_pattern, text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    raise ValueError(
        f"Could not parse JSON from Claude's response. "
        f"Response preview: {text[:200]}..."
    )


def validate_and_normalize(analysis: dict) -> dict:
    """
    Validate the analysis response and fill in defaults for missing fields.

    Args:
        analysis: Parsed analysis dict from Claude

    Returns:
        dict: Validated and normalized analysis
    """
    # Required fields with defaults
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
        "risk_warning": "Always use proper risk management and never risk more than you can afford to lose.",
        "timeframe_detected": "Unknown",
        "instrument_detected": "Unknown",
    }

    # Apply defaults for missing fields
    for key, default_value in defaults.items():
        if key not in analysis:
            analysis[key] = default_value

    # Normalize confidence to int between 1-10
    try:
        confidence = int(analysis["confidence"])
        analysis["confidence"] = max(1, min(10, confidence))
    except (ValueError, TypeError):
        analysis["confidence"] = 5

    # Normalize pattern_type
    if analysis["pattern_type"] not in ("bullish", "bearish", "neutral"):
        analysis["pattern_type"] = "neutral"

    # Normalize trend
    valid_trends = ("bullish", "bearish", "neutral", "ranging")
    if analysis["trend"] not in valid_trends:
        analysis["trend"] = "neutral"

    # Normalize trade_direction
    if analysis["trade_direction"] not in ("LONG", "SHORT", "WAIT"):
        analysis["trade_direction"] = "WAIT"

    # Ensure lists are lists
    for list_field in ("support_levels", "resistance_levels"):
        if not isinstance(analysis[list_field], list):
            analysis[list_field] = [str(analysis[list_field])] if analysis[list_field] else []

    return analysis


def get_analysis_error_response(error_message: str) -> dict:
    """
    Return a structured error response for failed analyses.

    Args:
        error_message: The error message to include

    Returns:
        dict: Error response in the standard analysis format
    """
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
        "analysis_summary": f"Error during analysis: {error_message}",
        "risk_warning": "Always use proper risk management.",
        "timeframe_detected": "Unknown",
        "instrument_detected": "Unknown",
    }
