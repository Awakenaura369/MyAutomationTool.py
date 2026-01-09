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

# واجهة المستخدم
st.title("🚀 AgoraMAI Control")

# 1. اختيار النيش (Niche)
niche = st.selectbox("Select Niche", ["Technology", "AI News", "Finance", "Health"])

# 2. دالة البحث عن الأخبار
def find_news(topic):
    try:
        url = f"https://www.google.com/search?q={topic}+news&tbm=nws"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find('div', str={'class': 'vv779b'}).text # تبسيط للبحث
        return title if title else "No news found"
    except:
        return f"Latest updates in {topic} field"

if st.button("🔍 Find Trending News"):
    with st.spinner('Searching for news...'):
        news_found = find_news(niche)
        st.session_state['news'] = news_found
        st.success(f"Found: {news_found}")

# 3. إعداد مسودة التويتة بالذكاء الاصطناعي
if 'news' in st.session_state:
    st.subheader("📝 Final Tweet Draft:")
    
    # طلب إعادة الصياغة من Groq
    completion = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": f"Create a viral tweet in Arabic about: {st.session_state['news']}. Add emojis. Don't include the link yet."}],
        model="llama3-8b-8192",
    )
    ai_text = completion.choices[0].message.content
    
    final_tweet = f"🚨 {ai_text}\n\n🔗 {smart_link}"
    edited_tweet = st.text_area("Edit your tweet before posting:", value=final_tweet, height=150)

    # 4. زر النشر النهائي
    if st.button("🚀 Post to Twitter Now"):
        try:
            client.create_tweet(text=edited_tweet)
            st.balloons()
            st.success("✅ Published successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")
st.caption("Auto-Pilot mode is handled by GitHub Actions.")
