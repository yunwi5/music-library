from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import music.tracks.services as services
import music.adapters.repository as repo
from music.authentication.authentication import login_required

# Create a track blueprint
tracks_blueprint = Blueprint('tracks_bp', __name__)


@tracks_blueprint.route('/tracks', methods=['GET'])
def browse_tracks():
    user_name = session['user_name'] if 'user_name' in session else None
    tracks_per_page = 10

    # Current page of browsing which starts from 0
    page = request.args.get('page')

    if page is None or not page.isdigit():
        page = 0
    else:
        page = int(page)

    num_tracks = services.get_number_of_tracks(repo.repo_instance)
    page_tracks = services.get_tracks_for_page(
        page, tracks_per_page, repo.repo_instance)

    first_tracks_url, prev_tracks_url, next_tracks_url, last_tracks_url = None, None, None, None

    # Previous page exists
    if page > 0:
        prev_tracks_url = url_for('tracks_bp.browse_tracks', page=page - 1)
        first_tracks_url = url_for('tracks_bp.browse_tracks')

    # Next page exists
    if page * tracks_per_page + tracks_per_page < num_tracks:
        next_tracks_url = url_for('tracks_bp.browse_tracks', page=page+1)
        # Last page using the last page index
        last_tracks_url = url_for(
            'tracks_bp.browse_tracks', page=(num_tracks-1)//tracks_per_page)

    # TODO: Construct urls for viewing tracks reviews and adding comments.
    for track in page_tracks:
        pass

    return render_template(
        'tracks/browse.html',
        title='Browse Tracks',
        page=page,
        user_name=user_name,
        tracks=page_tracks,
        first_tracks_url=first_tracks_url,
        prev_tracks_url=prev_tracks_url,
        next_tracks_url=next_tracks_url,
        last_tracks_url=last_tracks_url
    )
