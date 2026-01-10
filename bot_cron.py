import tweepy
import os
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

def run_bot():
    try:
        # 1. إعداد تويتر v2
        client = tweepy.Client(
            consumer_key=os.getenv("TWITTER_API_KEY"),
            consumer_secret=os.getenv("TWITTER_API_SECRET"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        )
        
        # 2. إعداد Gemini مع التصحيح النهائي
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        # استعملنا المسار الكامل للموديل لتفادي خطأ 404
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        smart_link = os.getenv("SMART_LINK")

        # 3. جلب خبر تقني عالمي
        res = requests.get("https://techcrunch.com/category/artificial-intelligence/", timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        # محاولة جلب أول عنوان خبر
        news_title = soup.find('h2').text.strip() if soup.find('h2') else "AI is reshaping the future of technology!"

        # 4. صياغة التويتة بذكاء واحترافية
        prompt = f"Write a viral, engaging tech tweet in English about: {news_title}. Use relevant emojis. Max 200 characters. Do not include links in the text."
        response = model.generate_content(prompt)
        ai_text = response.text.strip()
        
        # 5. النشر النهائي مع الرابط الخاص بك
        final_tweet = f"🚀 {ai_text}\n\nRead more 👇\n{smart_link}"
        
        client.create_tweet(text=final_tweet)
        print("✅ Auto-Tweet Posted Successfully to Tech Pulse!")
        
    except Exception as e:
        print(f"❌ Error during execution: {e}")

if __name__ == "__main__":
    run_bot()
