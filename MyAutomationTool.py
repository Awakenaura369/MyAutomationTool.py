import streamlit as st
import tweepy
import requests
from bs4 import BeautifulSoup
from groq import Groq

# إعداد الصفحة
st.set_page_config(page_title="AgoraMAI - Control Room", page_icon="🚀")

# جلب السوارت من Streamlit Secrets
try:
    api_key = st.secrets["TWITTER_API_KEY"]
    api_secret = st.secrets["TWITTER_API_SECRET"]
    access_token = st.secrets["TWITTER_ACCESS_TOKEN"]
    access_token_secret = st.secrets["TWITTER_ACCESS_TOKEN_SECRET"]
    groq_key = st.secrets["GROQ_API_KEY"]
    smart_link = st.secrets["SMART_LINK"]

    client = tweepy.Client(
        consumer_key=api_key, consumer_secret=api_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )
    groq_client = Groq(api_key=groq_key)
except Exception as e:
    st.error("❌ تأكد من وضع جميع السوارت في Streamlit Secrets!")

st.title("🚀 AgoraMAI Control")

# اختيار النيش
niche = st.selectbox("Select Niche", ["Technology", "AI News", "Business", "World News"])

# دالة البحث
def find_news(topic):
    try:
        url = f"https://www.google.com/search?q={topic}+latest+news"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        # طريقة بسيطة لجب أول عنوان متاح
        title = soup.find('h3').text if soup.find('h3') else f"New update in {topic}"
        return title
    except:
        return f"Special report on {topic}"

if st.button("🔍 Find Trending News"):
    with st.spinner('Searching...'):
        news_found = find_news(niche)
        st.session_state['news'] = news_found
        st.success(f"Found: {news_found}")

# الجزء اللي فيه المشكل (تم تصليحه هنا)
if 'news' in st.session_state:
    st.subheader("📝 Final Tweet Draft:")
    
    try:
        # هنا استعملنا موديل كتر استقرارا وتأكدنا من الطريقة
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant", # جرب هاد الموديل الجديد
            messages=[
                {"role": "system", "content": "You are a helpful assistant that writes viral tweets in Arabic."},
                {"role": "user", "content": f"Write a viral Arabic tweet about this news: {st.session_state['news']}. Include emojis but NO hashtags and NO links."}
            ]
        )
        ai_text = completion.choices[0].message.content
        
        final_tweet = f"🚨 {ai_text}\n\n🔗 {smart_link}"
        edited_tweet = st.text_area("Edit before posting:", value=final_tweet, height=150)

        if st.button("🚀 Post to Twitter Now"):
            client.create_tweet(text=edited_tweet)
            st.balloons()
            st.success("✅ Published!")
    except Exception as e:
        st.error(f"AI Error: {e}") # باش نعرفو المشكل فين بالضبط
