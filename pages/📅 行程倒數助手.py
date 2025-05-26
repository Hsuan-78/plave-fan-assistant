import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

st.set_page_config(page_title="PLAVE 行程倒數助手", page_icon="📅", layout="centered")
st.title("📅 PLAVE 行程倒數助手")

DATA_FILE = "schedule_data.csv"

# 資料載入
if "schedule" not in st.session_state:
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df["start"] = pd.to_datetime(df["start"])
        df["end"] = pd.to_datetime(df["end"])
        st.session_state.schedule = df.to_dict("records")
    else:
        st.session_state.schedule = []

if "editing" not in st.session_state:
    st.session_state.editing = None

def save_data():
    pd.DataFrame(st.session_state.schedule).to_csv(DATA_FILE, index=False)

# 活動類別選項
category_options = ["官方活動", "粉絲應援", "演唱會資訊", "節目出演", "社群直播", "其他"]

st.subheader("➕ 新增行程")
with st.form("add_event_form", clear_on_submit=True):
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
        save_data()
        st.success("✅ 已新增行程")

# 顯示所有行程
st.subheader("📋 所有行程")
if not st.session_state.schedule:
    st.info("目前尚未新增任何行程")
else:
    df = pd.DataFrame(st.session_state.schedule)
    df_display = df.copy()
    df_display["期間"] = df["start"].astype(str) + " ～ " + df["end"].astype(str)
    df_display = df_display[["name", "category", "期間"]]
    st.dataframe(df_display.rename(columns={"name": "活動名稱", "category": "活動類別"}), use_container_width=True)

    for i, event in enumerate(st.session_state.schedule):
        col1, col2 = st.columns([8, 2])
        with col1:
            st.markdown(f"**{event['name']}**｜{event['category']}")
            st.markdown(f"⏳ {event['start']} ～ {event['end']}")
            now = datetime.now()
            if event["start"] > now:
                left = event["start"] - now
                st.markdown(f"🕒 尚未開始，倒數：{left.days} 天 {left.seconds//3600} 小時")
            elif event["start"] <= now <= event["end"]:
                st.markdown("🟢 活動進行中！")
            else:
                st.markdown("⚫ 活動已結束")
        with col2:
            if st.button("✏️ 編輯", key=f"edit_{i}"):
                st.session_state.editing = i
            if st.button("🗑 刪除", key=f"delete_{i}"):
                st.session_state.schedule.pop(i)
                save_data()
                st.experimental_rerun()

# 編輯區
if st.session_state.editing is not None:
    idx = st.session_state.editing
    if idx < len(st.session_state.schedule):
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

            save = st.form_submit_button("儲存變更")
            if save:
                st.session_state.schedule[idx] = {
                    "name": new_name,
                    "category": new_cat,
                    "start": new_start,
                    "end": new_end
                }
                save_data()
                st.session_state.editing = None
                st.success("✅ 已更新行程")
                st.experimental_rerun()