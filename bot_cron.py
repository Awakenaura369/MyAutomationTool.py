import tweepy
import requests
from bs4 import BeautifulSoup
import random
from groq import Groq
import os

# جلب السوارت من GitHub Secrets (هادو كيهزهم GitHub Actions أوتوماتيكياً)
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

def get_blog_posts(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        for a in soup.find_all('a', href=True):
            if '/20' in a['href'] and len(a.text.strip()) > 10:
                links.append({"title": a.text.strip(), "url": a['href']})
        return links
    except: return []

def generate_tweet(title):
    prompt = f"Write an engaging tweet about: '{title}'. Add emojis. End with 'Read more:'"
    chat = groq_client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role": "user", "content": prompt}]
    )
    return chat.choices[0].message.content

def run_automation():
    posts = get_blog_posts(SMART_LINK)
    if posts:
        post = random.choice(posts)
        tweet_content = generate_tweet(post['title'])
        final_text = f"{tweet_content}\n\n{post['url']}"
        
        try:
            client_x.create_tweet(text=final_text)
            print(f"✅ Success: Posted {post['title']}")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("⚠️ No posts found.")

if __name__ == "__main__":
    run_automation()
