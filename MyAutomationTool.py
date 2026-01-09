import streamlit as st
import tweepy
from groq import Groq
import time

# --- إعداد الصفحة ---
st.set_page_config(page_title="X AI Adsterra Bot", page_icon="🐦")

# --- جلب السوارت من Streamlit Secrets ---
try:
    # سوارت X (Twitter)
    bearer_token = st.secrets["X_BEARER_TOKEN"]
    api_key = st.secrets["X_API_KEY"]
    api_secret = st.secrets["X_API_SECRET"]
    access_token = st.secrets["X_ACCESS_TOKEN"]
    access_token_secret = st.secrets["X_ACCESS_TOKEN_SECRET"]
    # ساروت Groq والرابط
    groq_key = st.secrets["GROQ_API_KEY"]
    smart_link = st.secrets["SMART_LINK"]
except Exception as e:
    st.error("❌ السوارت ناقصين! تأكد أنك حطيتيهم فـ Streamlit Secrets.")
    st.stop()

# --- إعداد الـ Clients ---
client_x = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=api_key,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)
groq_client = Groq(api_key=groq_key)

st.title("🐦 X (Twitter) AI Traffic Bot")
st.markdown("---")

# --- واجهة التحكم ---
query = st.text_input("Keywords to search (e.g., 'money online' or 'football')", "make money online")
max_replies = st.slider("Number of replies per cycle", 1, 10, 3)

if st.button("🚀 Start AI Reply Cycle"):
    st.info(f"Searching for tweets about: {query}...")
    
    # البحث عن تويتات
    tweets = client_x.search_recent_tweets(query=f"{query} -is:retweet", max_results=10)
    
    if tweets.data:
        count = 0
        for tweet in tweets.data:
            if count >= max_replies: break
            
            with st.spinner(f"AI is thinking of a reply for tweet {count+1}..."):
                # صياغة الرد بـ Groq
                prompt = f"Someone tweeted: '{tweet.text}'. Write a natural, very short human-like reply (max 15 words) and suggest they check this for more: {smart_link}"
                
                completion = groq_client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[{"role": "user", "content": prompt}]
                )
                ai_reply = completion.choices[0].message.content
                
                # الرد على التويتة
                try:
                    client_x.create_tweet(text=ai_reply, in_reply_to_tweet_id=tweet.id)
                    st.success(f"✅ Replied to tweet ID: {tweet.id}")
                    count += 1
                    time.sleep(30) # وقت راحة باش ما يتسدش الحساب
                except Exception as e:
                    st.error(f"❌ Error: {e}")
    else:
        st.warning("No tweets found for this keyword.")
