import os
import requests
from bs4 import BeautifulSoup
from groq import Groq
import streamlit as st

# 1. إعداد الواجهة
st.set_page_config(page_title="Global Tech Bot", page_icon="🤖")
st.title("🤖 Global Tech News Bot")

def get_config(key):
    if key in st.secrets:
        return st.secrets[key]
    return os.environ.get(key)

# 2. جلب الخبر بطريقة RSS مستقرة
def get_tech_news():
    try:
        url = "https://techcrunch.com/category/artificial-intelligence/feed/"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.content, 'xml')
        
        first_item = soup.find('item')
        if first_item:
            title = first_item.find('title').text
            # صورة افتراضية احترافية للذكاء الاصطناعي
            img_url = "https://images.unsplash.com/photo-1677442136019-21780ecad995"
            return title, img_url
        return "Latest AI Breakthroughs", "https://images.unsplash.com/photo-1677442136019-21780ecad995"
    except Exception:
        return "AI and Future Tech Updates", "https://images.unsplash.com/photo-1677442136019-21780ecad995"

# 3. توليد المحتوى بـ Groq
def generate_content(title):
    api_key = get_config("GROQ_API_KEY")
    if not api_key:
        return None
    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": f"Create a catchy Telegram post about this news: {title}. Use emojis. Max 300 chars."}],
        )
        return completion.choices[0].message.content
    except Exception:
        return None

# 4. النشر فـ تلغرام
def send_to_telegram(text, image_url):
    token = get_config("TELEGRAM_BOT_TOKEN")
    chat_id = get_config("TELEGRAM_CHAT_ID")
    link = get_config("SMART_LINK") or "https://dub.sh/technews24"
    
    caption = f"🚀 <b>GLOBAL TECH UPDATE</b>\n\n{text}\n\n🔗 <b>More:</b> {link}"
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    data = {"chat_id": chat_id, "photo": image_url, "caption": caption, "parse_mode": "HTML"}
    try:
        return requests.post(url, data=data).json()
    except Exception as e:
        return {"ok": False, "error": str(e)}

# --- عرض الواجهة فـ Streamlit ---
target_channel = get_config("TELEGRAM_CHAT_ID") or "Not Connected"
st.info(f"Connected to: `{target_channel}`")

if st.button("🚀 Publish Manual Post Now"):
    with st.spinner("Generating with Groq..."):
        title, img = get_tech_news()
        ai_msg = generate_content(title)
        
        if ai_msg:
            result = send_to_telegram(ai_msg, img)
            if result.get("ok"):
                st.success("✅ Success! Check your Telegram Channel.")
                st.image(img, caption="Posted Image")
                st.balloons()
            else:
                st.error(f"Telegram Error: {result}")
        else:
            st.error("Groq generation failed. Please check your API Key.")

# الجزء الخاص بـ GitHub Actions
if __name__ == "__main__":
    if not os.environ.get("STREAMLIT_RUNTIME_CHECKS"):
        news_title, image = get_tech_news()
        message = generate_content(news_title)
        if message:
            send_to_telegram(message, image)
