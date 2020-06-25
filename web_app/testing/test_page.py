import os
from dotenv import load_dotenv
import tweepy
import pandas as pd
import requests
import time
from twython import Twython

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

def sn_df():
    # specify number of items (followers) to return, MAX 180 every 15 mins for free users
    # set to two for testing purposes
    items = 2
    # collect followers
    followers = tweepy.Cursor(api.followers, screen_name=at_name).items(items)
    
    # Collect lists
    screen_names_list = [follower.screen_name for follower in followers]
    #ids_list = [follower.id for follower in followers]
    #name_list = [follower.name for follower in followers]

    print(type(screen_names_list))

    #zip the lists
    zippedList =  list(zip(screen_names_list))
    print("zippedList = " , zippedList)

    # build followers dataframe
    sn_df = pd.DataFrame(zippedList, columns = ['Screen_Name'])
    return sn_df

def id_df():
    # specify number of items (followers) to return, MAX 180 every 15 mins for free users
    # set to two for testing purposes
    items = 2
    # collect followers
    followers = tweepy.Cursor(api.followers, screen_name=at_name).items(items)
    
    # Collect lists
    #screen_names_list = [follower.screen_name for follower in followers]
    id_list = [follower.id for follower in followers]
    #name_list = [follower.name for follower in followers]

    print(type(id_list))

    #zip the lists
    zippedList =  list(zip(id_list))
    print("zippedList = " , zippedList)

    # build followers dataframe
    id_df = pd.DataFrame(zippedList, columns = ['Id'])
    return id_df

def name_df():
    # specify number of items (followers) to return, MAX 180 every 15 mins for free users
    # set to two for testing purposes
    items = 2
    # collect followers
    followers = tweepy.Cursor(api.followers, screen_name=at_name).items(items)
    
    # Collect lists
    #screen_names_list = [follower.screen_name for follower in followers]
    #ids_list = [follower.id for follower in followers]
    name_list = [follower.name for follower in followers]

    print(type(name_list))

    #zip the lists
    zippedList =  list(zip(name_list))
    print("zippedList = " , zippedList)

    # build followers dataframe
    name_df = pd.DataFrame(zippedList, columns = ['Name'])
    return name_df


# gathering more user info, print statements working, place in dataframes
def sleeper():
    followers = tweepy.Cursor(api.followers, screen_name=at_name, count=5).items()
    for follower in range(0,5):
        try:
            follower = next(followers)
            screen_names_list = []
            screen_names_list.append(follower.screen_name)

            print(type(screen_names_list))
            print(screen_names_list)
        except tweepy.TweepError:
            print("Tweepy has hit its rate limit for now")
            # time function
            time.sleep(60*15)
            # run function again
            next(followers)
    return followers



# working for reference
def original_sleeper():
    followers = tweepy.Cursor(api.followers, screen_name=at_name, count=200).items()
    for follower in range(0,200):
        try:
            follower = next(followers)
            print(follower.screen_name)
            print(follower.name)
        except tweepy.TweepError:
            print("Tweepy has hit its rate limit for now")
            # time function
            time.sleep(60*15)
            # run function again
            next(followers)
    return followers

# This method DOES NOT WORK, is no longer supported with Tweepy
text = "This is a test."
# recipient ID
recipient = "pcsubirachs"

def send_message():
    text = "This is a test."
    # recipient ID
    recipient = "pcsubirachs"
    message = tweepy.send_direct_message(user=recipient, screen_name=recipient, text=text)
    return message

def dm():
    # type your message
    text = "This is a test."

    # my fake accounts
    send_text_list = [1126704586893316096, 1039712141283139584]

    for i in send_text_list:
        api.send_direct_message(i, text)




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
