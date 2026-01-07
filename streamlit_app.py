import streamlit as st
from transformers import pipeline

# إعداد الصفحة
st.set_page_config(
    page_title="منصة مهدي للذكاء الاصطناعي",
    page_icon="🤖",
    layout="centered"
)

# العنوان
st.markdown("<h1 style='text-align:center;'>منصة مهدي للذكاء الاصطناعي 🤖</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>تطوير: عبدالرزاق مهدي</p>", unsafe_allow_html=True)
st.markdown("---")

# تحميل النموذج (مرة واحدة)
@st.cache_resource
def load_model():
    return pipeline(
        "text-generation",
        model="akhooli/gpt2-small-arabic"
    )

model = load_model()

# واجهة المستخدم
user_input = st.text_input("✍️ اكتب سؤالك هنا:")

if user_input:
    with st.spinner("⏳ الذكاء الاصطناعي يفكّر..."):
        result = model(
            user_input,
            max_length=120,
            do_sample=True,
            temperature=0.9
        )

    st.success("🤖 الرد:")
    st.write(result[0]["generated_text"])
