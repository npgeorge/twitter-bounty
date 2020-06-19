import os
from dotenv import load_dotenv
import tweepy
import pandas as pd
import requests
import time

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
screen_name="nickpgeorge"

def df():
    # items is how many followers you want in your df
    items = 3

    # initiate lists and append
    follower_list = []
    for follower in tweepy.Cursor(api.followers, screen_name=screen_name).items(items):
        follower = follower.screen_name
        follower_list.append(follower)

    ids_list = []
    for ids in tweepy.Cursor(api.followers_ids, screen_name=screen_name).items(items):
        ids_list.append(ids)
    
    name_list = []
    for name in tweepy.Cursor(api.followers, screen_name=screen_name).items(items):
        name = name.name
        name_list.append(name)
    
    # initiate dataframe
    df = pd.DataFrame({"Screen_Name": follower_list, "Id": ids_list, "Name": name_list, "DM_Sent?": "No"})

    # print
    return df

# Send a DM!
def dm():
    # type your message
    text = "This is an automated direct message."

    # my fake accounts
    send_text_list = [1126704586893316096, 1039712141283139584]

    for user_ids in send_text_list:
        # time function, 1 message every 87 seconds is ~1000 per day, twitter limit
        # (60 secs * 60 mins * 24 hours) / 1000 messages = 86.7 seconds
        time.sleep(86.7)
        api.send_direct_message(user_ids, text)

#if __name__ == "__main__":
