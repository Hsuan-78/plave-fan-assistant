import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="PLAVE 追星助理", page_icon="💱", layout="centered")

st.title("💱 偶像周邊匯率比較小幫手")

jpy = st.number_input("💴 日圓價格", min_value=0.0, format="%.2f")
usd = st.number_input("💵 美元價格", min_value=0.0, format="%.2f")
krw = st.number_input("🇰🇷 韓圓價格", min_value=0.0, format="%.2f")

@st.cache_data
def get_rates():
    res = requests.get("https://open.er-api.com/v6/latest/USD")
    return res.json()["rates"]

rates = get_rates()

def convert(amount, cur):
    rate = rates["TWD"] / rates[cur]
    return round(rate, 3), round(amount * rate, 2)

results = []
for cur, amt in [("JPY", jpy), ("USD", usd), ("KRW", krw)]:
    rate, twd = convert(amt, cur)
    results.append((cur, amt, rate, twd))

st.markdown("## 💖 換算結果")
if any(r[1] > 0 for r in results):
    min_cost = min(r[3] for r in results if r[3] > 0)
    for cur, amt, rate, twd in results:
        if amt == 0:
            continue
        tag = "🌟 最划算！" if twd == min_cost else ""
        st.markdown(f"使用 **{cur}** 付款：{amt} → 約 **{twd} TWD**（1 {cur} ≈ {rate}）{tag}")
else:
    st.info("請輸入任一金額來換算")
