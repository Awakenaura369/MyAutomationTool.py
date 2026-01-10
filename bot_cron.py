import tweepy
import os
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
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
        
        # إعداد Gemini (التصحيح النهائي للـ 404)
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # جلب خبر تقني
        res = requests.get("https://techcrunch.com/category/artificial-intelligence/", timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        news_title = soup.find('h2').text.strip() if soup.find('h2') else "AI Innovation Update"

        # توليد البوست
        prompt = f"Write a viral short tweet about: {news_title}. Max 200 chars. Use emojis. No links."
        response = model.generate_content(prompt)
        ai_text = response.text.strip()
        
        # الرابط النهائي
        final_tweet = f"🚀 {ai_text}\n\nRead more 👇\n{os.environ['SMART_LINK']}"
        
        # النشر
        print(f"Post Content: {final_tweet}")
        pub = client.create_tweet(text=final_tweet)
        print(f"✅ DONE! Tweet ID: {pub.data['id']}")

    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_bot()
