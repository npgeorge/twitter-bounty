from flask import Blueprint, jsonify, request, render_template, current_app, Response, make_response
from web_app.models import Followers
import tweepy
import webbrowser
import pickle               
from pprint import pprint
from flask import Flask, redirect, url_for
from web_app.followers import twitter_api_client
import pandas as pd
import time
#from flask_dance.contrib.twitter import make_twitter_blueprint, twitter

#
# ROUTING
#

my_routes = Blueprint("my_routes", __name__)

# method decorators
# above our normal looking function, it specifies a route or url path
# each def needs to be unique for this to work
@my_routes.route("/")
def homepage():
    return render_template("homepage.html")

# landing page route
@my_routes.route("/index")
def index():
    return render_template("index.html")


#
#
#
# ---- ADDED & OPTIMIZED -----
#
#
#

# login
# almost works, needs correct callback, needs work
@my_routes.route("/login", methods=["POST"])
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

# messaging
@my_routes.route("/message", methods=['POST', 'GET'])
def message_test():
    client = current_app.config["TWITTER_API_CLIENT"]

    screen_name = request.form['message_sn']

    pages = request.form['pages']

    pages = int(pages)
    
    ids = []
    # change the pages parameter for more ids, each page is 5000 users
    for page in tweepy.Cursor(client.followers_ids, screen_name=screen_name).pages(pages):
        try:
            ids.extend(page)
            # check
            print(ids)
            # see size
            print("Number of ID's gathered: ", len(ids))
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
            print("C")
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
                    "verified": follower.verified,
                    "location": follower.location
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
    
    # params filter
    param = request.form["message_sort"]

    # grabbing user input location
    location  = request.form['location_message']

    # filtering by location
    location_filter = (df['location'] == location)

    # if user does not pass in location, filter by params only
    # else filter by params and location filter
    if(len(location) == 0):
        print("----- SORTED DATAFRAME -----")
        sorted_df = df.sort_values(by=param, ascending=False)
    else :
        print("----- LOCATION DF -----")
        sorted_df = df.sort_values(by=param, ascending=False) 
        sorted_df = sorted_df[location_filter]

    print("----- SORTED DATAFRAME -----")
    print(sorted_df)

    # grab sorted id's
    message_ids_df = sorted_df['id']
    #check
    print(message_ids_df)

    #
    #
    # --- TESTING ENVIRONMENT, CHANGE BEFORE DEPLOYING ---
    #
    #
    
    #
    #
    # for deployment pass in message_list_df
    #
    #

    # my fake accounts for testing

    #
    #
    # ***** REPLACE WITH message_ids_df BEFORE DEPLOYING *****
    send_text_list = [1126704586893316096, 1039712141283139584]

    df_tester = pd.DataFrame(send_text_list,columns=['Id'])

    # adding column to track messages sent
    df_tester['DM_Sent'] = 'No'

    print(df_tester)
    # ***** REPLACE WITH message_ids_df BEFORE DEPLOYING *****
    #
    #

    message = request.form['message']
    print('-----')
    print("Message sending to followers is...", '"', message,'"...')

    for row in df_tester.itertuples():
        # time function, 1 message every 87 seconds is ~1000 per day, twitter limit
        # run throughout the day or send 1000 all at once, you choose
        # (60 secs * 60 mins * 24 hours) / 1000 messages = 86.7 seconds
        time.sleep(86.7)
        if client.send_direct_message(row.Id, message):
            df_tester.loc[df_tester.DM_Sent == 'No', 'DM_Sent'] = 'Yes'
    
    print(df_tester)

    print('Success! You direct messaged all the followers above.')

    return render_template("message.html")


@my_routes.route("/followers", methods=['POST'])
def followers():
    client = current_app.config["TWITTER_API_CLIENT"]

    screen_name=request.form['csv_sn']

    pages = request.form['pages_followers']

    pages = int(pages)
    
    ids = []
    for page in tweepy.Cursor(client.followers_ids, screen_name=screen_name).pages(pages):
        try:
            ids.extend(page)
            # check for terminal
            print(ids)
            # see size
            print("Number of ID's gathered: ", len(ids))
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
                    "verified": follower.verified,
                    "location": follower.location
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
    param = request.form['csv_param']


    location  = request.form['location_param']

    location_filter = (df['location'] == location)

    if(len(location) == 0):
        print("----- SORTED DATAFRAME -----")
        sorted_df = df.sort_values(by=param, ascending=False)
    else :
        print("----- LOCATION DF -----")
        sorted_df = df.sort_values(by=param, ascending=False) 
        sorted_df = sorted_df[location_filter]
    
    print(sorted_df)

    resp = make_response(sorted_df.to_csv())
    resp.headers["Content-Disposition"] = "attachment; filename=followers_db.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp

# exporting 10,000 followers database to csv
@my_routes.route("/10000_followers", methods=['POST'])
def test_ten_thou():
    client = current_app.config["TWITTER_API_CLIENT"]

    screen_name = request.form['10000_csv_sn']
    
    ids = []
    # change the pages parameter for more ids, each page is 5000 users
    for page in tweepy.Cursor(client.followers_ids, screen_name=screen_name).pages(2):
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
    
    # check
    print(followers)
    print(type(followers))

    # creating dataframe
    df = pd.DataFrame.from_dict(followers)

    # check
    print(df)
    
    # params
    param = request.form['10000_csv_param']

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
@my_routes.route("/get_followers", methods=['POST', 'GET'])
def get_twitter_user():
    username = request.form['get_followers_dict']
    
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