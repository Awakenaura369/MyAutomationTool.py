import tweepy
import os
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

def run_bot():
    # 1. إعداد تويتر
    client = tweepy.Client(
        consumer_key=os.getenv("TWITTER_API_KEY"),
        consumer_secret=os.getenv("TWITTER_API_SECRET"),
        access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
        access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    )
    
    # 2. إعداد Gemini
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')
    smart_link = os.getenv("SMART_LINK")

    # 3. جلب خبر عالمي بالإنجليزية
    try:
        res = requests.get("https://techcrunch.com/category/artificial-intelligence/", timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        news_title = soup.find('h2').text.strip()
    except:
        news_title = "AI innovation is accelerating globally!"

    # 4. صياغة التويتة بـ Gemini
    prompt = f"Write a viral tech influencer tweet in English about: {news_title}. Use emojis. Max 200 chars. No links."
    response = model.generate_content(prompt)
    ai_text = response.text.strip()
    
    # 5. النشر النهائي
    final_tweet = f"🚀 {ai_text}\n\nFull Story 👇\n{smart_link}"
    
    try:
        client.create_tweet(text=final_tweet)
        print("✅ Global Auto-Tweet Posted!")
    except Exception as e:
        print(f"❌ Tweet failed: {e}")

if __name__ == "__main__":
    run_bot()
