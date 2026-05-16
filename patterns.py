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

    # ── 35 additional patterns scraped from trading education sources ──

    "abandoned_baby_bullish": {
        "name": "Abandoned Baby (Bullish)",
        "type": "bullish",
        "reliability": 9,
        "description": (
            "A rare three-candle bullish reversal: a strong bearish candle, followed by a Doji "
            "that gaps completely below it (no shadow overlap), then a strong bullish candle that "
            "gaps up above the Doji. The isolation of the Doji on both sides signals complete "
            "indecision at a price island before buyers surge back. More reliable than Morning Star "
            "because the full gap requirements are far stricter."
        ),
        "trade_guidance": (
            "Enter long at the close of the third bullish candle. Stop-loss just below the Doji's "
            "low. Target the prior swing high or use a 2:1 reward-to-risk ratio."
        ),
    },

    "abandoned_baby_bearish": {
        "name": "Abandoned Baby (Bearish)",
        "type": "bearish",
        "reliability": 9,
        "description": (
            "A rare three-candle bearish reversal: a strong bullish candle, followed by a Doji "
            "that gaps completely above it (no shadow overlap), then a strong bearish candle that "
            "gaps down below the Doji. The gapped-out Doji signals a sudden and decisive rejection "
            "of higher prices. One of the most reliable bearish reversal signals in candlestick analysis."
        ),
        "trade_guidance": (
            "Enter short at the close of the third bearish candle. Stop-loss just above the Doji's "
            "high. Target the prior swing low or a 2:1 risk-reward minimum."
        ),
    },

    "belt_hold_bullish": {
        "name": "Belt Hold (Bullish)",
        "type": "bullish",
        "reliability": 6,
        "description": (
            "A single long bullish candle that opens at or very near its low (no lower shadow) "
            "and closes near its high, appearing in a downtrend. The candle 'holds' sellers from "
            "pushing price lower and signals a possible reversal. Success rate is approximately "
            "71% for bullish reversals when confirmed with volume."
        ),
        "trade_guidance": (
            "Enter long at the close or on the next candle's open. Stop-loss just below the "
            "candle's low. Seek confirmation from a follow-through bullish candle with above-average volume."
        ),
    },

    "belt_hold_bearish": {
        "name": "Belt Hold (Bearish)",
        "type": "bearish",
        "reliability": 6,
        "description": (
            "A single long bearish candle that opens at or very near its high (no upper shadow) "
            "and closes near its low, appearing in an uptrend. The inability of buyers to push "
            "price higher signals potential reversal. Works best at key resistance after an extended rally."
        ),
        "trade_guidance": (
            "Enter short at the close or on the next candle's open. Stop-loss just above the "
            "candle's high. Look for confirmation with a subsequent bearish candle and elevated volume."
        ),
    },

    "breakaway_bullish": {
        "name": "Breakaway (Bullish)",
        "type": "bullish",
        "reliability": 7,
        "description": (
            "A five-candle bullish reversal: a long bearish candle gaps down, followed by two to "
            "three smaller candles continuing the decline, ending with a strong bullish candle that "
            "closes back into the gap. Signals that selling momentum is exhausted and buyers are "
            "reclaiming control."
        ),
        "trade_guidance": (
            "Enter long when the fifth bullish candle closes, or confirm with a break above its "
            "high. Stop-loss at the pattern's lowest point. Target the starting level of the pattern."
        ),
    },

    "breakaway_bearish": {
        "name": "Breakaway (Bearish)",
        "type": "bearish",
        "reliability": 7,
        "description": (
            "A five-candle bearish reversal: a long bullish candle gaps up, followed by two to "
            "three smaller bullish candles with weakening momentum, then a large bearish candle "
            "that closes back inside the gap. Signals that the uptrend is losing steam and bears "
            "are retaking control."
        ),
        "trade_guidance": (
            "Enter short at the close of the fifth bearish candle. Stop-loss just above the "
            "pattern's highest high. Target the base of the gap or prior swing low."
        ),
    },

    "concealing_baby_swallow": {
        "name": "Concealing Baby Swallow",
        "type": "bullish",
        "reliability": 7,
        "description": (
            "A rare four-candle bullish reversal in a downtrend. Two bearish Marubozus are "
            "followed by a third candle that gaps down but has an upper shadow penetrating the "
            "second candle's body. The fourth candle completely engulfs the third including its "
            "shadow — signalling sellers have overextended and a reversal is imminent."
        ),
        "trade_guidance": (
            "Enter long at the open of the candle following the fourth engulfing candle. "
            "Stop-loss below the lowest low of the pattern. Seek volume confirmation on the fifth candle."
        ),
    },

    "counterattack_lines_bullish": {
        "name": "Counterattack Lines (Bullish)",
        "type": "bullish",
        "reliability": 6,
        "description": (
            "A two-candle bullish reversal in a downtrend: a large bearish candle is followed by "
            "a bullish candle that gaps down sharply on the open but rallies to close at exactly "
            "the same price as the prior candle's close. This stalemate at the same price level "
            "often precedes a reversal."
        ),
        "trade_guidance": (
            "Enter long above the close of the second bullish candle, confirmed by a third bullish "
            "candle. Stop-loss below the low of the second candle. Works best at known support zones."
        ),
    },

    "counterattack_lines_bearish": {
        "name": "Counterattack Lines (Bearish)",
        "type": "bearish",
        "reliability": 6,
        "description": (
            "A two-candle bearish reversal in an uptrend: a large bullish candle is followed by a "
            "bearish candle that gaps up on the open but reverses to close at the same price as "
            "the prior candle's close. Bulls and bears reach parity at a key price, signaling "
            "potential reversal."
        ),
        "trade_guidance": (
            "Enter short below the close of the second bearish candle, confirmed by a third bearish "
            "candle. Stop-loss above the high of the second candle. Most effective at established resistance."
        ),
    },

    "deliberation": {
        "name": "Deliberation",
        "type": "bearish",
        "reliability": 5,
        "description": (
            "A three-candle bearish reversal in an uptrend: two large bullish bodies advance "
            "strongly, but the third candle is significantly smaller and may gap up slightly, "
            "indicating that bulls are losing conviction. The 'deliberation' signals hesitation "
            "at the top before a potential reversal."
        ),
        "trade_guidance": (
            "Wait for a fourth bearish confirmation candle closing below the third candle before "
            "entering short. Stop-loss above the high of the third candle. Works best near strong resistance."
        ),
    },

    "dragonfly_doji": {
        "name": "Dragonfly Doji",
        "type": "bullish",
        "reliability": 7,
        "description": (
            "Open, high, and close are at or near the same level with a long lower shadow. "
            "Sellers drove price down sharply but buyers completely reversed the move, closing "
            "near the open. Most significant at the end of a downtrend near support."
        ),
        "trade_guidance": (
            "Enter long above the high of the Dragonfly Doji on the next candle. Stop-loss "
            "below the long lower shadow's low. Best used at key support zones with RSI oversold."
        ),
    },

    "gravestone_doji": {
        "name": "Gravestone Doji",
        "type": "bearish",
        "reliability": 7,
        "description": (
            "Open, low, and close are at or near the same level with a long upper shadow. "
            "Bulls drove price sharply higher but sellers completely reversed it, closing back "
            "at the open. The long upper wick is a powerful rejection signal at resistance zones."
        ),
        "trade_guidance": (
            "Enter short below the low of the Gravestone Doji on the subsequent candle. "
            "Stop-loss above the long upper shadow's high. Combine with RSI overbought or key resistance."
        ),
    },

    "long_legged_doji": {
        "name": "Long-Legged Doji",
        "type": "neutral",
        "reliability": 5,
        "description": (
            "A Doji with exceptionally long upper and lower shadows with open/close near the "
            "middle. Represents extreme indecision — both bulls and bears battled aggressively "
            "but neither won decisively. Direction depends on prior trend and subsequent candle."
        ),
        "trade_guidance": (
            "Do not trade in isolation. Wait for the next candle to break either the high or "
            "low of the pattern. Stop-loss on the opposite extreme. Best at key inflection points."
        ),
    },

    "morning_doji_star": {
        "name": "Morning Doji Star",
        "type": "bullish",
        "reliability": 8,
        "description": (
            "A three-candle bullish reversal: a large bearish candle, followed by a Doji that "
            "gaps below it, then a strong bullish candle that closes above the midpoint of the "
            "first candle. The Doji as the middle candle makes this stronger than the standard "
            "Morning Star — it represents perfect equilibrium before buyers take over."
        ),
        "trade_guidance": (
            "Enter long at the close of the third bullish candle. Stop-loss below the Doji's "
            "low. A gap between the Doji and third candle increases reliability. Target the start "
            "of the preceding downtrend."
        ),
    },

    "evening_doji_star": {
        "name": "Evening Doji Star",
        "type": "bearish",
        "reliability": 8,
        "description": (
            "A three-candle bearish reversal: a large bullish candle, followed by a Doji that "
            "gaps above it, then a strong bearish candle closing below the midpoint of the first "
            "candle. The Doji as the central indecision candle makes this stronger than a standard "
            "Evening Star — buyers have completely stalled before sellers dominate."
        ),
        "trade_guidance": (
            "Enter short at the close of the third bearish candle. Stop-loss above the Doji's "
            "high. Target the base of the prior uptrend. Confirm with high volume on the third candle."
        ),
    },

    "identical_three_crows": {
        "name": "Identical Three Crows",
        "type": "bearish",
        "reliability": 8,
        "description": (
            "A three-candle bearish reversal where each successive bearish candle opens exactly "
            "at the prior candle's close (not just within the body). This precision signals "
            "orderly, relentless institutional distribution and is confirmed at 79-87% across "
            "backtests — stronger than standard Three Black Crows."
        ),
        "trade_guidance": (
            "Enter short at the close of the third candle. Stop-loss above the high of the first "
            "candle. Target the next major support level. Confirm with increasing volume across all three."
        ),
    },

    "kicking_bullish": {
        "name": "Kicking (Bullish)",
        "type": "bullish",
        "reliability": 9,
        "description": (
            "One of the most powerful bullish signals: a strong bearish Marubozu is followed by "
            "a gap up and a strong bullish Marubozu. The complete gap with no shadow overlap and "
            "strength of both candles signals an explosive shift in sentiment, often driven by "
            "a major catalyst or institutional order flow."
        ),
        "trade_guidance": (
            "Enter long at the open of the second bullish candle or at its close for conservative "
            "entry. Stop-loss below the low of the second candle — the gap should not be filled. "
            "Target a measured move equal to the height of the pattern projected upward."
        ),
    },

    "kicking_bearish": {
        "name": "Kicking (Bearish)",
        "type": "bearish",
        "reliability": 9,
        "description": (
            "One of the most powerful bearish signals: a strong bullish Marubozu is followed by "
            "a complete gap down and a strong bearish Marubozu. Both candles have no shadows and "
            "the gap reflects a violent shift from bullish to bearish sentiment. Considered among "
            "the most reliable of all reversal signals."
        ),
        "trade_guidance": (
            "Enter short at the open of the second bearish candle or at its close. Stop-loss "
            "above the high of the second candle — the gap should hold as resistance. Target a "
            "measured move equal to the pattern's height projected downward."
        ),
    },

    "ladder_bottom": {
        "name": "Ladder Bottom",
        "type": "bullish",
        "reliability": 7,
        "description": (
            "A five-candle bullish reversal at the end of a downtrend. Three consecutive bearish "
            "candles create descending lows like a ladder, followed by a fourth bearish candle "
            "with a long upper shadow indicating waning selling pressure, and a fifth strong "
            "bullish candle confirming the reversal."
        ),
        "trade_guidance": (
            "Enter long at the close of the fifth bullish candle or on break above the fourth "
            "candle's upper shadow high. Stop-loss below the lowest low of the pattern. Target "
            "the origin of the three-candle decline."
        ),
    },

    "mat_hold": {
        "name": "Mat Hold",
        "type": "bullish",
        "reliability": 7,
        "description": (
            "A five-candle bullish continuation: a large bullish candle gaps up, followed by "
            "three small bearish/mixed candles that pull back but stay within the first candle's "
            "range, then a fifth strong bullish candle closing above all prior highs. The "
            "pullback acts as brief consolidation before the trend resumes."
        ),
        "trade_guidance": (
            "Enter long at the close of the fifth bullish candle. Stop-loss below the low of "
            "the correction candles. Trend-continuation trade; target the next resistance level."
        ),
    },

    "rising_three_methods": {
        "name": "Rising Three Methods",
        "type": "bullish",
        "reliability": 7,
        "description": (
            "A five-candle bullish continuation: a large bullish candle is followed by three "
            "small bearish candles that stay within its range, then a fifth large bullish candle "
            "closing above the first candle's high. The three corrective candles represent a "
            "controlled pullback before bulls reassert control."
        ),
        "trade_guidance": (
            "Enter long at the close of the fifth bullish candle. Stop-loss below the lowest "
            "low of the three corrective candles. Target the next resistance zone or a 1.5-2x "
            "move of the first candle's range."
        ),
    },

    "falling_three_methods": {
        "name": "Falling Three Methods",
        "type": "bearish",
        "reliability": 7,
        "description": (
            "A five-candle bearish continuation: a large bearish candle is followed by three "
            "small bullish candles staying within its range, then a fifth large bearish candle "
            "closing below the first candle's low. The three bullish candles are a weak "
            "counter-rally before bears push prices to new lows."
        ),
        "trade_guidance": (
            "Enter short at the close of the fifth bearish candle. Stop-loss above the highest "
            "high of the three corrective candles. Target the next support level or a measured "
            "move equal to the first candle's range."
        ),
    },

    "separating_lines_bullish": {
        "name": "Separating Lines (Bullish)",
        "type": "bullish",
        "reliability": 6,
        "description": (
            "A two-candle bullish continuation in an uptrend: a bearish pullback candle is "
            "followed by a bullish candle that opens at exactly the same price as the bearish "
            "candle's open and closes higher. Both candles share the same opening price but "
            "move in opposite directions, confirming the bullish trend is intact."
        ),
        "trade_guidance": (
            "Enter long at the close of the second bullish candle. Stop-loss below the low of "
            "the first bearish candle. Best used in strong trending markets with moving average confirmation."
        ),
    },

    "separating_lines_bearish": {
        "name": "Separating Lines (Bearish)",
        "type": "bearish",
        "reliability": 6,
        "description": (
            "A two-candle bearish continuation in a downtrend: a bullish counter-rally candle "
            "is followed by a bearish candle that opens at exactly the same price as the bullish "
            "candle's open and closes lower. Both candles share the same opening but diverge — "
            "confirming bearish trend continuation."
        ),
        "trade_guidance": (
            "Enter short at the close of the second bearish candle. Stop-loss above the high "
            "of the first bullish candle. Most reliable in strong downtrends with declining moving average."
        ),
    },

    "side_by_side_white_lines_bullish": {
        "name": "Side-by-Side White Lines (Bullish)",
        "type": "bullish",
        "reliability": 6,
        "description": (
            "A three-candle bullish continuation: a strong bullish candle gaps up, followed by "
            "two similar-sized bullish candles opening and closing at roughly the same levels "
            "(side-by-side). The pair of bullish candles above the gap confirms buyers are "
            "holding the gap open and the uptrend will continue."
        ),
        "trade_guidance": (
            "Enter long above the high of the third candle. Stop-loss below the gap between "
            "the first and second candles — a filled gap invalidates the pattern."
        ),
    },

    "side_by_side_white_lines_bearish": {
        "name": "Side-by-Side White Lines (Bearish)",
        "type": "bearish",
        "reliability": 5,
        "description": (
            "A three-candle bearish continuation: a large bearish candle gaps down, followed by "
            "two similar bullish candles that open and close near the same levels but fail to "
            "close the downside gap. Despite two white candles, their inability to fill the gap "
            "confirms continued bearish control."
        ),
        "trade_guidance": (
            "Enter short below the low of the third candle, confirming gap resistance holds. "
            "Stop-loss above the gap. Use volume analysis to confirm — the two bullish candles can be a bear trap."
        ),
    },

    "stick_sandwich": {
        "name": "Stick Sandwich",
        "type": "bullish",
        "reliability": 6,
        "description": (
            "A three-candle bullish reversal: a bearish candle is followed by a bullish candle "
            "that closes above it, then a third bearish candle that closes at exactly the same "
            "price as the first. The two outer bearish candles create a visible support level "
            "at their shared closing price, signaling strong demand at that level."
        ),
        "trade_guidance": (
            "Enter long above the high of the third candle on a subsequent bullish bar. "
            "Stop-loss below the shared closing price of the two bearish candles. Target the prior swing high."
        ),
    },

    "tasuki_gap_upside": {
        "name": "Tasuki Gap (Upside)",
        "type": "bullish",
        "reliability": 7,
        "description": (
            "A three-candle bullish continuation: two bullish candles separated by an upside gap "
            "are followed by a bearish candle that partially fills the gap but does not close it. "
            "The inability of sellers to fully close the gap confirms bullish continuation."
        ),
        "trade_guidance": (
            "Enter long when price resumes moving up after the third candle, or at the top of "
            "the gap as support. Stop-loss below the bottom of the gap — a filled gap invalidates the signal."
        ),
    },

    "tasuki_gap_downside": {
        "name": "Tasuki Gap (Downside)",
        "type": "bearish",
        "reliability": 7,
        "description": (
            "A three-candle bearish continuation: two bearish candles separated by a downside gap "
            "are followed by a bullish candle that partially fills the gap but cannot close it. "
            "The failure of buyers to reclaim the full gap level confirms sellers remain dominant."
        ),
        "trade_guidance": (
            "Enter short when price resumes declining after the third candle fails to fill the gap. "
            "Stop-loss above the top of the gap. Target the next support level."
        ),
    },

    "three_outside_up": {
        "name": "Three Outside Up",
        "type": "bullish",
        "reliability": 7,
        "description": (
            "A three-candle bullish reversal extending the Bullish Engulfing: a small bearish "
            "candle is followed by a larger bullish candle that fully engulfs it, then a third "
            "bullish candle that closes even higher. The third candle is the confirmation that "
            "raises reliability above a standard Bullish Engulfing."
        ),
        "trade_guidance": (
            "Enter long at the close of the third bullish candle. Stop-loss below the low of "
            "the second (engulfing) candle. Target the prior swing high or a 2:1 risk-reward ratio."
        ),
    },

    "three_outside_down": {
        "name": "Three Outside Down",
        "type": "bearish",
        "reliability": 7,
        "description": (
            "A three-candle bearish reversal extending the Bearish Engulfing: a small bullish "
            "candle is followed by a larger bearish candle that fully engulfs it, then a third "
            "bearish candle closing even lower. The third candle confirms sellers have taken "
            "definitive control."
        ),
        "trade_guidance": (
            "Enter short at the close of the third bearish candle. Stop-loss above the high of "
            "the second (engulfing) candle. Target the prior swing low. Best used at resistance "
            "zones after extended rallies."
        ),
    },

    "three_stars_south": {
        "name": "Three Stars in the South",
        "type": "bullish",
        "reliability": 7,
        "description": (
            "A rare three-candle bullish reversal: a long bearish candle with a long lower shadow, "
            "followed by a smaller bearish candle with a higher low and shorter lower shadow, then "
            "a small bearish Marubozu that fits entirely within the second candle's range. Each "
            "candle shows progressively diminishing bearish power."
        ),
        "trade_guidance": (
            "Enter long above the high of the third candle on the next bullish confirmation bar. "
            "Stop-loss below the lowest low of the pattern. Seek RSI or support-zone confluence due to rarity."
        ),
    },

    "tri_star_bullish": {
        "name": "Tri-Star (Bullish)",
        "type": "bullish",
        "reliability": 6,
        "description": (
            "Three consecutive Doji candles at the end of a downtrend, with the middle Doji "
            "gapping below the other two. Three consecutive Dojis signal extreme and prolonged "
            "indecision that historically precedes a directional resolution — often to the upside "
            "after a sustained decline. Very rare."
        ),
        "trade_guidance": (
            "Enter long above the high of the third Doji only after a fourth bullish confirmation "
            "candle. Stop-loss below the lowest low of the three Doji candles. Never trade without confirmation."
        ),
    },

    "tri_star_bearish": {
        "name": "Tri-Star (Bearish)",
        "type": "bearish",
        "reliability": 6,
        "description": (
            "Three consecutive Doji candles at the end of an uptrend, with the middle Doji "
            "gapping above the other two. The three Dojis signal extreme buyer exhaustion at "
            "a market top. Rare but meaningful when paired with overbought indicators or key resistance."
        ),
        "trade_guidance": (
            "Enter short below the low of the third Doji only after a fourth bearish confirmation "
            "candle. Stop-loss above the highest high of the three Doji candles. Always pair with "
            "overbought RSI or resistance confluence."
        ),
    },

    "two_crows": {
        "name": "Two Crows",
        "type": "bearish",
        "reliability": 6,
        "description": (
            "A three-candle bearish reversal in an uptrend: a large bullish candle is followed "
            "by a bearish candle that gaps up, then a third bearish candle that opens within the "
            "second candle's body and closes within the first candle's body. The progressive "
            "invasion of the first bullish candle's territory signals bears gaining ground."
        ),
        "trade_guidance": (
            "Enter short on a break below the first bullish candle's close after the pattern "
            "completes. Stop-loss above the gap high. Confirm with a bearish fourth candle or "
            "volume increase. Best used at resistance levels."
        ),
    },

    "unique_three_river": {
        "name": "Unique Three River Bottom",
        "type": "bullish",
        "reliability": 5,
        "description": (
            "A rare three-candle pattern in a downtrend: a large bearish candle, followed by a "
            "smaller bearish candle with a long lower shadow making a new low, then a small "
            "bullish candle closing above the second candle's close. Note: backtests show it acts "
            "as bearish continuation ~60% of the time — strong confirmation is essential."
        ),
        "trade_guidance": (
            "Enter long only with a strong bullish fourth candle above the third candle's high. "
            "Stop-loss below the second candle's low (extreme wick). Use only near well-defined "
            "support or oversold RSI zones. Reduce position size due to lower reliability."
        ),
    },

    "upside_gap_two_crows": {
        "name": "Upside Gap Two Crows",
        "type": "bearish",
        "reliability": 7,
        "description": (
            "A three-candle bearish reversal: a strong bullish candle is followed by a small "
            "bearish candle that gaps up (first 'crow'), then a second larger bearish candle "
            "that opens above the first bearish candle but closes within the body of the original "
            "bullish candle. The two consecutive bearish candles signal building selling pressure."
        ),
        "trade_guidance": (
            "Enter short after the third candle closes, especially if it closes below the midpoint "
            "of the first bullish candle. Stop-loss above the high of the second candle (the gap). "
            "Target the base of the initial bullish candle."
        ),
    },

    "advance_block": {
        "name": "Advance Block",
        "type": "bearish",
        "reliability": 5,
        "description": (
            "A three-candle bearish reversal in an uptrend: three consecutive bullish candles "
            "where each has a progressively smaller real body and increasingly long upper shadows. "
            "The shrinking bodies and growing upper wicks show buyers losing momentum while sellers "
            "push back. More reliable on higher timeframes."
        ),
        "trade_guidance": (
            "Wait for a bearish confirmation candle below the third candle's low before entering "
            "short. Stop-loss above the high of the third candle. Reversal rate is only ~36% — "
            "always combine with an overbought oscillator or resistance level."
        ),
    },

    "rising_window": {
        "name": "Rising Window",
        "type": "bullish",
        "reliability": 7,
        "description": (
            "A two-candle bullish continuation (also called a Bullish Gap) where the low of the "
            "second candle is higher than the high of the first, creating an unfilled gap — the "
            "'window'. Japanese candlestick theory holds that price continues trending upward "
            "until the window is closed. The gap acts as support on any retest."
        ),
        "trade_guidance": (
            "Enter long on a pullback to the top of the gap, which acts as support. Stop-loss "
            "below the bottom of the gap — a filled gap invalidates the signal. Target the next resistance."
        ),
    },

    "falling_window": {
        "name": "Falling Window",
        "type": "bearish",
        "reliability": 7,
        "description": (
            "A two-candle bearish continuation (also called a Bearish Gap) where the high of the "
            "second candle is lower than the low of the first, creating an unfilled downside gap. "
            "The gap acts as resistance on any retest and price is expected to continue lower "
            "until the window is closed."
        ),
        "trade_guidance": (
            "Enter short on a pullback up to the bottom of the gap, which acts as resistance. "
            "Stop-loss above the top of the gap. Target the next support level."
        ),
    },

    "homing_pigeon": {
        "name": "Homing Pigeon",
        "type": "bullish",
        "reliability": 5,
        "description": (
            "A two-candle bullish reversal similar to the Bullish Harami: a large bearish candle "
            "followed by a smaller bearish candle whose body is entirely within the first candle's "
            "range. Unlike the Harami, both candles are bearish. The smaller inner candle shows "
            "contracting selling pressure. Note: acts as bearish continuation 56% of the time."
        ),
        "trade_guidance": (
            "Wait for a third bullish candle closing above the first candle's high before entering "
            "long. Stop-loss below the low of the first large bearish candle. Only trade at defined "
            "support levels with RSI confirmation."
        ),
    },

    "matching_low": {
        "name": "Matching Low",
        "type": "bullish",
        "reliability": 6,
        "description": (
            "A two-candle bullish reversal where two consecutive bearish candles close at virtually "
            "the same price level, creating a clearly defined support zone. The identical closing "
            "prices signal that sellers have been unable to push price lower on two separate "
            "attempts, indicating strong underlying demand at that price."
        ),
        "trade_guidance": (
            "Enter long above the high of the second candle on a confirming bullish bar. "
            "Stop-loss just below the shared closing price (the matching low support level). "
            "Target the prior swing high."
        ),
    },

    "on_neck": {
        "name": "On Neck",
        "type": "bearish",
        "reliability": 5,
        "description": (
            "A two-candle bearish continuation in a downtrend: a large bearish candle is followed "
            "by a small bullish candle that opens below the first candle's low but closes at or "
            "near the first candle's closing price. The failure of the bullish candle to recover "
            "meaningful ground signals bears remain in control."
        ),
        "trade_guidance": (
            "Enter short on a break below the low of the second candle. Stop-loss above the high "
            "of the second candle. Low-reliability pattern — pair with a moving average or trendline."
        ),
    },

    "thrusting": {
        "name": "Thrusting",
        "type": "bearish",
        "reliability": 5,
        "description": (
            "A two-candle bearish continuation: a large bearish candle in a downtrend is followed "
            "by a bullish candle that opens below the prior low and closes into the prior candle's "
            "body, but only below its midpoint. The bull candle makes a valiant attempt at recovery "
            "but cannot reach the center — sellers retain dominance."
        ),
        "trade_guidance": (
            "Enter short when a subsequent candle breaks below the low of the bullish counter-candle. "
            "Stop-loss above the high of the second candle. Similar to On Neck but with slightly "
            "deeper penetration — still requires confirmation before trading."
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
