import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

st.set_page_config(page_title="PLAVE 行程倒數助手", page_icon="📅", layout="centered")
st.title("📅 PLAVE 行程倒數助手")

SCHEDULE_FILE = "schedules.csv"

if "schedule" not in st.session_state:
    if os.path.exists(SCHEDULE_FILE):
        df = pd.read_csv(SCHEDULE_FILE, parse_dates=["start", "end"])
        st.session_state.schedule = df.to_dict("records")
    else:
        st.session_state.schedule = []

def save_schedule():
    df = pd.DataFrame(st.session_state.schedule)
    df.to_csv(SCHEDULE_FILE, index=False)

category_options = ["官方活動", "粉絲應援", "演唱會資訊", "節目出演", "社群直播", "其他"]

with st.form("add_event_form", clear_on_submit=True):
    st.subheader("➕ 新增行程")
    name = st.text_input("活動名稱")
    category = st.selectbox("活動類別", category_options)
    start_date = st.date_input("開始日期", value=datetime.now().date())
    start_time = st.time_input("開始時間", value=datetime.now().time())
    end_date = st.date_input("結束日期", value=datetime.now().date())
    end_time = st.time_input("結束時間", value=(datetime.now() + timedelta(hours=1)).time())
    start_dt = datetime.combine(start_date, start_time)
    end_dt = datetime.combine(end_date, end_time)

    submit = st.form_submit_button("新增行程")
    if submit and name:
        st.session_state.schedule.append({
            "name": name,
            "category": category,
            "start": start_dt,
            "end": end_dt
        })
        save_schedule()
        st.success("✅ 已新增行程")

st.subheader("📋 所有行程")
if not st.session_state.schedule:
    st.info("目前尚未新增任何行程")
else:
    now = datetime.now()
    header = st.columns([2, 2, 2.5, 2.5, 2, 1.5])
    header[0].markdown("**活動名稱**")
    header[1].markdown("**類別**")
    header[2].markdown("**開始時間**")
    header[3].markdown("**結束時間**")
    header[4].markdown("**狀態**")
    header[5].markdown("**操作**")

    for i, event in enumerate(st.session_state.schedule):
        status = (
            f"🕒 倒數 {((event['start'] - now).days)} 天"
            if event["start"] > now else
            ("🟢 進行中" if event["start"] <= now <= event["end"] else "⚫ 已結束")
        )
        cols = st.columns([2, 2, 2.5, 2.5, 2, 1.5])
        cols[0].markdown(event["name"])
        cols[1].markdown(event["category"])
        cols[2].markdown(event["start"].strftime("%Y-%m-%d %H:%M"))
        cols[3].markdown(event["end"].strftime("%Y-%m-%d %H:%M"))
        cols[4].markdown(status)
        with cols[5]:
            if st.button("✏️", key=f"edit_{i}"):
                st.session_state.editing = i
            if st.button("🗑", key=f"delete_{i}"):
                st.session_state.schedule.pop(i)
                save_schedule()
                st.experimental_rerun()

if "editing" in st.session_state:
    idx = st.session_state.editing
    ev = st.session_state.schedule[idx]
    st.subheader("✏️ 編輯行程")
    with st.form("edit_form"):
        new_name = st.text_input("活動名稱", value=ev["name"])
        new_cat = st.selectbox("活動類別", category_options, index=category_options.index(ev["category"]))
        new_start_date = st.date_input("開始日期", value=ev["start"].date())
        new_start_time = st.time_input("開始時間", value=ev["start"].time())
        new_end_date = st.date_input("結束日期", value=ev["end"].date())
        new_end_time = st.time_input("結束時間", value=ev["end"].time())
        new_start = datetime.combine(new_start_date, new_start_time)
        new_end = datetime.combine(new_end_date, new_end_time)

        save_btn = st.form_submit_button("儲存變更")
        if save_btn:
            st.session_state.schedule[idx] = {
                "name": new_name,
                "category": new_cat,
                "start": new_start,
                "end": new_end
            }
            del st.session_state.editing
            save_schedule()
            st.success("✅ 已更新行程")
            st.experimental_rerun()
