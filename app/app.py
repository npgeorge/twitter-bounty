import os
from dotenv import load_dotenv
from flask import Flask, Blueprint, jsonify, request, render_template, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from routes import my_routes
#from models import db, migrate, User, Repos

load_dotenv()

# database url as an environment variable, needs to be updated
DATABASE_URL = os.getenv("DATABASE_URL", default="OOPS")

def create_app():

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # linking to routes.py page via my_routes variable
    app.register_blueprint(my_routes)

    return app