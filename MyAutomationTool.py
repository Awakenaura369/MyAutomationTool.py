import streamlit as st
import tweepy
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Tech Pulse Global", page_icon="🌐")

# إعداد المحركات
@st.cache_resource
def load_engines():
    try:
        # إعداد Gemini بالسمية القصيرة (هذا هو الحل للـ 404)
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # إعداد تويتر
        client = tweepy.Client(
            consumer_key=st.secrets["TWITTER_API_KEY"],
            consumer_secret=st.secrets["TWITTER_API_SECRET"],
            access_token=st.secrets["TWITTER_ACCESS_TOKEN"],
            access_token_secret=st.secrets["TWITTER_ACCESS_TOKEN_SECRET"]
        )
        return client, model
    except Exception as e:
        st.error(f"Setup Error: {e}")
        return None, None

client, model = load_engines()

st.title("🌐 Tech Pulse Agent (Gemini)")

topic = st.selectbox("Topic", ["AI", "Crypto", "Tech"])

if st.button("🔍 Scan"):
    res = requests.get(f"https://www.google.com/search?q={topic}+latest+news&hl=en")
    soup = BeautifulSoup(res.text, "html.parser")
    st.session_state.news = soup.find('h3').text if soup.find('h3') else "New Tech Update"
    st.info(f"Found: {st.session_state.news}")

if 'news' in st.session_state and model:
    if st.button("🚀 Generate & Post"):
        try:
            # توليد النص
            response = model.generate_content(f"Tweet about: {st.session_state.news}. Max 200 chars.")
            tweet_text = f"🚨 {response.text}\n\nRead: {st.secrets['SMART_LINK']}"
            
            # النشر
            client.create_tweet(text=tweet_text)
            st.success("✅ Tweet is LIVE!")
            st.balloons()
        except Exception as e:
            st.error(f"Gemini/Twitter Error: {e}")
