import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="PLAVE 粉絲留言板", page_icon="💬", layout="centered")
st.title("💬 PLAVE 粉絲留言牆")

MSG_FILE = "fan_messages.csv"

if "messages" not in st.session_state:
    if os.path.exists(MSG_FILE):
        st.session_state.messages = pd.read_csv(MSG_FILE).to_dict("records")
    else:
        st.session_state.messages = []

def save_messages():
    pd.DataFrame(st.session_state.messages).to_csv(MSG_FILE, index=False)

with st.form("留言表單", clear_on_submit=True):
    name = st.text_input("你的名字")
    message = st.text_area("想說的話")
    submit_msg = st.form_submit_button("送出留言")
    if submit_msg and name and message:
        st.session_state.messages.append({
            "name": name,
            "message": message,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        save_messages()
        st.success("✅ 已送出留言")

st.subheader("📝 所有留言")
if not st.session_state.messages:
    st.info("目前沒有留言，快來發表第一則吧！")
else:
    for msg in reversed(st.session_state.messages):
        with st.container():
            st.markdown(f"**{msg['name']}** 說：")
            st.markdown(f"> {msg['message']}")
            st.caption(f"🕓 {msg['time']}")
            st.markdown("---")
