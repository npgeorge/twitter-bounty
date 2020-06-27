from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin, current_user, LoginManager, login_required, login_user, logout_user

# database object
db = SQLAlchemy()

migrate = Migrate()

# models from flask-dance
#db = SQLAlchemy(app)
login_manager = LoginManager()

# database tables
class Followers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    screen_name = db.Column(db.String(120))
    name = db.Column(db.String(120))
    followers_count = db.Column(db.Integer)
    created_at = db.Column(db.String(120))
    friends_count = db.Column(db.Integer)
    statuses_count = db.Column(db.Integer)
    verified = db.Column(db.Boolean)
    location = db.Column(db.String(120))
    DM_sent = db.Column(db.Boolean(create_constraint=False))

# from flask-dance
# tables for sign in
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True)

#class OAuth(OAuthConsumerMixin, db.Model):
#    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
#    user = db.relationship(User)