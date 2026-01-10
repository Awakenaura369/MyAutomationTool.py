import tweepy
import os
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

def run_bot():
    try:
        # إعداد تويتر بـ v2
        client = tweepy.Client(
            consumer_key=os.getenv("TWITTER_API_KEY"),
            consumer_secret=os.getenv("TWITTER_API_SECRET"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        )
        
        # إعداد Gemini
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-1.5-flash')
        smart_link = os.getenv("SMART_LINK")

        # جلب خبر
        res = requests.get("https://techcrunch.com/category/artificial-intelligence/", timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        news_title = soup.find('h2').text.strip()

        # صياغة التويتة
        prompt = f"Write a viral tech tweet in English about: {news_title}. Use emojis. Max 200 chars."
        response = model.generate_content(prompt)
        ai_text = response.text.strip()
        
        # النشر
        client.create_tweet(text=f"🚀 {ai_text}\n\nFull Story 👇\n{smart_link}")
        print("✅ Auto-Tweet Posted Successfully!")
        
    except Exception as e:
        print(f"❌ Error during execution: {e}")

if __name__ == "__main__":
    run_bot()
