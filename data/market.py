import streamlit as st
import yfinance as yf


@st.cache_data(ttl=3600)
def get_price_history(ticker, period="3mo"):
    ticker = ticker.upper().strip()

    data = yf.download(
        ticker,
        period=period,
        interval="1d",
        auto_adjust=False,
        progress=False
    )

    return data


def get_last_close(ticker):
    data = get_price_history(ticker, period="3mo")

    if data.empty:
        return None, None, data

    close_series = data["Close"]

    if hasattr(close_series, "columns"):
        close_series = close_series.iloc[:, 0]

    # 마지막 행은 장중 현재가일 수 있으므로, 전일 확정 종가는 -2 사용
    latest_date = close_series.index[-2]
    latest_close = float(close_series.iloc[-2])

    return latest_close, latest_date, data


def get_vix_value():
    data = get_price_history("^VIX", period="5d")

    if data.empty:
        return None

    vix_data = data["Close"].iloc[-1]

    if hasattr(vix_data, "iloc"):
        vix_value = float(vix_data.iloc[0])
    else:
        vix_value = float(vix_data)

    return vix_value