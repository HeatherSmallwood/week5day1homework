from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

# create instance of database
db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String, nullable=False)
    lastName = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password= db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self,firstName, lastName,email,password):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = generate_password_hash(password)
        

class Captured(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =db.Column(db.String)
    caption =db.Column(db.String)
    img_url = db.Column(db.String, nullable =False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __init__(self, name, caption, img_url, user_id):
        self.name = name
        self.caption = caption
        self.img_url = img_url
        self.user_id = user_id