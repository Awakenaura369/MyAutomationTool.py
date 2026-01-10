import tweepy
import os
import requests
from bs4 import BeautifulSoup
from groq import Groq

def run_bot():
    # جلب السوارت من GitHub Secrets
    client = tweepy.Client(
        consumer_key=os.getenv("TWITTER_API_KEY"),
        consumer_secret=os.getenv("TWITTER_API_SECRET"),
        access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
        access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    )
    groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    smart_link = os.getenv("SMART_LINK")

    # جلب خبر
    try:
        res = requests.get("https://techcrunch.com/category/artificial-intelligence/", timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        news_title = soup.find('h2').text.strip()
    except:
        news_title = "The future of AI is evolving fast!"

    # صياغة بالذكاء الاصطناعي
    completion = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": f"Write a viral English tweet about: {news_title}. Use emojis. Max 200 chars."}]
    )
    ai_text = completion.choices[0].message.content
    
    # النشر
    client.create_tweet(text=f"🚨 {ai_text}\n\nMore info: {smart_link}")
    print("✅ Auto-Tweet Posted!")

if __name__ == "__main__":
    run_bot()
