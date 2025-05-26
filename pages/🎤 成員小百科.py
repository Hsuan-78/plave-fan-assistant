import streamlit as st

st.set_page_config(page_title="PLAVE 成員小百科", page_icon="🎤", layout="centered")
st.title("🎤 PLAVE 成員小百科")

members = {
    "Yejun / 藝俊": {
        "photo": "yejun.jpeg",
        "生日": "2001.09.12", "年齡": "22", "身高": "183 cm", "血型": "B",
        "擔當": "隊長、Vocal", "符號": "🐬💙", "MBTI": "ISFJ-T",
        "興趣": "彈吉他、跑步、喝咖啡", "特長": "作詞作曲、跑步？",
        "喜歡": "音樂、咖啡、辣的食物、可愛動物", "討厭": "蟲子、炎熱的天氣"
    },
    "Noah / 諾亞": {
        "photo": "noah.jpeg",
        "生日": "2001.02.10", "年齡": "22", "身高": "179 cm", "血型": "O",
        "擔當": "自稱舞蹈（實際：Vocal）", "符號": "🦙💜", "MBTI": "ISTJ-A",
        "興趣": "唱歌、重訓、看電影", "特長": "作詞作曲、跳高？",
        "喜歡": "音樂、健身、咖啡", "討厭": "蟲子、嘈雜的地方、無禮的人、昏沈感"
    },
    "Bamby / 斑比": {
        "photo": "bamby.jpeg",
        "生日": "2002.07.15", "年齡": "21", "身高": "174 cm", "血型": "B",
        "擔當": "舞蹈、Vocal", "符號": "🦌💗", "MBTI": "INFP-T",
        "興趣": "跳舞、運動、演戲、看 Netflix", "特長": "跳舞、演戲、運動",
        "喜歡": "平壤冷麵、小狗、散步", "討厭": "又高又帥的人（銀虎）"
    },
    "Eunho / 銀虎": {
        "photo": "eunho.jpeg",
        "生日": "2003.05.24", "年齡": "20", "身高": "184 cm", "血型": "A",
        "擔當": "RAP、Vocal", "符號": "🐺❤️", "MBTI": "ENTP-T",
        "興趣": "重訓、游泳、看電影", "特長": "作曲、寫歌詞、RAP、游泳",
        "喜歡": "音樂、重訓、查餐廳跟……你們？", "討厭": "沒禮貌的人、虛偽、太吵"
    },
    "Hamin / 河玟": {
        "photo": "hamin.jpeg",
        "生日": "11月1日", "年齡": "20", "身高": "185 cm", "血型": "AB",
        "擔當": "RAP、舞蹈", "符號": "🐈‍⬛ 🖤", "MBTI": "ISFJ-T",
        "興趣": "畫畫、保齡球、看影片、足球", "特長": "RAP、舞蹈、跆拳道",
        "喜歡": "食物、鍛鍊、讚美、遊戲", "討厭": "謊言、蚊子"
    }
}

selected = st.selectbox("請選擇一位成員", list(members.keys()))
info = members[selected]
st.markdown(f"### {selected}")
st.image(f"./{info['photo']}", width=300, caption=f"{selected} 的照片")
for k, v in info.items():
    if k != "photo":
        st.markdown(f"**{k}**：{v}")
