from flask import Blueprint
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

# Configure Blueprint.
utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


class SearchForm(FlaskForm):
    search_key = SelectField(
        'SearchKey',
        choices=[('artist', 'Artist'), ('album', 'Album'), ('genre', 'Genre')])
    text = StringField('Text', [
        DataRequired(message='Search text is required'),
        Length(min=1, message='Search text is too short')])
    # Instead of a submit field, define custom submit button on the header.html template.
    submit = SubmitField('Search')
