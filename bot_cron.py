import tweepy
from groq import Groq
import os
import time
import random

def run_bot():
    try:
        # Get Secrets from Environment
        client_x = tweepy.Client(
            bearer_token=os.environ["X_BEARER_TOKEN"],
            consumer_key=os.environ["X_API_KEY"],
            consumer_secret=os.environ["X_API_SECRET"],
            access_token=os.environ["X_ACCESS_TOKEN"],
            access_token_secret=os.environ["X_ACCESS_TOKEN_SECRET"]
        )
        groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])
        link = os.environ["SMART_LINK"]

        queries = ["passive income ideas", "best side hustles", "remote work tips"]
        search_query = f"{random.choice(queries)} -is:retweet"
        
        tweets = client_x.search_recent_tweets(query=search_query, max_results=5)
        if tweets.data:
            for tweet in tweets.data[:2]: # Reply to 2 tweets max per hour
                prompt = f"Respond to this tweet in a helpful, short, human-like way in English: '{tweet.text}'. Suggest this link: {link}"
                res = groq_client.chat.completions.create(model="llama3-8b-8192", messages=[{"role": "user", "content": prompt}])
                reply = res.choices[0].message.content
                client_x.create_tweet(text=reply, in_reply_to_tweet_id=tweet.id)
                print(f"✅ Replied to {tweet.id}")
                time.sleep(60)
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_bot()
