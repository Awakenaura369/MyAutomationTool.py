import os
import requests
from bs4 import BeautifulSoup
from groq import Groq

def send_telegram_msg(text):
    """وظيفة إرسال الرسالة لتلغرام"""
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id, 
        "text": text, 
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    try:
        res = requests.post(url, data=payload)
        return res.json()
    except Exception as e:
        print(f"Telegram Error: {e}")
        return None

def get_tech_news():
    """جلب خبر جديد من TechCrunch"""
    try:
        res = requests.get("https://techcrunch.com/category/artificial-intelligence/", timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        news_element = soup.find('h2')
        return news_element.text.strip() if news_element else "AI Revolution"
    except:
        return "New Innovations in AI"

def run_auto_bot():
    try:
        # 1. إعداد Groq (المحرك المفضل عندك)
        client = Groq(api_key=os.environ["GROQ_API_KEY"])
        
        # 2. جلب الخبر
        news_title = get_tech_news()

        # 3. توليد المحتوى بـ Groq
        prompt = f"Write a catchy, professional viral news post about: {news_title}. Use emojis. Target: Tech enthusiasts. Max 400 chars."
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192", # موديل سريع واقتصادي ف Groq
        )
        ai_text = chat_completion.choices[0].message.content
        
        # 4. الرابط الذكي ديالك
        smart_link = os.environ["SMART_LINK"]
        
        # 5. التنسيق النهائي
        final_post = (
            f"🚀 <b>TECH INSIDER UPDATE</b>\n\n"
            f"{ai_text}\n\n"
            f"🔗 <b>Read More:</b> {smart_link}"
        )

        # 6. النشر ف تلغرام
        status = send_telegram_msg(final_post)
        if status and status.get("ok"):
            print("✅ Successfully posted to Telegram via Groq!")
        else:
            print(f"❌ Failed: {status}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_auto_bot()
