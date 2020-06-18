import os
from dotenv import load_dotenv
import tweepy

load_dotenv()

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY", default="OOPS")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET", default="OOPS")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN", default="OOPS")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", default="OOPS")

# only if we invoke this function will these methods be called
# create a function under
# so we can call on it in our routes
def twitter_api_client():
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
    print(type(auth))
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    client = tweepy.API(auth)
    print(client)
    return client

if __name__ == "__main__":

    # this is the twitter api client
    client = twitter_api_client()
    #print("-----")
    #print(dir(client))
    #print("-----")

    #public_tweets = client.home_timeline()

    #for tweet in public_tweets:
    #    print(type(tweet), tweet.text)

    print("--------------")
    elon_tweets = client.user_timeline("elonmusk", tweet_mode="extended")
    for tweet in elon_tweets:
        print(type(tweet), tweet.full_text)