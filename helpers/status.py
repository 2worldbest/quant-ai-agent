def get_rsi_status(rsi):
    if rsi < 30:
        return "🔵", "Oversold"
    elif rsi <= 70:
        return "🟢", "Neutral"
    else:
        return "🔴", "Overbought"


def get_ma_status(close_price, moving_average):
    if close_price > moving_average:
        return "🟢", "Above"
    else:
        return "🔴", "Below"


def get_vix_status(vix):
    if vix is None:
        return "⚪", "N/A"
    elif vix < 20:
        return "🟢", "Stable"
    elif vix <= 30:
        return "🟡", "Caution"
    else:
        return "🔴", "Risk"