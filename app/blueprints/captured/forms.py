from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired



class Captured(FlaskForm):
    name= StringField('Pokemon Name: ')
    capition = StringField('Caption: ')
    img_url = StringField('Image URL: ', validators=[DataRequired()])
    submitButton = SubmitField('Choose Pokemon')