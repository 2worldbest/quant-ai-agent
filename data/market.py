import yfinance as yf
import streamlit as st

@st.cache_data(ttl=3600)
def get_price_history(ticker, period="5d"):
    ticker = ticker.upper().strip()

    data = yf.download(
        ticker,
        period=period,
        interval="1d",
        auto_adjust=False,
        progress=False
    )

    return data

@st.cache_data(ttl=3600)
def get_last_close(ticker):
    data = get_price_history(ticker, period="5d")

    if data.empty:
        return None, None, data

    latest_date = data.index[-1]
    close_data = data["Close"].iloc[-1]

    if hasattr(close_data, "iloc"):
        latest_close = float(close_data.iloc[0])
    else:
        latest_close = float(close_data)

    return latest_close, latest_date, data