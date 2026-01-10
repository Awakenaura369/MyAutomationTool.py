import tweepy
import os
import requests
from bs4 import BeautifulSoup
from groq import Groq

# Fetching Secrets
api_key = os.getenv("TWITTER_API_KEY")
api_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
smart_link = os.getenv("SMART_LINK")
groq_key = os.getenv("GROQ_API_KEY")

# Setup Clients
client = tweepy.Client(
    consumer_key=api_key, consumer_secret=api_secret,
    access_token=access_token, access_token_secret=access_token_secret
)
groq_client = Groq(api_key=groq_key)

def get_global_news():
    try:
        url = "https://techcrunch.com/category/artificial-intelligence/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_title = soup.find('h2').text.strip()
        return news_title
    except:
        return "Major breakthrough in AI and Future Technology"

def rewrite_with_ai(title):
    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a top tech influencer on X (Twitter)."},
                {"role": "user", "content": f"Write a viral, high-engagement English tweet about: {title}. Use emojis. Keep it concise. No hashtags."}
            ]
        )
        return completion.choices[0].message.content
    except:
        return f"Check out this massive update in the AI world! 🚀"

def run_automation():
    news = get_global_news()
    ai_post = rewrite_with_ai(news)
    final_message = f"🚨 {ai_post}\n\nFull details here 👇\n{smart_link}"
    
    try:
        client.create_tweet(text=final_message)
        print("✅ Global Tweet Posted Successfully!")
    except Exception as e:
        print(f"❌ Failed to post: {e}")

if __name__ == "__main__":
    run_automation()
