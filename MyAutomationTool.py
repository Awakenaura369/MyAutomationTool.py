import streamlit as st
import tweepy
import requests
from bs4 import BeautifulSoup
from groq import Groq

# Page Config
st.set_page_config(page_title="AgoraMAI Global Control", page_icon="🌐")

# Load Secrets
try:
    client = tweepy.Client(
        consumer_key=st.secrets["TWITTER_API_KEY"],
        consumer_secret=st.secrets["TWITTER_API_SECRET"],
        access_token=st.secrets["TWITTER_ACCESS_TOKEN"],
        access_token_secret=st.secrets["TWITTER_ACCESS_TOKEN_SECRET"]
    )
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    smart_link = st.secrets["SMART_LINK"]
    st.sidebar.success("✅ System Online (English Mode)")
except Exception as e:
    st.sidebar.error("❌ Secrets Error!")

st.title("🚀 AgoraMAI Global Agent")

# Niche Selection
niche = st.selectbox("Select Target Topic", ["AI & Tech", "Crypto & Web3", "Space & Future"])

def fetch_news(topic):
    try:
        url = f"https://www.google.com/search?q={topic}+news&hl=en"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.find('h3').text if soup.find('h3') else f"Update on {topic}"
    except:
        return f"Global interest in {topic} spikes today!"

if st.button("🔍 Scan for Trends"):
    news = fetch_news(niche)
    st.session_state['news'] = news
    st.info(f"Breaking: {news}")

if 'news' in st.session_state:
    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a tech influencer. Write engaging English tweets."},
                {"role": "user", "content": f"Create a viral English tweet about: {st.session_state['news']}. Include emojis."}
            ]
        )
        ai_draft = completion.choices[0].message.content
        final_post = f"🚨 {ai_draft}\n\nRead more 👇\n{smart_link}"
        
        edited = st.text_area("Final Preview (English):", value=final_post, height=150)
        
        if st.button("🚀 Blast Globally"):
            client.create_tweet(text=edited)
            st.balloons()
            st.success("✅ Posted to Global Audience!")
    except Exception as e:
        st.error(f"AI Error: {e}")
