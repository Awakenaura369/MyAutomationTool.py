import streamlit as st
import tweepy
import requests
import feedparser
from groq import Groq
import random

# 1. جلب السوارت من Streamlit Secrets
X_API_KEY = st.secrets["X_API_KEY"]
X_API_SECRET = st.secrets["X_API_SECRET"]
X_ACCESS_TOKEN = st.secrets["X_ACCESS_TOKEN"]
X_ACCESS_TOKEN_SECRET = st.secrets["X_ACCESS_TOKEN_SECRET"]
X_BEARER_TOKEN = st.secrets["X_BEARER_TOKEN"]
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
SMART_LINK = st.secrets["SMART_LINK"]

# 2. إعداد الاتصال بـ Twitter (X)
client_x = tweepy.Client(
    bearer_token=X_BEARER_TOKEN,
    consumer_key=X_API_KEY,
    consumer_secret=X_API_SECRET,
    access_token=X_ACCESS_TOKEN,
    access_token_secret=X_ACCESS_TOKEN_SECRET
)

# 3. إعداد Groq AI
groq_client = Groq(api_key=GROQ_API_KEY)

# دالة لجلب الأخبار التريند
def get_trending_news(query="technology"):
    # كنستعملو Google News RSS كأفضل مصدر مجاني
    url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(url)
    return feed.entries[:15] # كيهز أول 15 خبر

# دالة صناعة التغريدة بذكاء اصطناعي (تم إصلاح الموديل هنا)
def generate_tweet(news_title):
    try:
        # استعملنا llama3-8b-8192 حيت هو المستقر حالياً
        prompt = f"Summarize this news in one viral engaging tweet with emojis: '{news_title}'. Keep it under 200 characters. End with a call to action."
        chat = groq_client.chat.completions.create(
            model="llama3-8b-8192", 
            messages=[{"role": "user", "content": prompt}]
        )
        return chat.choices[0].message.content
    except Exception as e:
        # إلا وقع مشكل فـ AI كيرجع العنوان الأصلي باش الخدمة ما توقفش
        return f"🚨 News Alert: {news_title}"

# 4. واجهة التطبيق Streamlit
st.set_page_config(page_title="AI Viral Poster", page_icon="🔥")
st.title("🔥 AI Trend & Viral Poster")
st.markdown(f"**Target Link:** `{SMART_LINK}`")

# اختيار المجال
niche = st.selectbox("Select Your Niche:", ["Technology", "AI", "Business", "Health", "Gaming", "Money"])

if st.button("🔍 Find Trending News"):
    news_list = get_trending_news(niche)
    if news_list:
        # اختيار خبر عشوائي من اللي لقينا
        item = random.choice(news_list)
        st.success(f"Found: {item.title}")
        
        # صناعة التويتة
        with st.spinner('AI is writing the tweet...'):
            tweet_text = generate_tweet(item.title)
            final_content = f"{tweet_text}\n\n🔗 {SMART_LINK}"
            
        st.subheader("📝 Final Tweet Draft:")
        st.info(final_content)
        
        # زر النشر النهائي
        if st.button("🚀 Post to Twitter Now"):
            try:
                client_x.create_tweet(text=final_content)
                st.balloons()
                st.success("✅ Tweet published successfully!")
            except Exception as e:
                st.error(f"Twitter Error: {e}")
    else:
        st.warning("No news found. Try another topic.")

st.divider()
st.caption("Auto-Pilot mode is handled by GitHub Actions.")
