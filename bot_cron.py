import tweepy
import os
import requests
from bs4 import BeautifulSoup
from groq import Groq
import sys

def run_bot():
    try:
        # إعداد تويتر
        client = tweepy.Client(
            consumer_key=os.environ["TWITTER_API_KEY"],
            consumer_secret=os.environ["TWITTER_API_SECRET"],
            access_token=os.environ["TWITTER_ACCESS_TOKEN"],
            access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
        )
        
        # إعداد Groq
        groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])
        
        # جلب خبر تقني
        res = requests.get("https://techcrunch.com/category/artificial-intelligence/", timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        news_title = soup.find('h2').text.strip() if soup.find('h2') else "Tech Innovation Update"

        # توليد البوست بـ Groq (Llama 3)
        completion = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": f"Write a viral short tweet about: {news_title}. Max 200 chars. Use emojis. No links."}]
        )
        ai_text = completion.choices[0].message.content.strip()
        
        # الرابط النهائي
        final_tweet = f"🚀 {ai_text}\n\nRead more 👇\n{os.environ['SMART_LINK']}"
        
        # النشر
        print(f"Posting: {final_tweet}")
        pub = client.create_tweet(text=final_tweet)
        print(f"✅ DONE! Tweet ID: {pub.data['id']}")

    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_bot()
