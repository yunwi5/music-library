from flask import Blueprint, render_template, session


home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    # Obtain the user name of the currently logged in user.
    user_name = session['user_name'] if 'user_name' in session else None
    print(f'use_name: {user_name}')

    return render_template(
        'home/home.html',
        user_name=user_name,
    )
