import streamlit as st
import tweepy
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Tech Pulse Global", page_icon="🌐")

# دالة لإعداد المحركات مع تصحيح الموديل
def setup_engines():
    try:
        # تأكد أن هاد السوارت كاينين فـ Secrets بنفس هاد السميات
        g_key = st.secrets["GEMINI_API_KEY"]
        s_link = st.secrets["SMART_LINK"]
        
        # إعداد تويتر
        client = tweepy.Client(
            consumer_key=st.secrets["TWITTER_API_KEY"],
            consumer_secret=st.secrets["TWITTER_API_SECRET"],
            access_token=st.secrets["TWITTER_ACCESS_TOKEN"],
            access_token_secret=st.secrets["TWITTER_ACCESS_TOKEN_SECRET"]
        )
        
        # إعداد Gemini (التصحيح هنا)
        genai.configure(api_key=g_key)
        # استعملنا الاسم القصير للموديل لتفادي 404
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        return client, model, s_link
    except Exception as e:
        st.error(f"⚠️ Secrets/Setup Error: {e}")
        return None, None, None

# تخزين فـ Session State باش ميبقاش يختفي
if 'init_done' not in st.session_state:
    st.session_state.client, st.session_state.model, st.session_state.link = setup_engines()
    st.session_state.init_done = True

client = st.session_state.client
model = st.session_state.model
smart_link = st.session_state.link

st.title("🌐 Tech Pulse Global Agent")

if model:
    st.sidebar.success("✅ Engine Ready")
else:
    st.sidebar.warning("⚠️ Engine Offline")

niche = st.selectbox("Topic", ["AI News", "Tech Trends", "Crypto"])

if st.button("🔍 Scan for News"):
    try:
        url = f"https://www.google.com/search?q={niche}+latest+news&hl=en"
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.text, "html.parser")
        st.session_state['news_content'] = soup.find('h3').text if soup.find('h3') else f"Latest in {niche}"
        st.info(f"Found: {st.session_state['news_content']}")
    except:
        st.error("Scan failed.")

if 'news_content' in st.session_state and model:
    try:
        # توليد البوست
        prompt = f"Write a viral tech tweet about: {st.session_state['news_content']}. Max 200 chars. Use emojis."
        response = model.generate_content(prompt)
        
        final_post = f"🚨 {response.text}\n\nRead more 👇\n{smart_link}"
        tweet_text = st.text_area("Draft:", value=final_post, height=150)
        
        if st.button("🚀 Blast to X"):
            client.create_tweet(text=tweet_text)
            st.balloons()
            st.success("✅ Live on X!")
    except Exception as e:
        st.error(f"❌ Gemini Error: {e}")
