import os
from dotenv import load_dotenv
from flask import Flask, Blueprint, jsonify, request, render_template, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from web_app.routes import my_routes
from web_app.models import db, migrate, Followers, User
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from web_app.services import twitter_api_client

# wrong
#from web_app.services import twitter_blueprint
load_dotenv()

# database url as an environment variable, needs to be updated
DATABASE_URL = os.getenv("DATABASE_URL", default="OOPS")

# for sign in
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY", default="OOPS")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET", default="OOPS")

def create_app():

    app = Flask(__name__)
    # already have
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # for login from flask dance
    app.config['SECRET_KEY'] = 'thisissupposedtobeasecret'

    app.config["TWITTER_OAUTH_CLIENT_KEY"] = TWITTER_API_KEY
    app.config["TWITTER_OAUTH_CLIENT_SECRET"] = TWITTER_API_SECRET

    twitter_bp = make_twitter_blueprint()
    
    app.register_blueprint(twitter_bp, url_prefix="/login")
    

    # for databases
    db.init_app(app)
    migrate.init_app(app, db)
    
    # linking to routes.py page via my_routes variable
    app.register_blueprint(my_routes)
     
    return app