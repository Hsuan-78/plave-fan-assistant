import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="行程倒數助手", page_icon="📅", layout="centered")
st.title("📅 PLAVE 行程倒數助手")

# 初始化資料
if "schedule" not in st.session_state:
    st.session_state.schedule = []

# 活動類別選項
category_options = ["官方活動", "粉絲應援", "演唱會資訊", "節目出演", "社群直播", "其他"]

# 新增行程
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
        st.success("✅ 已新增行程")

# 顯示所有行程（表格方式）
st.subheader("📋 所有行程")
if not st.session_state.schedule:
    st.info("目前尚未新增任何行程")
else:
    df = pd.DataFrame(st.session_state.schedule)
    df_display = df.copy()
    now = datetime.now()
    df_display["狀態"] = df_display.apply(lambda row: (
        f"🕒 倒數 {((row['start'] - now).days)} 天"
        if row["start"] > now else
        ("🟢 進行中" if row["start"] <= now <= row["end"] else "⚫ 已結束")
    ), axis=1)
    df_display["開始時間"] = df_display["start"].dt.strftime("%Y-%m-%d %H:%M")
    df_display["結束時間"] = df_display["end"].dt.strftime("%Y-%m-%d %H:%M")
    df_display = df_display[["name", "category", "開始時間", "結束時間", "狀態"]]
    df_display.columns = ["活動名稱", "類別", "開始時間", "結束時間", "狀態"]
    st.dataframe(df_display, use_container_width=True)

    for i in range(len(st.session_state.schedule)):
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"✏️ 編輯第 {i+1} 筆", key=f"edit_{i}"):
                st.session_state.editing = i
        with col2:
            if st.button(f"🗑 刪除第 {i+1} 筆", key=f"delete_{i}"):
                st.session_state.schedule.pop(i)
                st.experimental_rerun()

# 編輯區
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

        save = st.form_submit_button("儲存變更")
        if save:
            st.session_state.schedule[idx] = {
                "name": new_name,
                "category": new_cat,
                "start": new_start,
                "end": new_end
            }
            del st.session_state.editing
            st.success("✅ 已更新行程")
            st.experimental_rerun()
