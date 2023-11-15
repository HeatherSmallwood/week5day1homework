from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

# create instance of database
db = SQLAlchemy()

team = db.Table(
    'team',
    db.Column('trainer_id', db.Integer, db.ForeignKey('trainer.id')),
    db.Column('pokemon_id', db.String, db.ForeignKey('pokemon.id')),


)

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String, nullable=False)
    lastName = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password= db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    following = db.relationship('User', 
                                secondary = team,
                                backref = db.backref(team, lazy='dynamic'),
                                lazy='dynamic')

    def __init__(self,firstName, lastName,email,password):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = generate_password_hash(password)
        

class Pokemon(db.Model):
    name =db.Column(db.String, primary_key=True)
    img_url = db.Column(db.String, nullable =False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), nullable=False)




    def __init__(self, name, img_url, pokemon_id):
        self.name = name
        self.img_url = img_url
        self.user_id = pokemon_id

