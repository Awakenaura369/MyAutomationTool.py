import streamlit as st
import tweepy
from groq import Groq
import time
import pandas as pd
from datetime import datetime

# --- إعداد الصفحة ---
st.set_page_config(page_title="X AI Adsterra Bot v2", page_icon="🐦", layout="wide")

# --- جلب السوارت من Secrets ---
try:
    X_CREDS = {
        "bearer_token": st.secrets["X_BEARER_TOKEN"],
        "api_key": st.secrets["X_API_KEY"],
        "api_secret": st.secrets["X_API_SECRET"],
        "access_token": st.secrets["X_ACCESS_TOKEN"],
        "access_token_secret": st.secrets["X_ACCESS_TOKEN_SECRET"]
    }
    GRO_KEY = st.secrets["GROQ_API_KEY"]
    LINK = st.secrets["SMART_LINK"]
except Exception as e:
    st.error("❌ Secrets Error: Check your Streamlit Dashboard settings.")
    st.stop()

# --- تهيئة العملاء ---
client_x = tweepy.Client(
    bearer_token=X_CREDS["bearer_token"],
    consumer_key=X_CREDS["api_key"],
    consumer_secret=X_CREDS["api_secret"],
    access_token=X_CREDS["access_token"],
    access_token_secret=X_CREDS["access_token_secret"]
)
groq_client = Groq(api_key=GRO_KEY)

# --- واجهة المستخدم ---
st.title("🚀 X AI Traffic Dashboard")

# Session state لتخزين السجل
if 'history' not in st.session_state:
    st.session_state.history = []

col_main, col_sidebar = st.columns([2, 1])

with col_sidebar:
    st.subheader("⚙️ Control Panel")
    keyword = st.text_input("Search Keyword", "crypto tips")
    limit = st.slider("Replies Limit", 1, 10, 2)
    delay = st.number_input("Delay (seconds)", 30, 300, 60)

with col_main:
    if st.button("🔥 Run Automation Cycle"):
        st.write(f"🔍 Searching for '{keyword}'...")
        tweets = client_x.search_recent_tweets(query=f"{keyword} -is:retweet", max_results=10)
        
        if tweets.data:
            for i, tweet in enumerate(tweets.data):
                if i >= limit: break
                
                with st.spinner(f"AI generating reply {i+1}..."):
                    prompt = f"Write a helpful, short reply to this: '{tweet.text}'. Mention this link: {LINK}"
                    response = groq_client.chat.completions.create(
                        model="llama3-8b-8192",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    reply = response.choices[0].message.content
                    
                    try:
                        client_x.create_tweet(text=reply, in_reply_to_tweet_id=tweet.id)
                        # إضافة للسجل
                        st.session_state.history.append({
                            "Time": datetime.now().strftime("%H:%M:%S"),
                            "Tweet ID": tweet.id,
                            "Status": "✅ Success"
                        })
                        st.success(f"Replied to {tweet.id}")
                        time.sleep(delay)
                    except Exception as e:
                        st.error(f"Error on {tweet.id}: {e}")
        else:
            st.warning("No tweets found.")

# --- عرض سجل العمليات ---
st.markdown("---")
st.subheader("📜 Activity Log")
if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.table(df.iloc[::-1]) # عرض الأحدث هو الأول
else:
    st.write("No activity yet. Press 'Run' to start.")
