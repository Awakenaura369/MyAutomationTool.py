import os
import requests
from bs4 import BeautifulSoup
from groq import Groq
import streamlit as st

def get_config(key):
    if key in st.secrets: return st.secrets[key]
    return os.environ.get(key)

def get_tech_news():
    """جلب الخبر مع رابط الصورة"""
    try:
        url = "https://techcrunch.com/category/artificial-intelligence/"
        res = requests.get(url, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # جلب أول مقال
        article = soup.find('article')
        title = article.find('h2').text.strip()
        
        # محاولة جلب رابط الصورة
        img_tag = article.find('img')
        img_url = img_tag['src'] if img_tag else None
        
        return title, img_url
    except:
        return "AI Revolutionizing Tech", None

def generate_with_groq(news_title):
    client = Groq(api_key=get_config("GROQ_API_KEY"))
    prompt = f"Write a short, viral Telegram post about: '{news_title}'. Max 300 chars. Use emojis."
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
    )
    return completion.choices[0].message.content

def send_to_telegram(message, image_url=None):
    token = get_config("TELEGRAM_BOT_TOKEN")
    chat_id = get_config("TELEGRAM_CHAT_ID")
    smart_link = get_config("SMART_LINK") or "https://dub.sh/technews24"
    full_text = f"🚀 <b>GLOBAL TECH UPDATE</b>\n\n{message}\n\n🔗 <b>Full Story:</b> {smart_link}"
    
    # إذا كانت كاينة صورة، كنصيفطو Photo، إلا ماكايناش كنصيفطو غير Message
    if image_url:
        url = f"https://api.telegram.org/bot{token}/sendPhoto"
        payload = {"chat_id": chat_id, "caption": full_text, "photo": image_url, "parse_mode": "HTML"}
    else:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": full_text, "parse_mode": "HTML"}
    
    return requests.post(url, data=payload).json()

# --- Streamlit Interface ---
st.title("📸 Tech News Bot + Images")

if st.button("🚀 Post with Image"):
    with st.spinner("Generating..."):
        title, img = get_tech_news()
        ai_msg = generate_with_groq(title)
        result = send_to_telegram(ai_msg, img)
        if result.get("ok"):
            st.success("✅ Sent with Image!")
            if img: st.image(img, caption="Sent Image")
            st.balloons()
