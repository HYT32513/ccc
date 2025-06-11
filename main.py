import streamlit as st
import random
import openai

# OpenAI API 설정
openai.api_key = st.secrets["openai_api_key"]

# 이름 생성기 (더 많은 조합)
first_names = [
    "에리카", "레온", "키아나", "테오", "미레이", "하쿠", "리아", "벨렌", "제노", "카일", "엘리온", "아르테", "세피아", "라일락", "노르마", "실피드"
]
last_names = [
    "다크문", "블러드레이븐", "스노우필드", "블레이즈", "나이트폴", "윈터게일", "스톰루인", "샤도우크라운", "고스트하트", "엘더그레이브", "루인하임", "데스로즈"
]

def generate_character_name():
    return f"{random.choice(first_names)} {random.choice(last_names)}"

# 캐릭터 설명 생성
def generate_character_description(mood, concept):
    prompt = f"""
    분위기: {mood}
    배경: {concept}
    
    위의 분위기와 배경을 가진 캐릭터의 이름, 외형, 성격, 장식 요소, 의상 스타일을 자세히 묘사해줘. 
    고딕하거나 장식이 많은 스타일이면 더 좋아. 이름은 마지막에 따로 표시해줘.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.85
    )
    return response.choices[0].message.content.strip()

# 이미지 생성 (DALL·E 또는 OpenAI Image API)
def generate_character_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )
    return response['data'][0]['url']

# Streamlit UI 구성
st.set_page_config(page_title="고딕 캐릭터 생성기", page_icon="🦇", layout="centered")

st.markdown("""
    <style>
        body {
            background-color: #0d0d0d;
            color: #eeeeee;
        }
        .stButton>button {
            background-color: #550088;
            color: white;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🦇 고딕 & 으스스한 캐릭터 생성기")
st.markdown("원하는 분위기와 세계관을 입력하면, 이름부터 외형까지 자동 생성하고 이미지를 그려드려요!")

mood = st.text_input("💀 분위기 (예: 으스스하고 장식이 많은, 고딕풍, 유령이 나오는 등)")
concept = st.text_area("📜 세계관 및 캐릭터 설정 (예: 폐허가 된 성에 사는 망령의 왕자)")

if st.button("🔮 캐릭터 생성"):
    with st.spinner("운명의 캐릭터를 소환 중..."):
        name = generate_character_name()
        description = generate_character_description(mood, concept)
        full_prompt = f"gothic anime character, ornate costume, spooky, dark fantasy, {mood}, background: {concept}, highly detailed, illustration"
        image_url = generate_character_image(full_prompt)

        st.subheader("✨ 생성된 캐릭터")
        st.markdown(f"**이름:** `{name}`")
        st.write(description)
        st.image(image_url, caption=f"{name}의 모습", use_column_width=True)
