from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField,StringField, EmailField
from wtforms.validators import DataRequired, EqualTo



class PostForm(FlaskForm):
    title= StringField('Title: ')
    capition = StringField('Caption: ')
    img_url = EmailField('Email ', validators=[DataRequired()])
    password= PasswordField('Password ', validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password ', validators=[DataRequired(), EqualTo('password')])
    submitButton = SubmitField('Login')