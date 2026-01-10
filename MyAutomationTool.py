import streamlit as st
import tweepy
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="Tech Pulse Global", page_icon="🌐")

# ربط السوارت (تويتر + جيمناي)
try:
    client = tweepy.Client(
        consumer_key=st.secrets["TWITTER_API_KEY"],
        consumer_secret=st.secrets["TWITTER_API_SECRET"],
        access_token=st.secrets["TWITTER_ACCESS_TOKEN"],
        access_token_secret=st.secrets["TWITTER_ACCESS_TOKEN_SECRET"]
    )
    # إعداد Gemini
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # تصحيح: استعملنا 'gemini-1.5-flash' ديريكت لتفادي خطأ 404
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    smart_link = st.secrets["SMART_LINK"]
    st.sidebar.success("✅ Engine Ready (Gemini)")
except Exception as e:
    st.sidebar.error(f"❌ Setup Error: {e}")

st.title("🌐 Tech Pulse Global Agent")

niche = st.selectbox("Target Topic", ["AI News", "Tech Trends", "Crypto", "Future Tech"])

if st.button("🔍 Scan for News"):
    try:
        # البحث عن آخر الأخبار في جوجل
        url = f"https://www.google.com/search?q={niche}+latest+news&hl=en"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        news = soup.find('h3').text if soup.find('h3') else f"Big update in {niche}"
        st.session_state['current_news'] = news
        st.info(f"Found: {news}")
    except:
        st.error("Could not fetch news.")

if 'current_news' in st.session_state:
    try:
        # صياغة التويتة بـ Gemini
        prompt = f"Write a viral English tweet about: {st.session_state['current_news']}. Use emojis. Max 200 chars. No links."
        response = model.generate_content(prompt)
        draft = response.text
        
        final_post = f"🚨 {draft}\n\nRead more 👇\n{smart_link}"
        final_text = st.text_area("Final Draft:", value=final_post, height=150)
        
        if st.button("🚀 Blast to X"):
            client.create_tweet(text=final_text)
            st.balloons()
            st.success("✅ Tweet is LIVE on Tech Pulse!")
    except Exception as e:
        st.error(f"Gemini Error: {e}")
