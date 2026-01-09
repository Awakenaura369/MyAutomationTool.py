import streamlit as st
import tweepy
from groq import Groq
import time
import pandas as pd

# --- Page Config ---
st.set_page_config(page_title="AI Traffic Master v2", page_icon="🚀", layout="wide")

# --- Get Secrets ---
try:
    X_CREDS = {
        "bearer_token": st.secrets["X_BEARER_TOKEN"],
        "api_key": st.secrets["X_API_KEY"],
        "api_secret": st.secrets["X_API_SECRET"],
        "access_token": st.secrets["X_ACCESS_TOKEN"],
        "access_token_secret": st.secrets["X_ACCESS_TOKEN_SECRET"]
    }
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    LINK = st.secrets["SMART_LINK"]
except Exception as e:
    st.error("❌ Secrets are missing in Streamlit Settings!")
    st.stop()

# --- Clients ---
client_x = tweepy.Client(
    bearer_token=X_CREDS["bearer_token"],
    consumer_key=X_CREDS["api_key"],
    consumer_secret=X_CREDS["api_secret"],
    access_token=X_CREDS["access_token"],
    access_token_secret=X_CREDS["access_token_secret"]
)
groq_client = Groq(api_key=GROQ_KEY)

st.title("🌐 Global AI Traffic Engine")
keyword = st.text_input("Enter Keyword (English)", "how to make money online")
replies_count = st.slider("Number of Manual Replies", 1, 5, 2)

if st.button("🔥 Run Manual Cycle"):
    tweets = client_x.search_recent_tweets(query=f"{keyword} -is:retweet", max_results=10)
    if tweets.data:
        for i, tweet in enumerate(tweets.data):
            if i >= replies_count: break
            prompt = f"Write a helpful, very short English reply to: '{tweet.text}'. Recommend this: {LINK}"
            res = groq_client.chat.completions.create(model="llama3-8b-8192", messages=[{"role": "user", "content": prompt}])
            reply = res.choices[0].message.content
            client_x.create_tweet(text=reply, in_reply_to_tweet_id=tweet.id)
            st.success(f"✅ Replied to tweet {i+1}")
            time.sleep(30)
    else:
        st.warning("No tweets found.")
