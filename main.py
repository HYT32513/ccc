import streamlit as st
import random
import openai

# OpenAI API 키 설정 (Streamlit Secrets 사용)
openai.api_key = st.secrets["openai_api_key"]

# 🎭 이름 데이터베이스 (확장)
first_names = [
    "에리카", "레온", "키아나", "테오", "미레이", "하쿠", "리아", "벨렌", "제노", "카일", "엘리온", "아르테", "세피아", "라일락", "노르마", "실피드",
    "이리스", "카산드라", "드레이븐", "세레나", "에드가", "라스카", "블라디", "아르만", "에델", "네라", "루시엘", "모르가나", "에즈라", "칼릭스", "제피르", "오필리아"
]

last_names = [
    "다크문", "블러드레이븐", "스노우필드", "블레이즈", "나이트폴", "윈터게일", "스톰루인", "샤도우크라운", "고스트하트", "엘더그레이브",
    "루인하임", "데스로즈", "섀도우마르크", "크림슨소울", "팔켄브로", "그림나이트", "블러드쏜", "에버다스크", "그레이락", "이블마스크",
    "소드미스트", "나이트울프", "그림할로우", "루나그레이브", "다스혼", "레이븐폴", "오브시디안소울", "사일런트펠", "마블리치", "어비스윈드"
]

def generate_character_name():
    return f"{random.choice(first_names)} {random.choice(last_names)}"

# 📜 캐릭터 설명 생성
def generate_character_description(name, mood, concept):
    prompt = f"""
    캐릭터 이름: {name}
    분위기: {mood}
    배경 설정: {concept}

    위 정보를 바탕으로 다음을 작성해줘:
    - 캐릭터의 배경 이야기 (과거의 상처, 저주, 세계에서의 위치)
    - 철학적인 주제를 담은 스토리 구성
    - 캐릭터의 상징적 장비 및 능력
    - 상징적 결말 혹은 운명 (한 문장)
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.85
    )
    return response.choices[0].message.content.strip()

# 🖼 이미지 생성 (DALL·E)
def generate_character_image(mood, concept):
    prompt = f"Highly detailed fantasy character portrait, gothic style, {mood}, story: {concept}, dark atmosphere, ornate clothes, glowing effects, digital painting"
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )
    return response['data'][0]['url']

# 🌙 Streamlit UI 구성
st.set_page_config(page_title="심오한 캐릭터 생성기", page_icon="🕯️", layout="centered")

st.markdown("""
    <style>
        body {
            background-color: #111111;
            color: #eeeeee;
        }
        .stButton > button {
            background-color: #550088;
            color: white;
            border-radius: 5px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🕯️ 심오한 고딕 캐릭터 생성기")
st.markdown("당신이 상상한 분위기와 이야기로 만들어진 캐릭터를 직접 만나보세요.")

mood = st.text_input("🩸 분위기 (예: 어둡고 장식이 많은, 유령 같은, 장미와 어둠이 공존하는)")
concept = st.text_area("📖 배경 설정 (예: 천 년 전 전쟁에서 저주받고 잠든 왕국의 그림자 기사)")

if st.button("🔮 캐릭터 생성"):
    with st.spinner("고대의 영혼을 불러오는 중..."):
        name = generate_character_name()
        story = generate_character_description(name, mood, concept)
        image_url = generate_character_image(mood, concept)

        st.subheader(f"🕯️ 이름: {name}")
        st.image(image_url, caption=f"{name}의 모습", use_column_width=True)
        st.markdown("📜 **캐릭터 스토리**")
        st.write(story)

