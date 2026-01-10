import streamlit as st
import tweepy
import requests
from bs4 import BeautifulSoup
from groq import Groq

st.set_page_config(page_title="Tech Pulse (Groq)", page_icon="⚡")

@st.cache_resource
def init_engines():
    try:
        # إعداد Groq و Twitter
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

st.title("⚡ Tech Pulse Control (Groq Edition)")

if isinstance(groq_engine, str):
    st.sidebar.error(f"❌ Connection Error: {groq_engine}")
else:
    st.sidebar.success("✅ Groq Engine Active!")

topic = st.text_input("Niche Topic", "Artificial Intelligence")

if st.button("🔍 Generate with Groq"):
    try:
        res = requests.get(f"https://www.google.com/search?q={topic}&hl=en")
        soup = BeautifulSoup(res.text, "html.parser")
        news = soup.find('h3').text if soup.find('h3') else "Latest Tech Update"
        
        # توليد بـ Groq
        chat_completion = groq_engine.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": f"Tweet about: {news}. Max 200 chars."}]
        )
        st.session_state.draft = f"🚨 {chat_completion.choices[0].message.content}\n\nRead: {st.secrets['SMART_LINK']}"
        st.success("Draft Ready!")
    except Exception as e:
        st.error(f"Error: {e}")

if 'draft' in st.session_state:
    final_text = st.text_area("Edit Draft:", value=st.session_state.draft, height=150)
    if st.button("🚀 Blast to X"):
        client.create_tweet(text=final_text)
        st.balloons()
        st.success("✅ Success!")
