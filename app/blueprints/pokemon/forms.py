from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired



class PokemonForm(FlaskForm):
    name= StringField('Pokemon Name: ')
    img_url = StringField('Image URL: ', validators=[DataRequired()])
    submitButton = SubmitField('Choose Pokemon')