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

# إعداد Twitter Client
client_x = tweepy.Client(
    bearer_token=X_BEARER_TOKEN,
    consumer_key=X_API_KEY,
    consumer_secret=X_API_SECRET,
    access_token=X_ACCESS_TOKEN,
    access_token_secret=X_ACCESS_TOKEN_SECRET
)

groq_client = Groq(api_key=GROQ_API_KEY)

# دالة لجلب الأخبار التريند
def get_trending_news(query="technology"):
    url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(url)
    return feed.entries[:10]

# دالة صناعة المحتوى بـ AI
def generate_tweet(news_title):
    prompt = f"Rewrite this news headline into a viral, engaging tweet: '{news_title}'. Use emojis and a call to action. Language: English."
    chat = groq_client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role": "user", "content": prompt}]
    )
    return chat.choices[0].message.content

# واجهة تطبيق Streamlit
st.set_page_config(page_title="AI Trend Poster", page_icon="🚀")
st.title("🚀 AI Trend Poster Control")
st.write(f"Link being promoted: `{SMART_LINK}`")

# اختيار المجال (Niche)
topic = st.selectbox("Choose a Topic:", ["Technology", "AI", "Business", "Health", "Gaming"])

if st.button("Search for Trending News"):
    news_list = get_trending_news(topic)
    if news_list:
        selected_news = random.choice(news_list)
        st.subheader("🔥 Latest News Found:")
        st.write(f"**Original:** {selected_news.title}")
        
        # صناعة المحتوى
        with st.spinner('AI is crafting your tweet...'):
            tweet_content = generate_tweet(selected_news.title)
            final_tweet = f"{tweet_content}\n\n🔗 {SMART_LINK}"
            
        st.subheader("📝 Draft for Twitter:")
        st.info(final_tweet)
        
        # زر النشر
        if st.button("Confirm & Post to X"):
            try:
                client_x.create_tweet(text=final_tweet)
                st.success("✅ Success! Check your Twitter account.")
            except Exception as e:
                st.error(f"Error publishing: {e}")
    else:
        st.warning("No news found for this topic.")
