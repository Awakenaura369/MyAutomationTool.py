import tweepy
import requests
import feedparser
from groq import Groq
import os
import random

# السوارت من GitHub Secrets
X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")
X_BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SMART_LINK = os.getenv("SMART_LINK")

client_x = tweepy.Client(
    bearer_token=X_BEARER_TOKEN,
    consumer_key=X_API_KEY,
    consumer_secret=X_API_SECRET,
    access_token=X_ACCESS_TOKEN,
    access_token_secret=X_ACCESS_TOKEN_SECRET
)

groq_client = Groq(api_key=GROQ_API_KEY)

# دالة كتقلب على أخبار تريند (Google News Tech)
def get_trending_news():
    url = "https://news.google.com/rss/search?q=technology+AI&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(url)
    if feed.entries:
        item = random.choice(feed.entries[:10]) # كياخد خبر من الـ 10 اللولين
        return {"title": item.title, "link": item.link}
    return None

# دالة إعادة الصياغة بالذكاء الاصطناعي
def rewrite_with_ai(news_title):
    prompt = f"""
    Rewrite this news headline into a viral, engaging tweet: '{news_title}'.
    - Use professional emojis.
    - Make it sound like a quick update.
    - End with a call to action like 'Check this out:'.
    - Language: English.
    """
    chat = groq_client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role": "user", "content": prompt}]
    )
    return chat.choices[0].message.content

def run_automation():
    news = get_trending_news()
    if news:
        ai_content = rewrite_with_ai(news['title'])
        # هنا كنحطو الرابط ديالك نتا (Smart Link)
        final_tweet = f"{ai_content}\n\n🔗 {SMART_LINK}"
        
        try:
            client_x.create_tweet(text=final_tweet)
            print(f"✅ Posted Trend: {news['title']}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_automation()
