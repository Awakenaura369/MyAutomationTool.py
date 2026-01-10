import tweepy
import os
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

def run_bot():
    try:
        # 1. إعداد تويتر (تأكد من الصلاحيات Read and Write في Twitter Developer)
        client = tweepy.Client(
            consumer_key=os.environ["TWITTER_API_KEY"],
            consumer_secret=os.environ["TWITTER_API_SECRET"],
            access_token=os.environ["TWITTER_ACCESS_TOKEN"],
            access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
        )
        
        # 2. إعداد Gemini (الطريقة الأضمن)
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        # استعملنا الموديل ديريكت بدون بادئة 'models/' لتفادي خطأ 404
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 3. جلب الخبر
        res = requests.get("https://techcrunch.com/category/artificial-intelligence/", timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        news_title = soup.find('h2').text.strip() if soup.find('h2') else "AI is evolving fast!"

        # 4. توليد النص
        prompt = f"Write a short viral tweet in English about: {news_title}. Max 200 chars. Use emojis. No links."
        response = model.generate_content(prompt)
        ai_text = response.text.strip()
        
        # 5. النشر (الرابط)
        smart_link = os.environ["SMART_LINK"]
        final_tweet = f"🚀 {ai_text}\n\nRead more 👇\n{smart_link}"
        
        # محاولة النشر وطباعة النتيجة
        response = client.create_tweet(text=final_tweet)
        if response.data:
            print(f"✅ SUCCESS: Tweet posted! ID: {response.data['id']}")
        else:
            print("⚠️ WARNING: Tweet might not have posted.")

    except Exception as e:
        print(f"❌ CRITICAL ERROR: {str(e)}")
        # هاد السطر غايخلي GitHub يعطيك علامة حمراء إلا فشل بالصح
        raise e 

if __name__ == "__main__":
    run_bot()
