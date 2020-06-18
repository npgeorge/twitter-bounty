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


