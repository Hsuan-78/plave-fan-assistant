import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="PLAVE 粉絲留言板", page_icon="💬", layout="centered")

st.title("💬 PLLI 留言板")
st.caption("自由留言、回覆、修改、按讚與分享應援話語！")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.form("add_msg_form"):
    user = st.text_input("你的暱稱", max_chars=20)
    msg = st.text_area("想說的話", max_chars=200)
    submitted = st.form_submit_button("送出留言")
    if submitted and user.strip() and msg.strip():
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        st.session_state.messages.insert(0, {
            "user": user,
            "msg": msg,
            "time": now,
            "likes": 0,
            "replies": [],
            "edit_mode": False
        })
        st.success("✅ 已留言")
        st.rerun()

st.markdown("### 📝 最新留言")
if not st.session_state.messages:
    st.info("目前尚無留言，快來留言第一則吧！")

for i, m in enumerate(st.session_state.messages):
    with st.expander(f"💬 {m['user']}｜🕒 {m['time']}"):
        if m.get("edit_mode", False):
            new_content = st.text_area("✏️ 修改留言內容", value=m["msg"], key=f"edit_text_{i}")
            save_col, cancel_col = st.columns(2)
            with save_col:
                if st.button("💾 儲存", key=f"save_{i}"):
                    st.session_state.messages[i]["msg"] = new_content
                    st.session_state.messages[i]["edit_mode"] = False
                    st.success("✅ 留言已更新")
                    st.rerun()
            with cancel_col:
                if st.button("❌ 取消", key=f"cancel_{i}"):
                    st.session_state.messages[i]["edit_mode"] = False
                    st.rerun()
        else:
            st.markdown(f"**留言內容：** {m['msg']}")
            st.markdown(f"👍 按讚數：{m['likes']}")

        with st.form(f"reply_form_{i}"):
            reply_user = st.text_input("你的暱稱", key=f"reply_user_{i}")
            reply_msg = st.text_input("回覆內容", key=f"reply_msg_{i}")
            reply_btn = st.form_submit_button("回覆")
            if reply_btn and reply_user.strip() and reply_msg.strip():
                now = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.session_state.messages[i]["replies"].append({
                    "user": reply_user,
                    "msg": reply_msg,
                    "time": now
                })
                st.success("✅ 已回覆")
                st.rerun()

        if m["replies"]:
            st.markdown("📨 回覆：")
            for r in m["replies"]:
                st.markdown(f"- **{r['user']}**（{r['time']}）：{r['msg']}")

        op1, op2, op3 = st.columns(3)
        with op1:
            if not m.get("edit_mode", False) and st.button("✏️ 修改", key=f"edit_btn_{i}"):
                st.session_state.messages[i]["edit_mode"] = True
                st.rerun()
        with op2:
            if st.button("👍 按讚", key=f"like_{i}"):
                st.session_state.messages[i]["likes"] += 1
                st.rerun()
        with op3:
            if st.button("📤 分享（模擬）", key=f"share_{i}"):
                st.success("📎 已複製分享連結！（模擬）")
