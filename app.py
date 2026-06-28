import streamlit as st

from data.market import get_last_close


# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="Quant AI Agent",
    page_icon="📈",
    layout="wide"
)

# -----------------------------
# 제목
# -----------------------------
st.title("📈 양적 AI 에이전트")

# -----------------------------
# 티커 입력
# -----------------------------
ticker = st.text_input(
    "티커를 입력하세요",
    value="SOXL"
)

# -----------------------------
# 조회 버튼
# -----------------------------
if st.button("조회"):

    close_price, close_date, df = get_last_close(ticker)

    if df.empty:
        st.error("데이터를 가져오지 못했습니다. 티커를 확인해주세요.")

    else:

        st.subheader(f"📊 {ticker.upper()} 요약")

        # 전일 종가 카드
        st.metric(
            label="전일 종가",
            value=f"${close_price:.2f}"
        )

        st.caption(f"기준일 : {close_date.strftime('%Y-%m-%d')}")

        st.divider()

        # 최근 5일 종가 그래프
        st.subheader("📈 최근 5일 종가 추이")

        close_series = df["Close"]

        # yfinance MultiIndex 대응
        if hasattr(close_series, "columns"):
            close_series = close_series.iloc[:, 0]

        # 날짜만 표시
        close_series.index = close_series.index.strftime("%m-%d")

        st.line_chart(close_series)