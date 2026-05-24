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

    # ── Smart Money Concepts (SMC) — Order Blocks ──────────────────────────────

    "bullish_order_block": {
        "name": "Bullish Order Block",
        "type": "bullish",
        "reliability": 8,
        "description": (
            "The last bearish candle before a strong impulse move upward, identified by Smart Money "
            "Concepts (SMC). Institutional buyers placed large orders at this zone, leaving a price "
            "footprint. When price returns to this area, it typically finds demand and bounces "
            "strongly, as institutions defend their original position entries."
        ),
        "trade_guidance": (
            "Enter long when price retraces into the Order Block zone (body of the last bearish "
            "candle before the impulse). Stop-loss just below the OB low. Target the next liquidity "
            "pool or previous high. Best used on 15m–4H timeframes with HTF confluence."
        ),
    },

    "bearish_order_block": {
        "name": "Bearish Order Block",
        "type": "bearish",
        "reliability": 8,
        "description": (
            "The last bullish candle before a strong impulse move downward, identified by SMC. "
            "Institutional sellers placed large short orders in this zone. When price retraces up "
            "to this area, supply overwhelms demand and price typically rejects sharply downward, "
            "repeating the institutional sell pattern."
        ),
        "trade_guidance": (
            "Enter short when price retraces into the Order Block zone (body of the last bullish "
            "candle before the bearish impulse). Stop-loss just above the OB high. Target the "
            "previous low or the next demand zone. Combine with bearish BOS for higher confluence."
        ),
    },

    "bullish_breaker_block": {
        "name": "Bullish Breaker Block",
        "type": "bullish",
        "reliability": 8,
        "description": (
            "A former Bearish Order Block that has been invalidated by a Break of Structure to the "
            "upside. Once price breaks above the swing high that the bearish OB was protecting, the "
            "OB 'flips' polarity and becomes a demand zone (Breaker Block). Institutions use this "
            "level to add to long positions on the retest."
        ),
        "trade_guidance": (
            "Enter long on retracement back to the Breaker Block zone. Stop-loss below the zone. "
            "Target the next supply zone or liquidity pool above. The BOS confirmation before the "
            "retest makes this a high-probability setup."
        ),
    },

    "bearish_breaker_block": {
        "name": "Bearish Breaker Block",
        "type": "bearish",
        "reliability": 8,
        "description": (
            "A former Bullish Order Block that has been invalidated by a Break of Structure to the "
            "downside. Once price breaks below the swing low the bullish OB was protecting, it "
            "flips to a supply zone. When price retraces back into this area, sellers re-engage "
            "strongly, making it a high-confluence short entry zone."
        ),
        "trade_guidance": (
            "Enter short on retracement back into the Breaker Block zone. Stop-loss above the zone. "
            "Target the next demand zone or equal lows below. Confirm with a bearish BOS and "
            "lower-timeframe rejection candle at the zone."
        ),
    },

    "bullish_mitigation_block": {
        "name": "Bullish Mitigation Block",
        "type": "bullish",
        "reliability": 7,
        "description": (
            "A price area where institutional buyers failed to push price higher on the first "
            "attempt, leaving unfilled orders (unmitigated demand). When price returns to this "
            "zone, the remaining orders are 'mitigated' (filled), causing a strong bounce. Similar "
            "to an OB but specifically marks incomplete institutional business."
        ),
        "trade_guidance": (
            "Enter long at the mitigation block zone on a lower-timeframe confirmation candle. "
            "Stop-loss below the zone. Target the failed swing high from the first attempt. "
            "Works best when price approaches from below with bullish momentum."
        ),
    },

    "bearish_mitigation_block": {
        "name": "Bearish Mitigation Block",
        "type": "bearish",
        "reliability": 7,
        "description": (
            "A price area where institutional sellers failed to push price lower on the first "
            "attempt, leaving unfilled supply orders. When price returns to this zone, the "
            "remaining sell orders are triggered, causing a sharp rejection downward. Most "
            "effective after a failed breakdown attempt followed by a retest."
        ),
        "trade_guidance": (
            "Enter short at the mitigation block zone with lower-timeframe confirmation. "
            "Stop-loss above the zone high. Target the failed swing low or the next demand zone. "
            "Most effective when combined with a bearish CHOCH or BOS confirmation."
        ),
    },

    # ── Smart Money Concepts — Fair Value Gaps (FVG) ───────────────────────────

    "bullish_fvg": {
        "name": "Bullish Fair Value Gap",
        "type": "bullish",
        "reliability": 7,
        "description": (
            "A three-candle imbalance where the high of candle 1 and the low of candle 3 do not "
            "overlap, leaving a gap in price that was skipped in a rapid bullish move. This gap "
            "represents inefficiency in price delivery and acts as a magnet — price often retraces "
            "to fill it before continuing the trend. Also called a bullish imbalance zone."
        ),
        "trade_guidance": (
            "Enter long when price retraces into the FVG zone (between candle 1 high and candle 3 "
            "low). Stop-loss below the FVG bottom. Target the previous high or next imbalance. "
            "Best used when FVG aligns with an Order Block for confluence."
        ),
    },

    "bearish_fvg": {
        "name": "Bearish Fair Value Gap",
        "type": "bearish",
        "reliability": 7,
        "description": (
            "A three-candle downward imbalance where the low of candle 1 and the high of candle 3 "
            "do not overlap, leaving a bearish price gap. Created during rapid institutional selling. "
            "Price tends to retrace upward to fill this gap before continuing lower. It acts as a "
            "distribution zone where sellers re-enter."
        ),
        "trade_guidance": (
            "Enter short when price retraces up into the FVG zone. Stop-loss above the FVG top. "
            "Target the previous low or the next demand zone. High conviction when FVG sits within "
            "a Bearish Order Block or Breaker Block zone."
        ),
    },

    "fvg_continuation": {
        "name": "FVG Continuation",
        "type": "neutral",
        "reliability": 7,
        "description": (
            "When price retraces into a Fair Value Gap and then resumes in the original trend "
            "direction, it confirms the FVG acted as support/resistance and the trend is intact. "
            "This continuation pattern shows that the imbalance zone absorbed counter-trend "
            "pressure and institutional order flow remains directionally committed."
        ),
        "trade_guidance": (
            "Enter in trend direction when price touches the FVG zone and shows a rejection "
            "candle (pin bar, engulfing, or doji). Stop just outside the FVG. Target next "
            "imbalance zone or swing high/low. Most reliable on higher timeframes (1H, 4H, Daily)."
        ),
    },

    "fvg_reversal": {
        "name": "FVG Reversal",
        "type": "neutral",
        "reliability": 6,
        "description": (
            "When price aggressively blows through an FVG zone without any pause or rejection, "
            "it signals a potential reversal of the prevailing trend. This 'violation' of the "
            "imbalance zone indicates that the opposing institutional force is strong enough to "
            "override the existing order flow, suggesting a trend change may be underway."
        ),
        "trade_guidance": (
            "Wait for price to fully close through the FVG zone, then look for a structural "
            "shift (CHOCH) on a lower timeframe. Enter in the new direction on the retest of the "
            "violated FVG as new S/R. Stop above the entry candle's wick. Requires patience and confirmation."
        ),
    },

    "bullish_ifvg": {
        "name": "Bullish Inverse Fair Value Gap (iFVG)",
        "type": "bullish",
        "reliability": 7,
        "description": (
            "An FVG that has been violated and flipped — a Bearish FVG that price has broken "
            "through to the upside, inverting its polarity from resistance to support. The iFVG "
            "becomes a bullish demand zone on retest, as the institutional order that originally "
            "caused the bearish imbalance has been absorbed and overcome."
        ),
        "trade_guidance": (
            "Enter long when price retraces back to the iFVG zone after the bullish violation. "
            "Stop-loss below the iFVG zone. Target the next supply zone or previous high. "
            "Confirm with a lower-timeframe bullish structure shift before entry."
        ),
    },

    "bearish_ifvg": {
        "name": "Bearish Inverse Fair Value Gap (iFVG)",
        "type": "bearish",
        "reliability": 7,
        "description": (
            "A Bullish FVG that has been violated to the downside, flipping its polarity from "
            "support to resistance. The zone that was once a demand imbalance now acts as supply "
            "on retest. Institutional sell orders have overwhelmed the original buyers, and the "
            "flipped zone attracts new short entries from smart money."
        ),
        "trade_guidance": (
            "Enter short when price retraces up to the iFVG zone after the bearish violation. "
            "Stop-loss above the iFVG zone top. Target the previous low or next demand zone. "
            "Best used when iFVG sits near a Breaker Block or in a clear downtrend structure."
        ),
    },

    # ── Smart Money Concepts — Structure ───────────────────────────────────────

    "bullish_bos": {
        "name": "Bullish Break of Structure (BOS)",
        "type": "bullish",
        "reliability": 8,
        "description": (
            "Price breaks above a previous swing high in an existing uptrend, confirming trend "
            "continuation. The BOS signals that buyers have overcome supply at a key resistance "
            "level and are establishing higher highs. In SMC, a BOS in an uptrend indicates "
            "institutional accumulation and momentum continuation."
        ),
        "trade_guidance": (
            "Enter long on the retest of the broken swing high (now acting as support) or the "
            "FVG/OB left behind during the impulse. Stop-loss below the retest low. Target the "
            "next liquidity pool above. Best combined with bullish OB or FVG confluence."
        ),
    },

    "bearish_bos": {
        "name": "Bearish Break of Structure (BOS)",
        "type": "bearish",
        "reliability": 8,
        "description": (
            "Price breaks below a previous swing low in an existing downtrend, confirming bearish "
            "trend continuation. Indicates institutional distribution is ongoing and sellers are "
            "successfully pushing price to new lows. Each BOS lower represents a new wave of "
            "smart money selling pressure."
        ),
        "trade_guidance": (
            "Enter short on the retest of the broken swing low (now acting as resistance) or the "
            "bearish OB/FVG from the impulse move. Stop-loss above the retest high. Target the "
            "next demand zone or equal lows below."
        ),
    },

    "bullish_choch": {
        "name": "Bullish Change of Character (CHOCH)",
        "type": "bullish",
        "reliability": 8,
        "description": (
            "In a downtrend, price breaks above the most recent swing high for the first time, "
            "signaling a potential trend reversal from bearish to bullish. The CHOCH is the first "
            "sign that institutional buyers have stepped in and taken control, disrupting the "
            "previous lower-high, lower-low sequence. Distinct from BOS — it signals a new trend, not continuation."
        ),
        "trade_guidance": (
            "Enter long on the retest of the CHOCH level or the bullish OB/FVG created during "
            "the CHOCH impulse. Stop-loss below the swing low that preceded the CHOCH. Target "
            "the next major supply zone. Lower timeframe confirmation strongly recommended."
        ),
    },

    "bearish_choch": {
        "name": "Bearish Change of Character (CHOCH)",
        "type": "bearish",
        "reliability": 8,
        "description": (
            "In an uptrend, price breaks below the most recent swing low for the first time, "
            "signaling a potential trend reversal from bullish to bearish. The CHOCH indicates "
            "that institutional sellers have overcome buying pressure and initiated distribution. "
            "It is the critical first signal that the bullish trend structure has been broken."
        ),
        "trade_guidance": (
            "Enter short on the retest of the CHOCH level or the bearish OB/FVG from the impulse. "
            "Stop-loss above the swing high that preceded the CHOCH. Target the next major demand "
            "zone. Use lower timeframe structure to fine-tune entry for better risk-reward."
        ),
    },

    # ── Liquidity Concepts ─────────────────────────────────────────────────────

    "bullish_liquidity_sweep": {
        "name": "Bullish Liquidity Sweep",
        "type": "bullish",
        "reliability": 8,
        "description": (
            "Price briefly dips below a key swing low or support level, triggering stop-losses "
            "and buy-stop orders from retail traders, then rapidly reverses upward. Smart money "
            "uses this sweep to accumulate long positions at better prices by hunting the liquidity "
            "resting below the obvious support level."
        ),
        "trade_guidance": (
            "Enter long when price sweeps below the key level and the candle closes back above it "
            "(a wick below the level with bullish close). Stop-loss below the sweep wick low. "
            "Target the previous high or next supply zone. Best at equal lows or marked support."
        ),
    },

    "bearish_liquidity_sweep": {
        "name": "Bearish Liquidity Sweep",
        "type": "bearish",
        "reliability": 8,
        "description": (
            "Price briefly spikes above a key swing high or resistance level, triggering stop-losses "
            "and sell-stop orders, then rapidly reverses downward. Institutions use this move to "
            "distribute (sell) large positions at inflated prices using retail stop orders as "
            "liquidity. The sweep above resistance is a trap for breakout buyers."
        ),
        "trade_guidance": (
            "Enter short when price sweeps above the key level and closes back below it (a wick "
            "above with bearish close). Stop-loss above the sweep wick high. Target the previous "
            "low or next demand zone. Most powerful at equal highs or marked resistance levels."
        ),
    },

    "double_liquidity_sweep": {
        "name": "Double Liquidity Sweep",
        "type": "neutral",
        "reliability": 9,
        "description": (
            "Price sweeps liquidity on both sides of a range — first triggering stops below a "
            "support, then sweeping above a resistance (or vice versa) before making a decisive "
            "directional move. This double sweep clears all resting orders on both sides, giving "
            "institutions a clean order book for a high-velocity directional move."
        ),
        "trade_guidance": (
            "After both sides have been swept, enter in the direction of the final rejection with "
            "high conviction. Stop beyond the extreme of the final sweep. Target a move equal to "
            "the full range of the double sweep. One of the highest-probability SMC setups."
        ),
    },

    "bullish_liquidity_grab": {
        "name": "Bullish Liquidity Grab",
        "type": "bullish",
        "reliability": 7,
        "description": (
            "A sharp wick below a support zone that briefly touches resting buy orders and "
            "stop-losses before snapping back. The grab is typically quick — one or two candles — "
            "and shows up as a long lower wick on a key level. Institutions are filling long "
            "orders by triggering retail stop-losses as the sell side of their trade."
        ),
        "trade_guidance": (
            "Enter long when the candle with the long lower wick closes above the support level. "
            "Stop-loss below the wick low. Target the nearest resistance. Combine with an Order "
            "Block or FVG for highest conviction."
        ),
    },

    "bearish_liquidity_grab": {
        "name": "Bearish Liquidity Grab",
        "type": "bearish",
        "reliability": 7,
        "description": (
            "A sharp wick above a resistance zone that touches resting sell orders and buy stop-losses "
            "before reversing down. Appears as a long upper wick at a key level. Institutions "
            "distribute (sell) large positions using the retail momentum above the obvious resistance, "
            "then push price sharply lower after the grab."
        ),
        "trade_guidance": (
            "Enter short when the grabbing candle closes back below the resistance level. "
            "Stop-loss above the wick high. Target the nearest support or swing low. "
            "Best executed on 15m or 1H chart with HTF structure alignment."
        ),
    },

    "equal_highs_sweep": {
        "name": "Equal Highs Sweep",
        "type": "bearish",
        "reliability": 8,
        "description": (
            "Two or more swing highs at approximately the same price level create visible "
            "buy-stop liquidity. Smart money pushes price slightly above these equal highs to "
            "collect the resting orders, then sells aggressively into that liquidity. Equal highs "
            "are a major SMC concept — they signal a probable manipulation zone."
        ),
        "trade_guidance": (
            "Enter short after price wicks above the equal highs and closes back below them. "
            "Stop-loss above the wick high. Target the range low or next demand zone. "
            "A bearish engulfing or pin bar at the sweep adds significant confidence."
        ),
    },

    "equal_lows_sweep": {
        "name": "Equal Lows Sweep",
        "type": "bullish",
        "reliability": 8,
        "description": (
            "Two or more swing lows at approximately the same price level create visible "
            "sell-stop liquidity below. Institutions push price below these equal lows to trigger "
            "retail stop-losses and collect sell-side orders, then buy aggressively. Equal lows "
            "on any timeframe are a high-probability accumulation target."
        ),
        "trade_guidance": (
            "Enter long after price wicks below the equal lows and closes back above them. "
            "Stop-loss below the wick low. Target the range high or next supply zone. "
            "Combine with a bullish OB or FVG near the equal lows for maximum confluence."
        ),
    },

    "high_sweep_drop": {
        "name": "High Sweep + Drop",
        "type": "bearish",
        "reliability": 8,
        "description": (
            "Price sweeps above a previous significant high (taking out buy stops), then "
            "immediately reverses and drops sharply. The sweep is followed by a strong bearish "
            "impulse that often breaks the structure below. This is a classic SMC trap: "
            "retail traders buy the breakout; smart money sells into that buying pressure."
        ),
        "trade_guidance": (
            "Enter short when the sweeping candle closes below the swept high level. Aggressive "
            "entry: on the close of the sweep candle. Conservative: on the retest of the swept "
            "level from below. Stop above the sweep wick. Target the previous low or -1R minimum."
        ),
    },

    "low_sweep_rally": {
        "name": "Low Sweep + Rally",
        "type": "bullish",
        "reliability": 8,
        "description": (
            "Price sweeps below a previous significant low (triggering sell stops), then "
            "immediately reverses and rallies strongly. Retail sellers who shorted the breakdown "
            "get squeezed as price reverses. This is the bullish version of the SMC liquidity "
            "hunt — institutions accumulate longs at discount prices using retail stops as fuel."
        ),
        "trade_guidance": (
            "Enter long when the sweeping candle closes above the swept low level. Stop below "
            "the wick low. Target the previous high or a measured move equal to the pre-sweep "
            "range. Best at key daily/weekly lows with bullish higher-timeframe structure."
        ),
    },

    # ── Price Action Setups ────────────────────────────────────────────────────

    "bullish_pin_bar": {
        "name": "Bullish Pin Bar",
        "type": "bullish",
        "reliability": 8,
        "description": (
            "A single candle with a small body near the top and a long lower wick (at least 2x "
            "the body length). The long lower tail shows price was aggressively rejected from lower "
            "levels — sellers pushed price down but buyers reclaimed nearly all the losses. "
            "Most powerful at key support levels, demand zones, or SMC structures."
        ),
        "trade_guidance": (
            "Enter long above the high of the pin bar. Stop-loss below the wick low. "
            "Target the nearest resistance or the next swing high. Risk-reward is naturally "
            "favorable due to the tight stop. Add confluence with OB, FVG, or trendline support."
        ),
    },

    "bearish_pin_bar": {
        "name": "Bearish Pin Bar",
        "type": "bearish",
        "reliability": 8,
        "description": (
            "A single candle with a small body near the bottom and a long upper wick (at least 2x "
            "the body length). The extended upper tail signals a sharp rejection from higher prices — "
            "buyers pushed price up but sellers overwhelmed them and drove it back down. Most "
            "significant at resistance zones, supply areas, or after liquidity sweeps of highs."
        ),
        "trade_guidance": (
            "Enter short below the low of the pin bar. Stop-loss above the wick high. "
            "Target the nearest support or swing low. A bearish pin bar at a swept high or "
            "Order Block is one of the highest-probability entries in price action trading."
        ),
    },

    "bullish_inside_bar": {
        "name": "Bullish Inside Bar",
        "type": "bullish",
        "reliability": 7,
        "description": (
            "A candle whose high and low are entirely within the range of the prior (mother) candle, "
            "appearing in an uptrend or at a support level. The inside bar signals consolidation and "
            "compressed volatility before continuation. A bullish breakout above the mother bar's "
            "high confirms the pattern and signals trend resumption."
        ),
        "trade_guidance": (
            "Enter long on a break above the mother bar's high. Stop-loss below the inside bar's "
            "low (tight stop) or below the mother bar's low (wider). Target the next resistance. "
            "Works best as a continuation setup in established uptrends."
        ),
    },

    "bearish_inside_bar": {
        "name": "Bearish Inside Bar",
        "type": "bearish",
        "reliability": 7,
        "description": (
            "A candle whose range is fully contained within the prior (mother) candle, in a "
            "downtrend or at a resistance level. Represents consolidation within the dominant "
            "bearish move. A break below the mother bar's low triggers the bearish continuation "
            "signal as the compressed energy releases to the downside."
        ),
        "trade_guidance": (
            "Enter short on a break below the mother bar's low. Stop-loss above the inside bar's "
            "high. Target the next support zone or a measured move equal to the mother bar's range. "
            "Most reliable in strong downtrends — avoid trading against the higher timeframe trend."
        ),
    },

    "outside_bar": {
        "name": "Outside Bar",
        "type": "neutral",
        "reliability": 6,
        "description": (
            "A candle whose high is above and low is below the prior candle, fully engulfing it "
            "on both sides. Also called an 'Engulfing Bar' in price action trading. It represents "
            "a volatility expansion and can signal either reversal or continuation depending on "
            "where it appears. Direction is determined by the outside bar's close relative to the prior bar."
        ),
        "trade_guidance": (
            "Trade in the direction of the outside bar's close. Enter on a break of the outside "
            "bar's high (bullish) or low (bearish). Stop on the opposite extreme of the outside bar. "
            "Filter using trend direction and key S/R levels — avoid trading in choppy ranges."
        ),
    },

    "rejection_setup": {
        "name": "Rejection Setup",
        "type": "neutral",
        "reliability": 7,
        "description": (
            "Price tests a key level (support, resistance, trendline, OB, or FVG) and is sharply "
            "rejected, showing clear inability to sustain the move beyond that level. The rejection "
            "appears as a long wick or an engulfing candle at the zone. Direction depends on which "
            "level is being rejected — bullish at support, bearish at resistance."
        ),
        "trade_guidance": (
            "Enter in the direction of the rejection when the rejecting candle closes. Stop beyond "
            "the extreme of the rejection wick. Target the opposite key level. Strongest when the "
            "rejection aligns with an SMC structure (OB, FVG, CHOCH) on a higher timeframe."
        ),
    },

    "break_and_retest": {
        "name": "Break and Retest",
        "type": "neutral",
        "reliability": 8,
        "description": (
            "Price breaks through a key support or resistance level with conviction, then pulls "
            "back to retest the broken level (now acting as flipped S/R) before continuing in the "
            "breakout direction. One of the most classic and reliable price action setups across "
            "all timeframes and markets. Institutions often initiate positions during the retest."
        ),
        "trade_guidance": (
            "Enter on the retest of the broken level. For bullish: enter long when price bounces "
            "from the broken resistance (now support). For bearish: enter short when price rejects "
            "the broken support (now resistance). Stop beyond the retest level. Target 1.5-3x risk."
        ),
    },

    "support_rejection": {
        "name": "Support Rejection",
        "type": "bullish",
        "reliability": 7,
        "description": (
            "Price reaches a well-defined support level and shows clear rejection with a long lower "
            "wick or bullish reversal candle. The support has been tested and held, confirming "
            "demand is present at that price. Multiple successful tests of the same support level "
            "increase the reliability of the next rejection."
        ),
        "trade_guidance": (
            "Enter long when the rejection candle closes above the support level. Stop-loss just "
            "below the rejection wick or the support zone. Target the nearest resistance. "
            "Add a second position after a pullback confirms the support holds."
        ),
    },

    "resistance_rejection": {
        "name": "Resistance Rejection",
        "type": "bearish",
        "reliability": 7,
        "description": (
            "Price reaches a key resistance level and is sharply rejected with a long upper wick "
            "or bearish reversal candle. The resistance holds as supply overwhelms demand at that "
            "price. Previous rejections from the same zone increase pattern reliability and often "
            "result in faster, larger moves on subsequent rejections."
        ),
        "trade_guidance": (
            "Enter short when the rejection candle closes below the resistance level. Stop-loss "
            "above the wick high. Target the nearest support or the prior swing low. "
            "Works best when resistance aligns with a Bearish OB, FVG, or equal highs."
        ),
    },

    "trendline_support": {
        "name": "Trendline Support",
        "type": "bullish",
        "reliability": 7,
        "description": (
            "Price touches a well-defined ascending trendline (connecting at least two swing lows) "
            "and bounces, confirming the trendline as dynamic support. Each successful test of the "
            "trendline provides a buying opportunity in the direction of the trend. The more times "
            "the trendline has been tested, the more significant the next touch."
        ),
        "trade_guidance": (
            "Enter long when price touches the trendline and forms a rejection candle (pin bar, "
            "engulfing). Stop-loss below the trendline. Target the upper channel boundary or the "
            "prior swing high. Never trade a first-touch trendline — require at least two confirmed touches."
        ),
    },

    "trendline_resistance": {
        "name": "Trendline Resistance",
        "type": "bearish",
        "reliability": 7,
        "description": (
            "Price touches a well-defined descending trendline (connecting at least two swing highs) "
            "and is rejected, confirming the trendline as dynamic resistance. Each failed attempt "
            "to break the trendline reinforces seller confidence. A bearish candle at the trendline "
            "provides a high-probability short entry in the downtrend."
        ),
        "trade_guidance": (
            "Enter short when price touches the trendline and shows a bearish rejection candle. "
            "Stop-loss above the trendline. Target the lower channel boundary or prior swing low. "
            "Trendline breaks should be treated as a separate setup, not traded as resistance bounces."
        ),
    },

    # ── Chart Patterns ─────────────────────────────────────────────────────────

    "head_and_shoulders": {
        "name": "Head and Shoulders",
        "type": "bearish",
        "reliability": 8,
        "description": (
            "A three-peak bearish reversal pattern: a left shoulder (moderate high), a head "
            "(higher high), and a right shoulder (lower high that matches the left shoulder). "
            "The neckline connects the two lows between the peaks. A close below the neckline "
            "triggers the pattern and signals a major trend reversal from bullish to bearish."
        ),
        "trade_guidance": (
            "Enter short on a confirmed close below the neckline. Stop-loss above the right "
            "shoulder's high. Measured target: subtract the head-to-neckline distance from the "
            "neckline breakout point. A retest of the neckline as resistance provides a second "
            "lower-risk entry opportunity."
        ),
    },

    "inverse_head_and_shoulders": {
        "name": "Inverse Head and Shoulders",
        "type": "bullish",
        "reliability": 8,
        "description": (
            "A three-trough bullish reversal: a left shoulder (moderate low), a head (lower low), "
            "and a right shoulder (higher low matching the left). The neckline connects the two "
            "highs between the troughs. A close above the neckline signals a major reversal from "
            "bearish to bullish. Volume typically increases on the right shoulder and breakout."
        ),
        "trade_guidance": (
            "Enter long on a confirmed close above the neckline. Stop-loss below the right "
            "shoulder's low. Measured target: add the head-to-neckline distance to the neckline "
            "breakout point. A neckline retest as support offers a lower-risk entry."
        ),
    },

    "double_top": {
        "name": "Double Top",
        "type": "bearish",
        "reliability": 8,
        "description": (
            "Two peaks at approximately the same price level separated by a trough, forming an 'M' "
            "shape. The second top failing to exceed the first signals buyer exhaustion at that "
            "level. Confirmation occurs when price breaks below the trough (the neckline) between "
            "the two peaks, signaling a potential trend reversal to bearish."
        ),
        "trade_guidance": (
            "Enter short on a confirmed break below the neckline between the two tops. Stop-loss "
            "above the second top. Measured target: the distance from the tops to the neckline "
            "subtracted from the breakout point. Volume should contract on the second top and "
            "expand on the neckline break."
        ),
    },

    "double_bottom": {
        "name": "Double Bottom",
        "type": "bullish",
        "reliability": 8,
        "description": (
            "Two troughs at approximately the same price level separated by a peak, forming a 'W' "
            "shape. The second bottom holding at the same level as the first signals strong demand. "
            "Confirmation occurs when price breaks above the peak between the two lows. One of the "
            "most commonly traded and reliable bullish reversal patterns."
        ),
        "trade_guidance": (
            "Enter long on a confirmed break above the neckline (the peak between the two bottoms). "
            "Stop-loss below the second bottom. Measured target: add the distance from the bottoms "
            "to the neckline to the breakout point. Volume confirmation on the neckline break is key."
        ),
    },

    "triple_top": {
        "name": "Triple Top",
        "type": "bearish",
        "reliability": 8,
        "description": (
            "Three successive peaks at approximately the same price level, showing that price "
            "has repeatedly failed to break through resistance. After three failed attempts, "
            "sellers gain the upper hand and a breakdown below the support between the peaks "
            "confirms a bearish reversal. More reliable than a Double Top due to the triple "
            "rejection confirmation."
        ),
        "trade_guidance": (
            "Enter short on a break below the lows between the three peaks. Stop-loss above the "
            "highest peak. Measured target: the height of the pattern subtracted from the "
            "breakdown point. The triple rejection is a strong signal — target larger than a Double Top."
        ),
    },

    "triple_bottom": {
        "name": "Triple Bottom",
        "type": "bullish",
        "reliability": 8,
        "description": (
            "Three successive troughs at approximately the same price level, showing strong "
            "demand consistently absorbing selling at that zone. After the third test of support, "
            "a breakout above the resistance between the troughs confirms a bullish reversal. "
            "The triple support test indicates a major accumulation zone."
        ),
        "trade_guidance": (
            "Enter long on a break above the highs between the three troughs. Stop-loss below the "
            "lowest trough. Measured target: the height of the pattern added to the breakout point. "
            "Volume should spike on the breakout to confirm institutional participation."
        ),
    },

    "symmetrical_triangle": {
        "name": "Symmetrical Triangle",
        "type": "neutral",
        "reliability": 7,
        "description": (
            "A consolidation pattern with converging trendlines — lower highs and higher lows — "
            "forming a symmetric triangle. Both buyers and sellers compress into an equilibrium. "
            "The breakout direction determines trade bias; typically resolves in the direction of "
            "the prior trend. Volume contracts during formation and expands on breakout."
        ),
        "trade_guidance": (
            "Trade the breakout: enter long above the upper trendline or short below the lower "
            "trendline. Stop on the opposite trendline. Target: width of the triangle's widest "
            "point added to the breakout. Beware of false breakouts — wait for a close beyond the line."
        ),
    },

    "ascending_triangle": {
        "name": "Ascending Triangle",
        "type": "bullish",
        "reliability": 8,
        "description": (
            "A bullish consolidation pattern with a flat upper resistance (equal highs) and a "
            "rising lower trendline (higher lows). Buyers are becoming more aggressive, willing "
            "to buy at higher prices, while sellers defend a fixed level. Eventually buyers "
            "overpower sellers and price breaks out above the flat resistance."
        ),
        "trade_guidance": (
            "Enter long on a confirmed close above the flat resistance level. Stop-loss below the "
            "most recent higher low. Measured target: height of the triangle's widest left side "
            "added to the breakout level. Volume expansion on the breakout is a strong confirmation signal."
        ),
    },

    "descending_triangle": {
        "name": "Descending Triangle",
        "type": "bearish",
        "reliability": 8,
        "description": (
            "A bearish consolidation with a flat lower support (equal lows) and a descending upper "
            "trendline (lower highs). Sellers are becoming increasingly aggressive at lower levels "
            "while buyers defend a fixed support. Eventually sellers break through the floor and "
            "price collapses below the flat support."
        ),
        "trade_guidance": (
            "Enter short on a confirmed close below the flat support level. Stop-loss above the "
            "most recent lower high. Measured target: height of the triangle's widest point "
            "subtracted from the breakout level. Declining volume into the breakout confirms seller dominance."
        ),
    },

    "rectangle_breakout": {
        "name": "Rectangle Breakout",
        "type": "neutral",
        "reliability": 7,
        "description": (
            "Price consolidates between a flat support and a flat resistance, forming a rectangle "
            "or range. Multiple tests of both levels compress price before a breakout. The "
            "breakout direction determines trade bias — bullish breakout above resistance, bearish "
            "below support. Volume typically spikes significantly on the breakout candle."
        ),
        "trade_guidance": (
            "Enter in the direction of the breakout. Stop on the opposite side of the rectangle. "
            "Measured target: height of the rectangle added to the breakout level. A retest of "
            "the broken level as S/R flip offers a second, lower-risk entry."
        ),
    },

    "bullish_flag": {
        "name": "Bullish Flag",
        "type": "bullish",
        "reliability": 8,
        "description": (
            "A bullish continuation: a sharp vertical rally (the flagpole) followed by a brief "
            "downward-sloping channel (the flag) representing a controlled pullback. The flag "
            "shows sellers testing the move but failing to reverse it. A breakout above the upper "
            "flag boundary signals continuation with a measured move equal to the flagpole."
        ),
        "trade_guidance": (
            "Enter long on a breakout above the upper channel boundary of the flag. Stop-loss "
            "below the lower flag boundary. Target: add the flagpole length to the breakout point. "
            "High volume on the flagpole and contracting volume in the flag confirm the pattern."
        ),
    },

    "bearish_flag": {
        "name": "Bearish Flag",
        "type": "bearish",
        "reliability": 8,
        "description": (
            "A bearish continuation: a sharp vertical decline (flagpole) followed by a brief "
            "upward-sloping channel (flag) representing a shallow counter-trend bounce. Buyers "
            "are unable to reverse the trend — the pullback is weak relative to the drop. "
            "A breakdown below the lower flag boundary confirms continuation."
        ),
        "trade_guidance": (
            "Enter short on a breakout below the lower channel boundary. Stop-loss above the "
            "upper flag boundary. Target: subtract the flagpole length from the breakdown point. "
            "Contracting volume during the flag and expanding on breakdown is the ideal volume profile."
        ),
    },

    "bullish_pennant": {
        "name": "Bullish Pennant",
        "type": "bullish",
        "reliability": 8,
        "description": (
            "Similar to the Bullish Flag but with converging trendlines forming a symmetrical "
            "triangle instead of a parallel channel. A strong rally (flagpole) is followed by "
            "a tight symmetrical consolidation as price compresses. The breakout above the upper "
            "trendline signals continuation with a measured move equal to the flagpole."
        ),
        "trade_guidance": (
            "Enter long on breakout above the pennant's upper trendline. Stop below the pennant's "
            "lower trendline. Target: flagpole length added to the breakout point. Volume should "
            "contract sharply during the pennant and surge on the breakout."
        ),
    },

    "bearish_pennant": {
        "name": "Bearish Pennant",
        "type": "bearish",
        "reliability": 8,
        "description": (
            "A bearish continuation: a sharp drop (flagpole) followed by a symmetrical converging "
            "consolidation. Price compresses into a triangle as bulls and bears reach temporary "
            "equilibrium. A breakdown below the lower trendline signals continuation of the "
            "downtrend with a measured move equal to the flagpole."
        ),
        "trade_guidance": (
            "Enter short on breakdown below the pennant's lower trendline. Stop above the pennant's "
            "upper trendline. Target: flagpole length subtracted from the breakdown point. "
            "Sharp volume contraction during the pennant and expansion on breakdown is ideal."
        ),
    },

    "cup_and_handle": {
        "name": "Cup and Handle",
        "type": "bullish",
        "reliability": 8,
        "description": (
            "A bullish continuation pattern: a rounded bottom forming a U-shape (the cup) followed "
            "by a small downward drift channel (the handle). The cup represents a gradual recovery "
            "from a decline, and the handle is a brief consolidation before breakout. The handle "
            "should not retrace more than one-third of the cup's depth."
        ),
        "trade_guidance": (
            "Enter long on a breakout above the handle's resistance (the rim of the cup). "
            "Stop-loss below the handle's low. Measured target: depth of the cup added to the "
            "breakout point. A volume surge on the breakout above the rim is a strong confirmation."
        ),
    },

    "rising_wedge": {
        "name": "Rising Wedge",
        "type": "bearish",
        "reliability": 8,
        "description": (
            "A bearish reversal or continuation pattern: price moves between two upward-sloping "
            "converging trendlines. Higher highs and higher lows narrow into a wedge as buyers "
            "lose conviction. Despite the apparent uptrend, the pattern resolves bearishly — "
            "price breaks down through the lower trendline and often falls sharply."
        ),
        "trade_guidance": (
            "Enter short on a confirmed close below the lower trendline. Stop above the last "
            "swing high within the wedge. Target: the start of the wedge pattern. Watch for "
            "volume declining as the wedge forms and expanding on the breakdown."
        ),
    },

    "falling_wedge": {
        "name": "Falling Wedge",
        "type": "bullish",
        "reliability": 8,
        "description": (
            "A bullish reversal or continuation pattern: price declines between two downward-sloping "
            "converging trendlines. Lower highs and lower lows narrow into a wedge but with "
            "diminishing momentum. Despite the apparent downtrend, the resolution is typically "
            "bullish — price breaks upward through the upper trendline."
        ),
        "trade_guidance": (
            "Enter long on a confirmed close above the upper trendline. Stop below the last "
            "swing low within the wedge. Target: the start of the wedge. Volume contraction "
            "during the wedge and a strong surge on the breakout are the key confirmation signals."
        ),
    },

    "channel_up": {
        "name": "Channel Up",
        "type": "bullish",
        "reliability": 7,
        "description": (
            "Price moves within two upward-sloping parallel trendlines, creating a rising channel. "
            "The lower trendline acts as support and the upper as resistance. Traders can buy at "
            "the lower channel boundary (support bounce) or prepare for a short if price "
            "overextends to the upper boundary. A breakout above the channel signals acceleration."
        ),
        "trade_guidance": (
            "For channel trading: enter long at the lower trendline support, stop below the channel. "
            "Target the upper channel boundary. For a breakout trade: enter long above the upper "
            "trendline. A channel breakdown (close below the lower trendline) signals trend reversal."
        ),
    },

    "channel_down": {
        "name": "Channel Down",
        "type": "bearish",
        "reliability": 7,
        "description": (
            "Price moves within two downward-sloping parallel trendlines forming a declining channel. "
            "The upper trendline acts as resistance and the lower as support. Sellers dominate "
            "and each rally is sold at the upper boundary. A breakout above the upper trendline "
            "signals a potential reversal while breakdowns below the lower signal acceleration."
        ),
        "trade_guidance": (
            "For channel trading: enter short at the upper trendline resistance, stop above channel. "
            "Target the lower boundary. For reversal: enter long on a close above the upper "
            "trendline. A channel breakdown (close below the lower trendline) signals trend continuation."
        ),
    },

    # ── Harmonic Patterns ──────────────────────────────────────────────────────

    "bat_pattern": {
        "name": "Bat Pattern (Harmonic)",
        "type": "neutral",
        "reliability": 8,
        "description": (
            "A harmonic reversal pattern using Fibonacci ratios: a sharp move (XA), a retracement "
            "to B (38.2%-50% of XA), an extension to C (38.2%-88.6% of AB), and a retracement to "
            "D at 88.6% of XA — the Potential Reversal Zone (PRZ). Defined by Scott Carney, "
            "the Bat has one of the highest success rates of all harmonic patterns."
        ),
        "trade_guidance": (
            "Enter at point D (88.6% Fibonacci retracement of XA). Stop beyond point X. "
            "Bullish Bat: enter long at D, target C then A. Bearish Bat: enter short at D, "
            "target C then A. Use the 88.6% level as the tight stop zone for excellent R:R."
        ),
    },

    "gartley_pattern": {
        "name": "Gartley Pattern (Harmonic)",
        "type": "neutral",
        "reliability": 8,
        "description": (
            "The original harmonic pattern from H.M. Gartley's 1935 book. Structure: XA move, "
            "B retraces 61.8% of XA, C retraces 38.2%-88.6% of AB, D completes at 78.6% of XA "
            "— the Potential Reversal Zone. The Gartley is considered the 'perfect' harmonic "
            "pattern and offers a well-defined PRZ with excellent risk-reward."
        ),
        "trade_guidance": (
            "Enter at the D point (78.6% Fibonacci retracement of XA). Stop beyond X. "
            "Bullish Gartley: long at D, target C (38.2% extension) then A. "
            "Bearish Gartley: short at D, same targets inverted. Risk is defined by the X point."
        ),
    },

    "butterfly_pattern": {
        "name": "Butterfly Pattern (Harmonic)",
        "type": "neutral",
        "reliability": 7,
        "description": (
            "A harmonic reversal discovered by Bryce Gilmore: XA move, B retraces 78.6% of XA, "
            "C retraces 38.2%-88.6% of AB, D extends to 127.2%-161.8% of XA — beyond point X. "
            "Unlike other harmonics, the Butterfly completes beyond the origin of the pattern, "
            "often marking extreme exhaustion moves and major reversal points."
        ),
        "trade_guidance": (
            "Enter at the D point (127.2% or 161.8% extension of XA). Stop beyond D's extreme. "
            "Bullish Butterfly: long at D, target 38.2%-61.8% retracement of the CD leg. "
            "Bearish Butterfly: short at D with same targets inverted. Tightest stop of all harmonics."
        ),
    },

    "crab_pattern": {
        "name": "Crab Pattern (Harmonic)",
        "type": "neutral",
        "reliability": 8,
        "description": (
            "Discovered by Scott Carney, the Crab pattern features the most extreme extension: "
            "XA move, B retraces 38.2%-61.8% of XA, C retraces 38.2%-88.6% of AB, D extends "
            "to 161.8% of XA — the largest extension of any harmonic. Carney considers it the "
            "most precise harmonic pattern with the tightest PRZ."
        ),
        "trade_guidance": (
            "Enter at the D point (161.8% extension of XA). Stop: just beyond D's extreme. "
            "Bullish Crab: long at D, target 38.2%-61.8% of CD. Bearish Crab: short with same "
            "targets inverted. The 161.8% completion requires patience but yields excellent R:R "
            "when the PRZ holds."
        ),
    },

    # ── Market Structure & Momentum ────────────────────────────────────────────

    "impulse_move": {
        "name": "Impulse Move",
        "type": "neutral",
        "reliability": 7,
        "description": (
            "A sharp, fast, high-momentum price move in one direction with minimal overlapping "
            "candles and little retracement. Impulse moves represent strong institutional order "
            "flow and often leave behind Fair Value Gaps and Order Blocks. Following an impulse, "
            "price typically retraces to fill imbalances before the next impulsive leg."
        ),
        "trade_guidance": (
            "Do not chase impulse moves. Instead, wait for the retracement phase and identify "
            "FVGs or OBs left by the impulse for entry. Enter at the imbalance zone in the "
            "direction of the impulse. Stop below the origin of the impulse move."
        ),
    },

    "correction_move": {
        "name": "Correction Move",
        "type": "neutral",
        "reliability": 6,
        "description": (
            "A controlled, overlapping pullback against the dominant trend following an impulse "
            "move. Corrections are characterized by slow, choppy price action with many overlapping "
            "candles. They serve to fill imbalances, retest OBs/FVGs, and reset oscillators "
            "before the trend resumes. Corrections should be traded carefully or avoided entirely."
        ),
        "trade_guidance": (
            "Avoid entering in the direction of the correction. Instead, use the correction to "
            "identify entry zones in the direction of the impulse. Wait for the correction to "
            "reach a key level (OB, FVG, Fibonacci) then look for reversal signals to join the "
            "main trend."
        ),
    },

    "v_shape_recovery": {
        "name": "V-Shape Recovery",
        "type": "bullish",
        "reliability": 7,
        "description": (
            "A sharp decline followed immediately by an equally sharp recovery forming a 'V' shape, "
            "with no consolidation at the bottom. The violent reversal shows extreme sentiment "
            "change — panic selling is instantly overwhelmed by aggressive buying. Often triggered "
            "by news events, liquidity sweeps, or a major support level being aggressively defended."
        ),
        "trade_guidance": (
            "Difficult to enter at the bottom of a V-shape in real time. Best approach: "
            "enter on the first pullback after the recovery leg, at the initial rally's FVG or OB. "
            "Stop below the V-shape low. Target the next resistance. Avoid chasing if already "
            "extended significantly from the low."
        ),
    },

    "contracting_range": {
        "name": "Contracting Range",
        "type": "neutral",
        "reliability": 6,
        "description": (
            "Price oscillates between support and resistance with each successive swing making "
            "a lower high and higher low — a contracting range or symmetrical triangle. Volume "
            "declines as the range tightens. A volatility squeeze is building and the pattern "
            "resolves with a breakout, typically in the direction of the prior trend."
        ),
        "trade_guidance": (
            "Wait for the breakout of the contracting range boundaries. Enter in the breakout "
            "direction with stop on the opposite boundary. Target: equal to the widest point of "
            "the range projected from the breakout. Avoid trading inside the range as S/R reliability decreases."
        ),
    },

    "expanding_range": {
        "name": "Expanding Range",
        "type": "neutral",
        "reliability": 5,
        "description": (
            "Price makes higher highs and lower lows with each swing, expanding the range "
            "progressively. This megaphone pattern indicates increasing volatility and uncertainty. "
            "Direction is unpredictable and the pattern is difficult to trade. It typically "
            "resolves with a violent move once one side capitulates — often to the downside."
        ),
        "trade_guidance": (
            "Avoid trading inside an expanding range. Wait for a clear breakdown below the "
            "pattern's lower support or a breakout above the upper resistance. Enter only on "
            "confirmation of direction with a wide stop to account for volatility. Reduce position size."
        ),
    },

    "bullish_fvg_order_block": {
        "name": "Bullish FVG + Order Block",
        "type": "bullish",
        "reliability": 9,
        "description": (
            "The highest-confluence bullish SMC setup: a Bullish Order Block and a Bullish Fair "
            "Value Gap overlap in the same price zone. The OB represents institutional demand and "
            "the FVG marks a price imbalance — when both align, the zone has double institutional "
            "significance. Price is expected to react strongly from this combined zone."
        ),
        "trade_guidance": (
            "Enter long when price enters the combined OB/FVG zone. Stop-loss just below the "
            "bottom of the zone. Target the next liquidity pool or supply zone. This is the "
            "highest-probability long entry in SMC trading — reduce risk if not aligned with "
            "higher timeframe bullish structure."
        ),
    },

    "bearish_fvg_order_block": {
        "name": "Bearish FVG + Order Block",
        "type": "bearish",
        "reliability": 9,
        "description": (
            "The highest-confluence bearish SMC setup: a Bearish Order Block and a Bearish Fair "
            "Value Gap overlap in the same price zone. Both the unfilled imbalance and institutional "
            "supply orders converge at the same level. When price retraces into this combined "
            "zone, the probability of a sharp rejection downward is significantly elevated."
        ),
        "trade_guidance": (
            "Enter short when price enters the combined OB/FVG zone. Stop-loss just above the "
            "top of the zone. Target the next demand zone or previous low. This is the highest-"
            "probability short entry in SMC. Align with bearish higher timeframe structure for "
            "maximum conviction."
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
