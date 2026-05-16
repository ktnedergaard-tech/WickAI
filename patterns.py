"""
Candlestick pattern reference data for WickAI.
Top 20 most reliable candlestick patterns with descriptions and trade guidance.
"""

CANDLESTICK_PATTERNS = {
    "doji": {
        "name": "Doji",
        "type": "neutral",
        "reliability": 7,
        "description": (
            "A Doji forms when the opening and closing prices are virtually equal, "
            "creating a cross or plus-sign shape. It signals indecision between buyers "
            "and sellers and often precedes a reversal."
        ),
        "trade_guidance": (
            "Wait for confirmation candle. Bullish Doji at support = potential long entry. "
            "Bearish Doji at resistance = potential short entry. Stop beyond the Doji's wicks."
        ),
    },
    "hammer": {
        "name": "Hammer",
        "type": "bullish",
        "reliability": 8,
        "description": (
            "A Hammer has a small body near the top of the candle with a long lower wick "
            "(at least 2x body length) and little to no upper wick. Found at market bottoms, "
            "it shows sellers pushed price down but buyers regained control."
        ),
        "trade_guidance": (
            "Enter long on the next bullish candle close. Stop below the hammer's low. "
            "Target previous resistance or 2:1 risk/reward ratio."
        ),
    },
    "shooting_star": {
        "name": "Shooting Star",
        "type": "bearish",
        "reliability": 8,
        "description": (
            "The inverse of a hammer, a Shooting Star has a small body near the low with "
            "a long upper wick and little lower wick. Appears at market tops, indicating "
            "buyers attempted a rally but sellers drove price back down."
        ),
        "trade_guidance": (
            "Enter short on the next bearish candle close. Stop above the Shooting Star's high. "
            "Target previous support or 2:1 risk/reward ratio."
        ),
    },
    "bullish_engulfing": {
        "name": "Bullish Engulfing",
        "type": "bullish",
        "reliability": 9,
        "description": (
            "A two-candle pattern where a large bullish candle completely engulfs the prior "
            "bearish candle's body. Signals strong buying momentum overcoming selling pressure. "
            "Most powerful at significant support levels."
        ),
        "trade_guidance": (
            "Enter long at the open of the third candle or on a pullback to the engulfing "
            "candle's midpoint. Stop below the engulfing candle's low. Target 2-3x risk."
        ),
    },
    "bearish_engulfing": {
        "name": "Bearish Engulfing",
        "type": "bearish",
        "reliability": 9,
        "description": (
            "A two-candle pattern where a large bearish candle completely engulfs the prior "
            "bullish candle's body. Signals strong selling momentum overwhelming buyers. "
            "Most powerful at significant resistance levels."
        ),
        "trade_guidance": (
            "Enter short at the open of the third candle or on a bounce to the engulfing "
            "candle's midpoint. Stop above the engulfing candle's high. Target 2-3x risk."
        ),
    },
    "morning_star": {
        "name": "Morning Star",
        "type": "bullish",
        "reliability": 9,
        "description": (
            "A three-candle bullish reversal pattern: large bearish candle, small-bodied "
            "middle candle (often a Doji) gapping lower, then a large bullish candle closing "
            "above the midpoint of the first candle. Signals a bottom reversal."
        ),
        "trade_guidance": (
            "Enter long at the close of the third candle. Stop below the lowest wick of "
            "the pattern. Target previous resistance levels with 2:1+ risk/reward."
        ),
    },
    "evening_star": {
        "name": "Evening Star",
        "type": "bearish",
        "reliability": 9,
        "description": (
            "A three-candle bearish reversal pattern: large bullish candle, small-bodied "
            "middle candle gapping higher, then a large bearish candle closing below the "
            "midpoint of the first candle. Signals a top reversal."
        ),
        "trade_guidance": (
            "Enter short at the close of the third candle. Stop above the highest wick of "
            "the pattern. Target previous support levels with 2:1+ risk/reward."
        ),
    },
    "bullish_harami": {
        "name": "Bullish Harami",
        "type": "bullish",
        "reliability": 6,
        "description": (
            "A small bullish candle contained within the body of a prior large bearish candle. "
            "'Harami' means pregnant in Japanese. Indicates bearish momentum may be slowing "
            "and a potential reversal could follow."
        ),
        "trade_guidance": (
            "Wait for confirmation (third bullish candle). Enter long above the small candle's "
            "high. Stop below the large bearish candle's low. Conservative risk management."
        ),
    },
    "bearish_harami": {
        "name": "Bearish Harami",
        "type": "bearish",
        "reliability": 6,
        "description": (
            "A small bearish candle contained within the body of a prior large bullish candle. "
            "Indicates bullish momentum may be slowing. Works best at overbought conditions "
            "or key resistance levels."
        ),
        "trade_guidance": (
            "Wait for confirmation (third bearish candle). Enter short below the small candle's "
            "low. Stop above the large bullish candle's high. Use conservative position sizing."
        ),
    },
    "piercing_line": {
        "name": "Piercing Line",
        "type": "bullish",
        "reliability": 7,
        "description": (
            "A two-candle bullish reversal at market bottoms. First candle is a large bearish "
            "candle; second is a bullish candle that opens below the first candle's low but "
            "closes above its midpoint. Shows strong buying pressure."
        ),
        "trade_guidance": (
            "Enter long on the close of the second candle or early in the third candle. "
            "Stop below the second candle's low. Target resistance above with 2:1 R/R."
        ),
    },
    "dark_cloud_cover": {
        "name": "Dark Cloud Cover",
        "type": "bearish",
        "reliability": 7,
        "description": (
            "The bearish counterpart to Piercing Line. A large bullish candle followed by a "
            "bearish candle that opens above the first candle's high but closes below its "
            "midpoint. Indicates bearish reversal at tops."
        ),
        "trade_guidance": (
            "Enter short on the close of the second candle or early in the third candle. "
            "Stop above the second candle's high. Target support below with 2:1 R/R."
        ),
    },
    "three_white_soldiers": {
        "name": "Three White Soldiers",
        "type": "bullish",
        "reliability": 9,
        "description": (
            "Three consecutive long bullish candles, each closing near its high and opening "
            "within the previous candle's body. Represents sustained buying pressure and "
            "strong upward momentum. Very reliable reversal/continuation pattern."
        ),
        "trade_guidance": (
            "Enter long on a pullback after the third candle, ideally to the 50% level of "
            "the third candle. Stop below the first soldier's low. Target 2-3x the pattern height."
        ),
    },
    "three_black_crows": {
        "name": "Three Black Crows",
        "type": "bearish",
        "reliability": 9,
        "description": (
            "Three consecutive long bearish candles, each closing near its low and opening "
            "within the previous candle's body. Signals strong sustained selling pressure "
            "and bearish momentum. Opposite of Three White Soldiers."
        ),
        "trade_guidance": (
            "Enter short on a bounce after the third candle, ideally to the 50% level of "
            "the third candle. Stop above the first crow's high. Target 2-3x the pattern depth."
        ),
    },
    "hanging_man": {
        "name": "Hanging Man",
        "type": "bearish",
        "reliability": 7,
        "description": (
            "Visually identical to the Hammer but appears at the top of an uptrend. "
            "The long lower wick shows sellers temporarily took control during the session. "
            "Context matters — location at resistance increases reliability."
        ),
        "trade_guidance": (
            "Enter short on confirmation (next bearish candle). Stop above the Hanging Man's "
            "high. Stronger signal when volume is elevated. Target prior support levels."
        ),
    },
    "inverted_hammer": {
        "name": "Inverted Hammer",
        "type": "bullish",
        "reliability": 7,
        "description": (
            "Appears at the bottom of a downtrend. Has a small body near the low with a long "
            "upper wick and little lower wick. Shows buyers attempted a rally — bullish "
            "confirmation candle required to validate the reversal."
        ),
        "trade_guidance": (
            "Enter long only after bullish confirmation candle. Stop below the Inverted "
            "Hammer's low. Conservative approach — wait for two confirming candles."
        ),
    },
    "spinning_top": {
        "name": "Spinning Top",
        "type": "neutral",
        "reliability": 5,
        "description": (
            "A small-bodied candle with upper and lower wicks of roughly equal length. "
            "Indicates market indecision — neither buyers nor sellers in control. "
            "Most significant when appearing after a strong trend move."
        ),
        "trade_guidance": (
            "Do not trade in isolation. Wait for directional confirmation. "
            "At support after downtrend = potential long setup. "
            "At resistance after uptrend = potential short setup."
        ),
    },
    "marubozu": {
        "name": "Marubozu",
        "type": "bullish",
        "reliability": 8,
        "description": (
            "A full-bodied candle with no wicks (or very small wicks). A bullish Marubozu "
            "opens at the low and closes at the high, showing complete buyer dominance. "
            "A bearish Marubozu is the opposite. Signals very strong momentum."
        ),
        "trade_guidance": (
            "Trade in the direction of the Marubozu. Bullish: enter on next open, stop "
            "below the candle's low. Bearish: enter short, stop above the candle's high. "
            "High-momentum setup, be cautious of overextension."
        ),
    },
    "tweezer_tops": {
        "name": "Tweezer Tops",
        "type": "bearish",
        "reliability": 7,
        "description": (
            "Two candles with matching highs — a bullish candle followed by a bearish candle "
            "reaching the same high. Indicates strong resistance at that level with buyers "
            "unable to push through. Most effective at key resistance zones."
        ),
        "trade_guidance": (
            "Enter short after the second candle closes. Stop just above the shared high. "
            "Target next significant support level. High confidence signal at major resistance."
        ),
    },
    "tweezer_bottoms": {
        "name": "Tweezer Bottoms",
        "type": "bullish",
        "reliability": 7,
        "description": (
            "Two candles with matching lows — a bearish candle followed by a bullish candle "
            "reaching the same low. Indicates strong support at that level with sellers "
            "unable to push through. Most effective at key support zones."
        ),
        "trade_guidance": (
            "Enter long after the second candle closes. Stop just below the shared low. "
            "Target next significant resistance level. High confidence at major support."
        ),
    },
    "three_inside_up": {
        "name": "Three Inside Up",
        "type": "bullish",
        "reliability": 8,
        "description": (
            "A three-candle bullish reversal: a large bearish candle, then a smaller bullish "
            "candle contained within it (Bullish Harami), then a third bullish candle closing "
            "above the first candle's open. Provides strong confirmation of trend reversal."
        ),
        "trade_guidance": (
            "Enter long on the close of the third candle. Stop below the first candle's low. "
            "The three-candle confirmation makes this a high-confidence setup."
        ),
    },
    "three_inside_down": {
        "name": "Three Inside Down",
        "type": "bearish",
        "reliability": 8,
        "description": (
            "A three-candle bearish reversal: a large bullish candle, then a smaller bearish "
            "candle contained within it (Bearish Harami), then a third bearish candle closing "
            "below the first candle's open. Strong confirmation of a top reversal."
        ),
        "trade_guidance": (
            "Enter short on the close of the third candle. Stop above the first candle's high. "
            "The three-candle confirmation provides high-confidence short setup."
        ),
    },
}


def get_pattern_names() -> list[str]:
    """Return a list of all pattern names."""
    return [p["name"] for p in CANDLESTICK_PATTERNS.values()]


def get_pattern_by_type(pattern_type: str) -> dict:
    """Return all patterns of a given type (bullish, bearish, neutral)."""
    return {
        k: v for k, v in CANDLESTICK_PATTERNS.items()
        if v["type"] == pattern_type
    }


def get_system_prompt_patterns() -> str:
    """Generate a formatted string of patterns for the system prompt."""
    lines = []
    for key, pattern in CANDLESTICK_PATTERNS.items():
        lines.append(
            f"- {pattern['name']} ({pattern['type'].upper()}, "
            f"reliability {pattern['reliability']}/10): {pattern['description']}"
        )
    return "\n".join(lines)
