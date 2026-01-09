import tweepy
import os

# جلب السوارت والرابط من GitHub Secrets
api_key = os.getenv("TWITTER_API_KEY")
api_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
smart_link = os.getenv("SMART_LINK")

# الاتصال بـ Twitter API v2 (النسخة اللي فيها Read and Write)
client = tweepy.Client(
    consumer_key=api_key,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

def post_tweet():
    try:
        # النص اللي غادي يتنشر أوتوماتيكياً
        message = (
            "🚀 اكتشفوا آخر مستجدات الذكاء الاصطناعي والتكنولوجيا الحصرية!\n\n"
            f"التفاصيل في الرابط التالي:\n{smart_link}\n\n"
            "#AI #TechNews #SmartLink #Automation"
        )
        
        # عملية النشر
        response = client.create_tweet(text=message)
        print(f"✅ ناضي! التويتة دازت بنجاح. ID: {response.data['id']}")
    except Exception as e:
        print(f"❌ وقع خطأ: {e}")

if __name__ == "__main__":
    post_tweet()
