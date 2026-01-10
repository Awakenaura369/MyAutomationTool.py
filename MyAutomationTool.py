import os
import requests
from bs4 import BeautifulSoup
from groq import Groq
import streamlit as st

# 1. دالة ذكية كتحضر السوارت من أي بلاصة (Streamlit أو GitHub)
def get_config(key):
    if key in st.secrets:
        return st.secrets[key]
    return os.environ.get(key)

def get_tech_news():
    """جلب آخر خبر تقني من TechCrunch"""
    try:
        url = "https://techcrunch.com/category/artificial-intelligence/"
        res = requests.get(url, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        news_element = soup.find('h2')
        return news_element.text.strip() if news_element else "AI & Tech Innovations"
    except:
        return "Latest Global Tech Trends"

def generate_with_groq(news_title):
    """توليد محتوى احترافي باستخدام محرك Groq"""
    api_key = get_config("GROQ_API_KEY")
    if not api_key:
        return "Error: No API Key found."
    
    client = Groq(api_key=api_key)
    
    prompt = (
        f"Create a short, engaging Telegram news post about: '{news_title}'. "
        "Use emojis, bold text for headings, and a professional tone. "
        "Max 400 characters. English language."
    )
    
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Groq Error: {str(e)}"

def send_to_telegram(message):
    """إرسال الخبر للقناة"""
    token = get_config("TELEGRAM_BOT_TOKEN")
    chat_id = get_config("TELEGRAM_CHAT_ID")
    smart_link = get_config("SMART_LINK") or "https://dub.sh/technews24"
    
    full_text = f"🚀 <b>GLOBAL TECH UPDATE</b>\n\n{message}\n\n🔗 <b>Full Story:</b> {smart_link}"
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": full_text, "parse_mode": "HTML"}
    
    try:
        res = requests.post(url, data=payload)
        return res.json()
    except Exception as e:
        return {"ok": False, "error": str(e)}

# --- واجهة Streamlit ---
st.title("🤖 Tech News Auto-Bot (Groq Edition)")
st.write(f"Connected to Channel: `{get_config('TELEGRAM_CHAT_ID')}`")

if st.button("🚀 Run Manual Post Now"):
    with st.spinner("Fetching news and generating content..."):
        news = get_tech_news()
        ai_msg = generate_with_groq(news)
        result = send_to_telegram(ai_msg)
        
        if result.get("ok"):
            st.success("✅ Post sent to Telegram successfully!")
            st.balloons()
            st.markdown(f"**Posted Content:**\n\n{ai_msg}")
        else:
            st.error(f"❌ Failed to post: {result}")

# هاد الجزء هو اللي كيخلي السكربت يخدم ف GitHub Actions أوتوماتيك
if __name__ == "__main__":
    # إذا كان السكربت خدام فـ GitHub Actions (ماشي فـ Streamlit)
    if not os.environ.get("STREAMLIT_RUNTIME_CHECKS"):
        print("🤖 Running Automation Task...")
        news_title = get_tech_news()
        content = generate_with_groq(news_title)
        send_to_telegram(content)
        print("✅ Task Finished.")
