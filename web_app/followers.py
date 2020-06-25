import os
from dotenv import load_dotenv
import tweepy
import pandas as pd
import requests
import time
from flask import Blueprint, jsonify, request, render_template, current_app, Response, make_response
from web_app.services import twitter_api_client

load_dotenv()

client = twitter_api_client()

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

    df = pd.DataFrame(send_text_list,columns=['Id'])

    df['DM_Sent'] = 'No'

    print(df)

    for row in df.itertuples():
        # time function, 1 message every 87 seconds is ~1000 per day, twitter limit
        # (60 secs * 60 mins * 24 hours) / 1000 messages = 86.7 seconds
        time.sleep(5)
        if api.send_direct_message(row.Id, text):
            df.loc[df.DM_Sent == 'No', 'DM_Sent'] = 'Yes'
    
    print(df)

#
#
#
# ---- ADDED -----
#
#
#

# login
# almost works, needs correct callback, needs work
def login():

    KEY = request.form['consumer_key']
    KEY_SECRET = request.form['consumer_secret']

    twitter = OAuth1Service(
    name='twitter',
    consumer_key=KEY,
    consumer_secret=KEY_SECRET,
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize',
    base_url = 'https://api.twitter.com/1/')

    request_token, request_token_secret = twitter.get_request_token()

    authorize_url = twitter.get_authorize_url(request_token)

    print('Visit this URL in your browser: ', authorize_url)
    open(authorize_url)
    verifier = raw_input('Enter oauth_verifier from browser: ')

    session = twitter.get_auth_session(
        request_token,
        request_token_secret,
        method='POST',
        data={'oauth_verifier': verifier})

    params = {
        # Include retweets
        'include_rts': 1,
        # 10 tweets
        'count': 10}

    resp = session.get('statuses/home_timeline.json', params=params)

    for i, tweet in enumerate(resp.json(), 1):
        handle = tweet['user']['screen_name'].encode('utf-8')
        text = tweet['text'].encode('utf-8')
        print('{0}. @{1} - {2}'.format(i, handle, text))



def tester():
    client = current_app.config["TWITTER_API_CLIENT"]

    screen_name=request.form['5000_csv_sn']
    
    ids = []
    for page in tweepy.Cursor(client.followers_ids, screen_name=screen_name).pages(1):
        try:
            ids.extend(page)
            # check
            print(ids)
            # see size
            print(len(ids))
            # to avoid rate limit
            time.sleep(60)
        except tweepy.RateLimitError:
            print("Rate Limit Reached! Script will resume in 15 minutes.") 
            time.sleep(60*15)

    # instantiate list for df build
    followers = []

    try:
        # make batches of 100 ids to pass into, WORKS
        for i in range(0, len(ids), 100):
            batch = ids[i:i+100]
            for follower in client.lookup_users(batch):
                followers.append({
                    "id": follower.id, 
                    "screen_name": follower.screen_name, 
                    "name": follower.name,
                    "followers_count": follower.followers_count,
                    "created_at": follower.created_at,
                    "friends_count": follower.friends_count,
                    "statuses_count": follower.statuses_count,
                    "verified": follower.verified
                    })
    except tweepy.RateLimitError:
        print("Rate Limit Reached! Script will resume in 15 minutes.") 
        time.sleep(60*15)
    
    # check, WORKS
    print(followers)
    print(type(followers))

    # creating dataframe
    df = pd.DataFrame.from_dict(followers)

    # check
    print(df)
    
    # params
    param = request.form['5000_csv_param']

    # sort by followers_count
    sorted_df = df.sort_values(by=param, ascending=False)

    # check
    print("-----")
    print(sorted_df)

    resp = make_response(sorted_df.to_csv())
    resp.headers["Content-Disposition"] = "attachment; filename=followers_db.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp


# getting followers dictionary response
def get_twitter_user():
    username = request.form['get_followers_json']
    
    followers_list = []

    followers_ids = []
    
    #client = twitter_api_client()
    
    client = current_app.config["TWITTER_API_CLIENT"]
    
    # trying to increase count with pages
    try:
        for page in tweepy.Cursor(client.followers_ids, count=5000).pages():
            followers_ids.append(page)
    except tweepy.RateLimitError:
        # wait 15 minutes for API limit to reset
        print("Rate Limit Exceeded: will resume in 15 minutes...") 
        time.sleep(15 * 60)

    # check
    print(followers_ids)

    # this works but count is low, no timer yet
    followers = client.followers(screen_name=username, count=200)

    for follower in followers:
        followers_list.append({
            "id": follower.id, 
            "screen_name": follower.screen_name, 
            "name": follower.name,
            "followers_count": follower.followers_count,
            "created_at": follower.created_at,
            "friends_count": follower.friends_count,
            "statuses_count": follower.statuses_count,
            "verified": follower.verified
            })
    
    # check
    print(followers_list)

    # get list of just id's of followers
    ids_list=[]
    for item in followers_list:
        ids_list.append(item['id'])

    # check
    print(ids_list)

    return jsonify(followers_list)