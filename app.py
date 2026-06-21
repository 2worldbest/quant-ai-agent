import streamlit as st

st.set_page_config(
    page_title="Quant AI Agent",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Quant AI Agent")

st.write("안녕하세요!")

st.success("첫 번째 Streamlit 프로그램이 정상적으로 실행되었습니다.")

if st.button("눌러보세요"):
    st.balloons()
    st.success("축하합니다! 첫 번째 Streamlit 앱이 성공적으로 실행되었습니다.")