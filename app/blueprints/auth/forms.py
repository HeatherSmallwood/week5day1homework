from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField,StringField, EmailField
from wtforms.validators import DataRequired, EqualTo

class pokemonFormForm(FlaskForm):
    name = StringField('Enter Pokeman Name: ', validators=[DataRequired()])
    submitButton = SubmitField('Search')
    
class LoginForm(FlaskForm):
    email = EmailField('Email ', validators=[DataRequired()])
    password= PasswordField('Password ', validators=[DataRequired()])
    submitButton = SubmitField('Login')

class SignupForm(FlaskForm):
    firstName = StringField('First Name: ', validators=[DataRequired()])
    lastName = StringField('Last Name: ', validators=[DataRequired()])
    email = EmailField('Email ', validators=[DataRequired()])
    password= PasswordField('Password ', validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password ', validators=[DataRequired(), EqualTo('password')])
    submitButton = SubmitField('Login')
 
