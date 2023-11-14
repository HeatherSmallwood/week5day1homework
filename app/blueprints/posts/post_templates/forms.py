from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired



class PostForm(FlaskForm):
    title= StringField('Title: ')
    capition = StringField('Caption: ')
    img_url = StringField('Image URL: ', validators=[DataRequired()])
    submitButton = SubmitField('Create Post')