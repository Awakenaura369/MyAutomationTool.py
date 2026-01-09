import tweepy
import requests
import feedparser
from groq import Groq
import os
import random

# جلب السوارت من GitHub Secrets
X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")
X_BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SMART_LINK = os.getenv("SMART_LINK")

# إعداد Twitter Client
client_x = tweepy.Client(
    bearer_token=X_BEARER_TOKEN,
    consumer_key=X_API_KEY,
    consumer_secret=X_API_SECRET,
    access_token=X_ACCESS_TOKEN,
    access_token_secret=X_ACCESS_TOKEN_SECRET
)

groq_client = Groq(api_key=GROQ_API_KEY)

def get_trending_news():
    # كنقلبو فمجال التكنولوجيا كمثال
    url = "https://news.google.com/rss/search?q=technology+AI&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(url)
    if feed.entries:
        return random.choice(feed.entries[:10])
    return None

def generate_tweet(news_title):
    try:
        # استعملنا الموديل المستقر llama3-8b-8192
        prompt = f"Summarize this news in one viral engaging tweet with emojis: '{news_title}'. Keep it under 200 characters."
        chat = groq_client.chat.completions.create(
            model="llama3-8b-8192", 
            messages=[{"role": "user", "content": prompt}]
        )
        return chat.choices[0].message.content
    except:
        return f"🚨 News Alert: {news_title}"

def run_automation():
    news_item = get_trending_news()
    if news_item:
        ai_content = generate_tweet(news_item.title)
        final_tweet = f"{ai_content}\n\n🔗 {SMART_LINK}"
        
        try:
            client_x.create_tweet(text=final_tweet)
            print(f"✅ Success: {news_item.title}")
        except Exception as e:
            print(f"❌ Twitter Error: {e}")
    else:
        print("⚠️ No news found.")

if __name__ == "__main__":
    run_automation()
