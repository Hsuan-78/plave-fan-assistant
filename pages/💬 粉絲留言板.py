import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="PLAVE 粉絲留言板", page_icon="💬", layout="centered")
st.title("💬 PLAVE 粉絲留言牆")

MSG_FILE = "fan_messages.csv"

# 初始化留言資料
if "messages" not in st.session_state:
    if os.path.exists(MSG_FILE):
        st.session_state.messages = pd.read_csv(MSG_FILE).to_dict("records")
    else:
        st.session_state.messages = []

# 保證欄位完整
for msg in st.session_state.messages:
    msg.setdefault("likes", 0)
    msg.setdefault("reply_to", None)

# 初始化互動狀態
if "editing" not in st.session_state:
    st.session_state.editing = None
if "replying" not in st.session_state:
    st.session_state.replying = None

def save_messages():
    pd.DataFrame(st.session_state.messages).to_csv(MSG_FILE, index=False)

# ➕ 新增留言
with st.form("留言表單", clear_on_submit=True):
    name = st.text_input("你的名字")
    message = st.text_area("想說的話")
    submit_msg = st.form_submit_button("送出留言")
    if submit_msg and name and message:
        st.session_state.messages.append({
            "id": len(st.session_state.messages),
            "name": name,
            "message": message,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "reply_to": None,
            "likes": 0
        })
        save_messages()
        st.success("✅ 已送出留言")

st.subheader("📝 所有留言")

# 留言顯示函式
def render_message(msg):
    with st.container():
        indent = "　" if msg.get("reply_to") is not None else ""
        st.markdown(f"{indent}**{msg['name']}** 說：")
        st.markdown(f"{indent}> {msg['message']}")
        st.caption(f"{indent}🕓 {msg['time']}")
        col1, col2, col3 = st.columns([1, 1, 6])
        with col1:
            if st.button(f"👍 {msg['likes']}", key=f"like_{msg['id']}"):
                msg["likes"] += 1
                save_messages()
                st.experimental_rerun()
        with col2:
            if st.button("✏️", key=f"edit_{msg['id']}"):
                st.session_state.editing = msg["id"]
        with col3:
            if st.button("💬 回覆", key=f"reply_{msg['id']}"):
                st.session_state.replying = msg["id"]
        st.markdown("---")

# 主要留言（未回覆的）
main_msgs = [m for m in st.session_state.messages if "reply_to" not in m or pd.isna(m["reply_to"]) or m["reply_to"] is None]
for msg in reversed(main_msgs):
    render_message(msg)
    replies = [m for m in st.session_state.messages if m.get("reply_to") == msg["id"]]
    for r in replies:
        render_message(r)

# ✏️ 編輯區
if st.session_state.editing is not None:
    msg_id = st.session_state.editing
    target = next((m for m in st.session_state.messages if m["id"] == msg_id), None)
    if target:
        st.subheader("✏️ 編輯留言")
        with st.form("edit_form"):
            new_msg = st.text_area("修改內容", value=target["message"])
            save_btn = st.form_submit_button("儲存修改")
            if save_btn and new_msg:
                target["message"] = new_msg
                save_messages()
                st.session_state.editing = None
                st.success("✅ 已更新留言")
                st.experimental_rerun()

# 💬 回覆區
if st.session_state.replying is not None:
    parent_id = st.session_state.replying
    parent = next((m for m in st.session_state.messages if m["id"] == parent_id), None)
    if parent:
        st.subheader(f"💬 回覆給 {parent['name']}")
        with st.form("reply_form"):
            name = st.text_input("你的名字", key="reply_name")
            message = st.text_area("你的回覆", key="reply_message")
            send = st.form_submit_button("送出回覆")
            if send and name and message:
                st.session_state.messages.append({
                    "id": len(st.session_state.messages),
                    "name": name,
                    "message": message,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "reply_to": parent_id,
                    "likes": 0
                })
                save_messages()
                st.session_state.replying = None
                st.success("✅ 已送出回覆")
                st.experimental_rerun()
