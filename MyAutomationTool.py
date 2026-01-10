import os
import requests
from bs4 import BeautifulSoup
from groq import Groq
import streamlit as st

# 1. إعداد الواجهة (باش ما تبقاش كحلة)
st.set_page_config(page_title="Tech Bot Dashboard", page_icon="🤖")
st.title("🤖 Global Tech News Bot")
st.sidebar.header("Configuration")

# 2. جلب السوارت
def get_config(key):
    if key in st.secrets: return st.secrets[key]
    return os.environ.get(key)

# 3. جلب الخبر والصورة
def get_tech_news():
    try:
        url = "https://techcrunch.com/category/artificial-intelligence/"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        article = soup.find('article')
        title = article.find('h2').text.strip()
        img_tag = article.find('img')
        img_url = img_tag['src'] if img_tag else None
        return title, img_url
    except Exception as e:
        st.error(f"Error fetching news: {e}")
        return "New Tech Update", None

# 4. توليد المحتوى بـ Groq
def generate_content(title):
    api_key = get_config("GROQ_API_KEY")
    if not api_key:
        st.warning("⚠️ GROQ_API_KEY is missing!")
        return None
    
    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant", # الموديل الجديد والشغال
            messages=[{"role": "user", "content": f"Summarize this tech news into a viral Telegram post with emojis: {title}. Max 300 chars."}],
            temperature=0.7
        )
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"Groq Error: {e}")
        return None

# 5. النشر فـ تلغرام
def send_to_telegram(text, image_url):
    token = get_config("TELEGRAM_BOT_TOKEN")
    chat_id = get_config("TELEGRAM_CHAT_ID")
    link = get_config("SMART_LINK") or "https://dub.sh/technews24"
    
    caption = f"🚀 <b>TECH UPDATE</b>\n\n{text}\n\n🔗 <b>More:</b> {link}"
    
    if image_url:
        url = f"https://api.telegram.org/bot{token}/sendPhoto"
        data = {"chat_id": chat_id, "photo": image_url, "caption": caption, "parse_mode": "HTML"}
    else:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {"chat_id": chat_id, "text": caption, "parse_mode": "HTML"}
    
    return requests.post(url, data=data).json()

# --- عرض الواجهة ---
chat_id = get_config("TELEGRAM_CHAT_ID")
st.info(f"Connected to: `{chat_id}`")

if st.button("🚀 Publish Manual Post Now"):
    with st.spinner("Processing..."):
        title, img = get_tech_news()
        ai_msg = generate_content(title)
        
        if ai_msg:
            result = send_to_telegram(ai_msg, img)
            if result.get("ok"):
                st.success("✅ Published Successfully!")
                if img: st.image(img)
                st.balloons()
            else:
                st.error(f"Telegram Error: {result}")

# هاد السطر مهم لـ GitHub Actions
if __name__ == "__main__":
    if not os.environ.get("STREAMLIT_RUNTIME_CHECKS"):
        title, img = get_tech_news()
        ai_msg = generate_content(title)
        if ai_msg:
            send_to_telegram(ai_msg, img)
