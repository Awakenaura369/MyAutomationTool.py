import os
import requests
from bs4 import BeautifulSoup
from groq import Groq

def get_config(key):
    # كنجيبو السوارت من GitHub Actions
    return os.environ.get(key)

def get_tech_news():
    """جلب عنوان الخبر وصورة المقال"""
    try:
        url = "https://techcrunch.com/category/artificial-intelligence/"
        res = requests.get(url, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        article = soup.find('article')
        title = article.find('h2').text.strip()
        img_tag = article.find('img')
        img_url = img_tag['src'] if img_tag else None
        return title, img_url
    except:
        return "AI Revolution Updates", None

def run_bot():
    try:
        title, img = get_tech_news()
        
        # إعداد Groq بالموديل الجديد
        client = Groq(api_key=get_config("GROQ_API_KEY"))
        prompt = f"Write a catchy viral news post about: '{title}'. Max 300 chars. Use emojis."
        
        chat = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        ai_msg = chat.choices[0].message.content
        
        # المعلومات ديال تلغرام
        token = get_config("TELEGRAM_BOT_TOKEN")
        chat_id = get_config("TELEGRAM_CHAT_ID")
        link = get_config("SMART_LINK") or "https://dub.sh/technews24"
        
        caption = f"🚀 <b>TECH UPDATE</b>\n\n{ai_msg}\n\n🔗 <b>More:</b> {link}"
        
        # إرسال الصورة إذا كانت موجودة، وإلا غير نص
        if img:
            api_url = f"https://api.telegram.org/bot{token}/sendPhoto"
            data = {"chat_id": chat_id, "photo": img, "caption": caption, "parse_mode": "HTML"}
        else:
            api_url = f"https://api.telegram.org/bot{token}/sendMessage"
            data = {"chat_id": chat_id, "text": caption, "parse_mode": "HTML"}
            
        requests.post(api_url, data=data)
        print("✅ Success!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_bot()
