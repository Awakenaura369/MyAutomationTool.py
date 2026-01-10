import os
import requests
from bs4 import BeautifulSoup
from groq import Groq
import streamlit as st

# إعداد الواجهة لتجنب الشاشة السوداء
st.set_page_config(page_title="Global Tech Bot", page_icon="🤖")
st.title("🤖 Global Tech News Bot")

def get_config(key):
    if key in st.secrets: return st.secrets[key]
    return os.environ.get(key)

def get_tech_news():
    try:
        # استعمال RSS Feed لأنه أكثر استقراراً
        url = "https://techcrunch.com/category/artificial-intelligence/feed/"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.content, 'xml')
        first_item = soup.find('item')
        if first_item:
            title = first_item.find('title').text
            img_url = "https://images.unsplash.com/photo-1677442136019-21780ecad995"
            return title, img_url
        return "New AI Innovations", "https://images.unsplash.com/photo-1677442136019-21780ecad995"
    except:
        return "AI Tech Updates", "https://images.unsplash.com/photo-1677442136019-21780ecad995"

def generate_content(title):
    api_key = get_config("GROQ_API_KEY")
    if not api_key: return None
    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant", # الموديل الجديد
            messages=[{"role": "user", "content": f"Create a viral Telegram post about: {title}. Use emojis. Max 300 chars."}],
        )
        return completion.choices[0].message.content
    except: return None

def send_to_telegram(text, image_url):
    token = get_config("TELEGRAM_BOT_TOKEN")
    chat_id = get_config("TELEGRAM_CHAT_ID")
    link = get_config("SMART_LINK") or "https://dub.sh/technews24"
    caption = f"🚀 <b>GLOBAL TECH UPDATE</b>\n\n{text}\n\n🔗 <b>More:</b> {link}"
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    data = {"chat_id": chat_id, "photo": image_url, "caption": caption, "parse_mode": "HTML"}
    return requests.post(url, data=data).json()

# عرض الواجهة
st.info(f"Connected to: `{get_config('TELEGRAM_CHAT_ID')}`")

if st.button("🚀 Publish Manual Post Now"):
    with st.spinner("Processing..."):
        title, img = get_tech_news()
        ai_msg = generate_content(title)
        if ai_msg:
            result = send_to_telegram(ai_msg, img)
            if result.get("ok"):
                st.success("✅ Post sent to Telegram!")
                st.balloons()
            else: st.error(f"Error: {result}")

if __name__ == "__main__":
    if not os.environ.get("STREAMLIT_RUNTIME_CHECKS"):
        t, i = get_tech_news()
        m = generate_content(t)
        if m: send_to_telegram(m, i)
