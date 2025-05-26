import streamlit as st

st.set_page_config(page_title="PLLI 粉絲助理", page_icon="💜", layout="centered")
st.title("🌌 安妞，歡迎來到 PLLI 的天地！")

st.image("assets/PLLI.jpg", use_column_width=True)

st.markdown("""
這裡是一個大家可以共同創作的地方，  
各位 **PLLI 們** 可以在這邊共享資訊、也可以交朋友！

請從左側選單進入不同功能喔 💫  
👉 行程倒數助手、成員小百科、留言板、匯率助手等功能等你探索！
""", unsafe_allow_html=True)
