import streamlit as st
import tweepy
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Tech Pulse Dashboard", page_icon="🌐")

# إعداد المحركات مع Cache لتفادي تكرار الأخطاء
@st.cache_resource
def init_engines():
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        client = tweepy.Client(
            consumer_key=st.secrets["TWITTER_API_KEY"],
            consumer_secret=st.secrets["TWITTER_API_SECRET"],
            access_token=st.secrets["TWITTER_ACCESS_TOKEN"],
            access_token_secret=st.secrets["TWITTER_ACCESS_TOKEN_SECRET"]
        )
        return client, model
    except Exception as e:
        return None, str(e)

client, result = init_engines()

st.title("🌐 Tech Pulse Global Control")

if isinstance(result, str):
    st.sidebar.error(f"❌ Error: {result}")
else:
    st.sidebar.success("✅ Engine Ready (Gemini 1.5)")

topic = st.text_input("Niche Topic", "Artificial Intelligence")

if st.button("🔍 Fetch & Generate"):
    try:
        res = requests.get(f"https://www.google.com/search?q={topic}&hl=en")
        soup = BeautifulSoup(res.text, "html.parser")
        st.session_state.news = soup.find('h3').text if soup.find('h3') else "Latest Tech Trends"
        
        # توليد بـ Gemini
        gen_res = result.generate_content(f"Tweet about: {st.session_state.news}. Max 200 chars.")
        st.session_state.draft = f"🚨 {gen_res.text}\n\nRead more: {st.secrets['SMART_LINK']}"
        st.success("Draft Generated!")
    except Exception as e:
        st.error(f"Error: {e}")

if 'draft' in st.session_state:
    final_text = st.text_area("Edit Draft:", value=st.session_state.draft, height=150)
    if st.button("🚀 Post to X"):
        client.create_tweet(text=final_text)
        st.balloons()
        st.success("✅ Live on Twitter!")
