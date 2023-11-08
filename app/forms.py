from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

class pokemonFormForm(FlaskForm):
    name = TextAreaField('Enter Pokeman Name: ', validators=[DataRequired()])
    submitButton = SubmitField('Search')
