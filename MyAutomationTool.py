import streamlit as st
import tweepy
import os

# 1. إعداد واجهة ستريمليت
st.title("🚀 لوحة تحكم الوحش (AgoraMAI)")
st.write("حكم في بوت تويتر ديالك من هنا")

# 2. جلب السوارت (فـ ستريمليت كيتسمى st.secrets)
try:
    api_key = st.secrets["TWITTER_API_KEY"]
    api_secret = st.secrets["TWITTER_API_SECRET"]
    access_token = st.secrets["TWITTER_ACCESS_TOKEN"]
    access_token_secret = st.secrets["TWITTER_ACCESS_TOKEN_SECRET"]
    smart_link = st.secrets["SMART_LINK"]

    # إعداد Tweepy
    client = tweepy.Client(
        consumer_key=api_key, consumer_secret=api_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )
    st.success("✅ السوارت خدامين مزيان!")
except Exception as e:
    st.error(f"❌ كاين مشكل فالسوارت: {e}")

# 3. زر النشر اليدوي
tweet_text = st.text_area("شنو بغيتي تنشر دابا؟", f"اكتشفوا الجديد هنا: {smart_link}")

if st.button("انشر دابا على تويتر 🚀"):
    try:
        client.create_tweet(text=tweet_text)
        st.balloons()
        st.success("✅ تم النشر بنجاح من ستريمليت!")
    except Exception as e:
        st.error(f"❌ وقع خطأ: {e}")
