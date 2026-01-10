import streamlit as st
import tweepy
import requests
from bs4 import BeautifulSoup
from groq import Groq

st.set_page_config(page_title="Global Tech Agent", page_icon="⚡")

@st.cache_resource
def init_engines():
    try:
        groq_c = Groq(api_key=st.secrets["GROQ_API_KEY"])
        tw_c = tweepy.Client(
            consumer_key=st.secrets["TWITTER_API_KEY"],
            consumer_secret=st.secrets["TWITTER_API_SECRET"],
            access_token=st.secrets["TWITTER_ACCESS_TOKEN"],
            access_token_secret=st.secrets["TWITTER_ACCESS_TOKEN_SECRET"]
        )
        return tw_c, groq_c
    except Exception as e:
        return None, str(e)

client, groq_engine = init_engines()

st.title("⚡ Global Tech Pulse Control")

if isinstance(groq_engine, str):
    st.sidebar.error(f"❌ Error: {groq_engine}")
else:
    st.sidebar.success("✅ Groq Llama 3.1 Active")

# استهداف نيتشات عالمية
niche = st.selectbox("Select Global Target", ["AI & Machine Learning", "Web3 & Crypto", "Future Gadgets", "Space Tech"])

if st.button("🔍 Scan Global News"):
    try:
        # بحث في جوجل نيوز بالإنجليزية للجمهور العالمي
        url = f"https://www.google.com/search?q={niche}+latest+news&hl=en&gl=us"
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.text, "html.parser")
        news = soup.find('h3').text if soup.find('h3') else f"Major update in {niche}"
        st.session_state.global_news = news
        st.success(f"Trending Topic: {news}")
    except:
        st.error("Scan failed.")

if 'global_news' in st.session_state:
    try:
        # استدعاء الموديل الجديد llama-3.1-8b-instant
        chat_completion = groq_engine.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": f"Write a viral English tweet about: {st.session_state.global_news}. Make it professional, use emojis, include global tech hashtags. Max 200 chars. No links."}]
        )
        draft = chat_completion.choices[0].message.content.strip()
        st.session_state.final_draft = f"🚨 {draft}\n\nRead more 👇\n{st.secrets['SMART_LINK']}"
        
        final_text = st.text_area("Global Draft:", value=st.session_state.final_draft, height=150)
        
        if st.button("🚀 Blast to Global Audience"):
            client.create_tweet(text=final_text)
            st.balloons()
            st.success("✅ Successfully posted to X!")
    except Exception as e:
        st.error(f"Error: {e}")
