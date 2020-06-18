import os
from dotenv import load_dotenv
import tweepy
import pandas as pd
import requests

load_dotenv()

#----- this model works for followers ---

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY", default="OOPS")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET", default="OOPS")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN", default="OOPS")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", default="OOPS")

# only if we invoke this function will these methods be called
# create a function under
# so we can call on it in our routes
def twitter_api_client():
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
    # print(type(auth))
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    # print(client)
    return api

api = twitter_api_client()

# define the users screen name (Eventually API Key)
at_name="nickpgeorge"

# specify number of items (followers) to return, MAX 180 every 15 mins for free users
# set to two for testing purposes
items = 2

# collect followers
followers = tweepy.Cursor(api.followers, screen_name=at_name).items(items)

# Collect followers list
followers_list = [follower.screen_name for follower in followers]

df = pd.DataFrame(followers_list)

print(df)



#if __name__ == "__main__":
#
#    # this is the twitter api client
#    client = twitter_api_client()
#
#    print("--------------")
#    my_tweets = client.user_timeline("nickpgeorge", tweet_mode="extended")
#    for tweet in my_tweets:
#        print(type(tweet), tweet.full_text)
#
#    print("--------------")
#    my_followers = client.followers("nickpgeorge")
#    df = pd.DataFrame(my_followers)
#    print(df)
