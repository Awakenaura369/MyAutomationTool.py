import tweepy
import os
import requests
from bs4 import BeautifulSoup
from groq import Groq
import sys

def run_global_bot():
    try:
        # تويتر
        client = tweepy.Client(
            consumer_key=os.environ["TWITTER_API_KEY"],
            consumer_secret=os.environ["TWITTER_API_SECRET"],
            access_token=os.environ["TWITTER_ACCESS_TOKEN"],
            access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
        )
        
        # Groq بالموديل الجديد
        groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])
        
        # جلب خبر عالمي من TechCrunch
        res = requests.get("https://techcrunch.com/category/artificial-intelligence/", timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        news_title = soup.find('h2').text.strip() if soup.find('h2') else "Innovation Alert"

        # توليد النص بـ Llama 3.1
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": f"Create a viral English tweet for a global audience about: {news_title}. Use emojis and hashtags. Max 200 chars."}]
        )
        ai_text = completion.choices[0].message.content.strip()
        
        final_tweet = f"🚀 {ai_text}\n\nCheck it out 👇\n{os.environ['SMART_LINK']}"
        
        # النشر
        client.create_tweet(text=final_tweet)
        print("✅ Global Tweet Posted Successfully!")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_global_bot()
