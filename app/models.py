from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

# create instance of database
db = SQLAlchemy()

team = db.Table(
    'team',
    db.Column('trainer_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id')),


)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String, nullable=False)
    lastName = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password= db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    following = db.relationship('User', 
                                secondary = team,
                                backref = db.backref('team', lazy='dynamic'),
                                lazy='dynamic')

    def __init__(self, firstName, lastName, email, password):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = generate_password_hash(password)
        

class Pokemon(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    ability_name = db.Column(db.String)
    base_experience = db.Column(db.String)
    attack_base_stat = db.Column(db.Integer)
    defense_base_stat = db.Column(db.Integer)
    hp_base_stat = db.Column(db.Integer)
    sprites_image = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
  




    def __init__(self, name, ability_name, base_experience, attack_base_stat, defense_base_stat, hp_base_stat, sprites_image):
        self.name = name
        self.ability_name =  ability_name
        self.base_experience = base_experience
        self.attack_base_stat = attack_base_stat
        self.defense_base_stat = defense_base_stat
        self.hp_base_stat = hp_base_stat
        self.sprites_image = sprites_image
       
      

