import os
import requests
from bs4 import BeautifulSoup
from groq import Groq
import streamlit as st

# 1. إعداد الواجهة
st.set_page_config(page_title="Global Tech Bot", page_icon="🤖")
st.title("🤖 Global Tech News Bot")

def get_config(key):
    if key in st.secrets: return st.secrets[key]
    return os.environ.get(key)

# 2. جلب الخبر بطريقة مضمونة (RSS Feed)
def get_tech_news():
    try:
        # استعملنا RSS حيت مستقر بزاف وما كيتأثرش بتبدال شكل الموقع
        url = "https://techcrunch.com/category/artificial-intelligence/feed/"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.content, 'xml') # كنستعملو xml هنا
        
        first_item = soup.find('item')
        if first_item:
            title = first_item.find('title').text
            # محاولة جلب الصورة من الوسائط
            img_url = "https://images.unsplash.com/photo-1677442136019-21780ecad995" # صورة افتراضية للذكاء الاصطناعي
            return title, img_url
        return "New Advances in AI", None
    except Exception as e:
        return "AI and Future Tech Updates", None

# 3. توليد المحتوى بـ Groq
def generate_content(title):
    api_key = get_config("GROQ_API_KEY")
    if not api_key: return None
    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": f"Create a catchy Telegram post about this: {title}. Use emojis and hashtags. Max 300 chars."}],
        )
        return completion.choices[0].message.content
    except: return None

# 4. النشر فـ تلغرام
def send_to_telegram(text, image_url):
    token = get_config("TELEGRAM_BOT_TOKEN")
    chat_id = get_config("TELEGRAM_CHAT_ID")
    link = get_config("SMART_LINK") or "https://dub.sh/technews24"
    
    caption = f"🚀 <b>GLOBAL TECH UPDATE</b>\n\n{text}\n\n🔗 <b>More:</b> {link}"
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    data = {"chat_id": chat_id, "photo": image_url, "caption": caption, "parse_mode": "HTML"}
    return requests.post(url, data=data).json()

# --- عرض الواجهة ---
st.info(f"Connected to: `{get_config('TELEGRAM_CHAT_ID')}`")

if st.button("
