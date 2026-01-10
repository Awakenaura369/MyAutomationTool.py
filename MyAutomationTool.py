import os
import requests
from bs4 import BeautifulSoup
from groq import Groq
import sys

def get_tech_news():
    """جلب عنوان خبر تقني جديد"""
    try:
        url = "https://techcrunch.com/category/artificial-intelligence/"
        res = requests.get(url, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        # كنجيبو أول عنوان خبر (H2)
        news_element = soup.find('h2')
        return news_element.text.strip() if news_element else "AI & Future Technology"
    except Exception:
        return "Latest Global Tech Trends"

def generate_content_with_groq(news_title):
    """توليد بوست احترافي باستخدام Groq"""
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    prompt = (
        f"Write a short, viral, and professional Telegram post about this news: '{news_title}'. "
        "Include relevant emojis, use a bold headline, and keep it under 400 characters. "
        "Language: English."
    )
    
    completion = client.chat.completions.create(
        model="llama3-8b-8192", # الموديل السريع ديال Groq
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=200
    )
    return completion.choices[0].message.content

def send_to_telegram(message):
    """إرسال النتيجة النهائية للقناة"""
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    smart_link = os.environ.get("SMART_LINK", "https://dub.sh/technews24")
    
    full_text = f"{message}\n\n🔗 <b>Full Story:</b> {smart_link}"
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": full_text,
        "parse_mode": "HTML"
    }
    
    response = requests.post(url, data=payload)
    return response.json()

if __name__ == "__main__":
    print("🚀 Starting Bot...")
    
    # 1. جلب الخبر
    title = get_tech_news()
    print(f"📰 News Found: {title}")
    
    # 2. توليد المحتوى بـ Groq
    ai_message = generate_content_with_groq(title)
    
    # 3. النشر ف تلغرام
    result = send_to_telegram(ai_message)
    
    if result.get("ok"):
        print("✅ Success! Post sent to Telegram.")
    else:
        print(f"❌ Error: {result}")
