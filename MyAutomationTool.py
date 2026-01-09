import streamlit as st
import tweepy
from groq import Groq
import time
import pandas as pd
from datetime import datetime

# --- إعدادات الصفحة والستايل ---
st.set_page_config(page_title="X AI Traffic Pro", page_icon="💎", layout="wide")

# إضافة لمسة جمالية بـ CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #1DA1F2; color: white; border: none; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- جلب السوارت ---
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
    st.error("❌ Secrets are missing! Check Streamlit Settings.")
    st.stop()

# --- تهيئة العملاء ---
@st.cache_resource
def init_clients():
    client_x = tweepy.Client(
        bearer_token=X_CREDS["bearer_token"],
        consumer_key=X_CREDS["api_key"],
        consumer_secret=X_CREDS["api_secret"],
        access_token=X_CREDS["access_token"],
        access_token_secret=X_CREDS["access_token_secret"]
    )
    groq_client = Groq(api_key=GROQ_KEY)
    return client_x, groq_client

client_x, groq_client = init_clients()

# --- واجهة المستخدم ---
st.title("💎 X AI Traffic Control Pro")
st.markdown("---")

# Session state لتخزين السجل
if 'history' not in st.session_state:
    st.session_state.history = []

# تقسيم الصفحة
col_stats, col_control = st.columns([1, 2])

with col_stats:
    st.subheader("📊 Live Stats")
    st.metric(label="Total Replies Sent", value=len(st.session_state.history))
    st.info(f"🔗 Target: {LINK[:30]}...")

with col_control:
    st.subheader("⚙️ Control Hub")
    col1, col2 = st.columns(2)
    with col1:
        keyword = st.text_input("🎯 Keyword", "make money online")
    with col2:
        replies_count = st.slider("🚀 Replies", 1, 10, 2)
    
    if st.button("🚀 Launch Automation Cycle"):
        with st.status("Running AI Cycle...", expanded=True) as status:
            st.write("🔍 Searching for tweets...")
            tweets = client_x.search_recent_tweets(query=f"{keyword} -is:retweet", max_results=10)
            
            if tweets.data:
                for i, tweet in enumerate(tweets.data):
                    if i >= replies_count: break
                    st.write(f"🤖 AI generating reply for tweet {i+1}...")
                    
                    prompt = f"Write a helpful, short human-like reply to: '{tweet.text}'. Mention this: {LINK}"
                    res = groq_client.chat.completions.create(model="llama3-8b-8192", messages=[{"role": "user", "content": prompt}])
                    reply = res.choices[0].message.content
                    
                    try:
                        client_x.create_tweet(text=reply, in_reply_to_tweet_id=tweet.id)
                        st.session_state.history.append({
                            "Time": datetime.now().strftime("%H:%M:%S"),
                            "Keyword": keyword,
                            "Status": "✅ Success"
                        })
                        st.write(f"✅ Posted reply to ID: {tweet.id}")
                        time.sleep(30)
                    except Exception as e:
                        st.error(f"Error: {e}")
                status.update(label="Cycle Complete!", state="complete")
            else:
                st.warning("No tweets found.")

# --- عرض سجل العمليات بستايل ناضي ---
st.markdown("---")
st.subheader("📜 Activity Log")
if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.table(df.iloc[::-1])
else:
    st.write("No activity recorded yet.")
