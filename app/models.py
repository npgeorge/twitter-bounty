from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# database object
db = SQLAlchemy()

migrate = Migrate()

# database tables
class Followers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    screen_name = db.Column(db.String(120))
    sent_dm = db.Column(db.Boolean(create_constraint=False))
    bio = db.Column(db.String(120))




#from flask_login import UserMixin, current_user, LoginManager, login_required, login_user, logout_user
#
#
# trying to port in sign in and authentication
#
#
#



#login_manager = LoginManager()

#class User(UserMixin, db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    username = db.Column(db.String(250), unique=True)
#
#class OAuth(OAuthConsumerMixin, db.Model):
#    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
#    user = db.relationship(User)
#
# not sure this goes here?
#twitter_blueprint.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)