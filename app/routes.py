# current app ppints to config in app.py
from flask import Blueprint, jsonify, request, render_template, current_app
#from models import User, Tweet, db
from services import twitter_api_client

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