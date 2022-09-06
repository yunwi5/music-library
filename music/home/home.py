from flask import Blueprint, render_template, session

from music.utilities.utilities import SearchForm

home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    # Obtain the user name of the currently logged in user.
    user_name = session['user_name'] if 'user_name' in session else None

    return render_template(
        'home/home.html',
        search_form=SearchForm(),
        user_name=user_name,
    )
