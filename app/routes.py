from flask import Blueprint, jsonify, request, render_template, current_app
from models import Followers
import tweepy


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

@my_routes.route('/keys', methods=['GET', 'POST'])
def get_keys():
    # user inputs twitter API Keys
    KEY = request.form['key']
    KEY_SECRET = request.form['key_secret']
    TOKEN = request.form['token']
    TOKEN_SECRET = request.form['token_secret']
    
    # authenticate user
    auth = tweepy.OAuthHandler(KEY, KEY_SECRET)
    auth.set_access_token(TOKEN, TOKEN_SECRET)
    # create api
    api = tweepy.API(auth)
    print('success!')
    return api