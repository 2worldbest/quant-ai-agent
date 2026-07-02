import streamlit as st
from indicators.moving_average import calculate_moving_average
from indicators.rsi import calculate_rsi
from data.market import get_last_close, get_vix_value
from helpers.status import get_rsi_status, get_ma_status, get_vix_status


def extract_close_series(df):
    close_series = df["Close"]
    if hasattr(close_series, "columns"):
        close_series = close_series.iloc[:, 0]
    return close_series


def render_metric_cards(close_price, latest_rsi, latest_ma20, latest_ma60, vix_value):
    rsi_emoji, rsi_status = get_rsi_status(latest_rsi)
    ma20_emoji, ma20_status = get_ma_status(close_price, latest_ma20)
    ma60_emoji, ma60_status = get_ma_status(close_price, latest_ma60)
    vix_emoji, vix_status = get_vix_status(vix_value)

    metrics = [
        ("Previous Close", f"${close_price:.2f}"),
        (f"RSI ({rsi_status})", f"{rsi_emoji} {latest_rsi:.1f}"),
        (f"20-Day MA ({ma20_status})", f"{ma20_emoji} ${latest_ma20:.2f}"),
        (f"60-Day MA ({ma60_status})", f"{ma60_emoji} ${latest_ma60:.2f}"),
        (f"VIX ({vix_status})", f"{vix_emoji} {vix_value:.1f}" if vix_value is not None else "⚪ N/A"),
    ]

    columns = st.columns(len(metrics))

    for column, (label, value) in zip(columns, metrics):
        with column:
            st.metric(label=label, value=value)

def render_price_chart(close_series):
    st.subheader("📈 최근 5일 종가 추이")

    recent_close = close_series.tail(5).copy()
    recent_close.index = recent_close.index.strftime("%m-%d")
    st.line_chart(recent_close)


def render_summary(ticker, close_price, close_date, close_series):
    rsi_series = calculate_rsi(close_series)
    ma20_series = calculate_moving_average(close_series, window=20)
    ma60_series = calculate_moving_average(close_series, window=60)

    latest_rsi = rsi_series.iloc[-1]
    latest_ma20 = ma20_series.iloc[-1]
    latest_ma60 = ma60_series.iloc[-1]
    vix_value = get_vix_value()

    st.subheader(f"📊 {ticker.upper()} 요약")
    render_metric_cards(close_price, latest_rsi, latest_ma20, latest_ma60, vix_value)
    st.caption(f"기준일 : {close_date.strftime('%Y-%m-%d')}")
    st.divider()
    render_price_chart(close_series)


st.set_page_config(
    page_title="Quant AI Agent",
    page_icon="📈",
    layout="wide",
)

st.title("📈 소연의 퀀트 AI")

ticker = st.text_input("티커를 입력하세요", value="SOXL")

if st.button("조회"):
    close_price, close_date, df = get_last_close(ticker)

    if df.empty:
        st.error("데이터를 가져오지 못했습니다. 티커를 확인해주세요.")
    else:
        render_summary(ticker, close_price, close_date, extract_close_series(df))
