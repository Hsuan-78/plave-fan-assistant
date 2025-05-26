import streamlit as st

st.set_page_config(page_title="PLLI 的天地", page_icon="✨", layout="centered")

# 星空背景圖 + 卡片樣式
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #fce4ec, #e0f7fa);
    color: #3f3f3f;
}
h1, h2, h3 {
    color: #7b1fa2;
    font-family: 'Segoe UI', 'Noto Sans TC', sans-serif;
}
span, p {
    font-family: 'Segoe UI', 'Noto Sans TC', sans-serif;
}
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# 開始卡片內容
st.markdown("<div class='card'>", unsafe_allow_html=True)

# LOGO 圖片
st.image("assets/PLLI.jpg", caption="💖 PLLI 的 LOGO", use_container_width=True)

st.markdown("""
<audio controls>
  <source src="app.mp3" type="audio/mpeg">
  您的瀏覽器不支援音訊播放。
</audio>
""", unsafe_allow_html=True)

# 歡迎文字
st.markdown("""
## ✨ 安妞！歡迎來到 **PLLI 的天地**
這裡是一個大家可以共同創作的地方，  
各位 **PLLI 們** 可以在這裡互相分享資訊、  
也能在這邊交朋友、聊天、應援我們的 PLAVE！🌌
""", unsafe_allow_html=True)

# 簡介
st.markdown("### 📘 PLAVE 簡介")
st.markdown("""
**PLAVE** 是韓國的虛擬偶像男團，由五位成員組成：

包括 NOAH、YEJUN、BAMBY、EUNHO 和 HAMIN，有別於過去的虛擬偶像，
PLAVE 除了成員們的風格宛如從少女漫畫中走出來的「撕漫男」以外，
他們的運作方式也相當特別，所有演出、直播、MV 等背後都是由真人實際參與來進行動態捕捉，
採用 3D 模組技術，揮別於過往二次元偶像的模式，若要與粉絲互動主要是以 Live2D 呈現，以真人動態作為捕捉的 PLAVE，
不論是與粉絲互動或是私下成員們的一舉一動，都像極了直接跟漫畫人物在現實生活進行交流。

出道於 2023 年，以虛擬形象與超高製作品質受到全球粉絲喜愛！
""", unsafe_allow_html=True)

# 音樂播放器
st.markdown("""
<div style="text-align: center;">
    <iframe width="300" height="170"
        src="https://www.youtube.com/embed/cFm8fTRW_so?loop=1&playlist=cFm8fTRW_so"
        frameborder="0"
        allow="autoplay; encrypted-media"
        allowfullscreen>
    </iframe>
    <br>
    <span style="font-size: 0.9em;">🎵 點上方播放 PLAVE - Wait for you</span>
</div>
""", unsafe_allow_html=True)

# 結束卡片
st.markdown("</div>", unsafe_allow_html=True)

st.caption("🌌 Designed for PLLI — 星空與希望的起點 💫")
