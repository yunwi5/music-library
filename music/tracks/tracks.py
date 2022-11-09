from flask import Blueprint
from flask import request, render_template, redirect, url_for, session, flash

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, validators, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError

import music.tracks.services as services
import music.adapters.repository as repo
from music.utilities.utilities import SearchForm
from music.authentication.authentication import login_required

# Create a track blueprint
tracks_blueprint = Blueprint('tracks_bp', __name__)


@tracks_blueprint.route('/browse_tracks', methods=['GET'])
def browse_tracks():
    user_name = session['user_name'] if 'user_name' in session else None
    tracks_per_page = 10

    # Current page of browsing which starts from 0
    page = request.args.get('page')
    page = int(page) if page is not None and page.isdigit() else 0

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

    # Construct urls for viewing tracks details and reviews.
    for track in page_tracks:
        track['track_detail_url'] = url_for(
            'tracks_bp.track_detail', track_id=track['track_id'])

    return render_template(
        'tracks/browse_tracks.html',
        # Custom page title
        title=f'Browse Tracks | CS235 Music Library',
        # Page heading
        heading='Browse Tracks',
        page=page,
        search_form=SearchForm(),
        user_name=user_name,
        tracks=page_tracks,
        number_of_tracks=num_tracks,
        first_tracks_url=first_tracks_url,
        prev_tracks_url=prev_tracks_url,
        next_tracks_url=next_tracks_url,
        last_tracks_url=last_tracks_url
    )


@tracks_blueprint.route('/search_tracks', methods=['GET', 'POST'])
def search_tracks():
    tracks_per_page = 10

    user_name = session['user_name'] if 'user_name' in session else None
    search_key, text = None, None

    # Create search form on the header searchbar
    search_form = SearchForm()
    if search_form.validate_on_submit():
        # Search key: 'title' | 'artist' | 'album' | 'genre'
        search_key = search_form.search_key.data
        text = search_form.text.data

    # If it is a get request, get search_key and text from the query strings to continue to search
    if request.method == 'GET':
        search_key = request.args.get('search_key')
        text = request.args.get('text')

    # Current page of browsing which starts from 0
    page = request.args.get('page')
    page = int(page) if page is not None and page.isdigit() else 0

    searched_tracks = services.get_tracks_for_search(
        search_key, text, repo.repo_instance)
    number_of_searched_tracks = len(searched_tracks)

    searched_page_tracks = searched_tracks[page *
                                           tracks_per_page:page*tracks_per_page+tracks_per_page]

    first_tracks_url, prev_tracks_url, next_tracks_url, last_tracks_url = None, None, None, None

    # Previous page exists
    if page > 0:
        prev_tracks_url = url_for(
            'tracks_bp.search_tracks', page=page - 1, search_key=search_key, text=text)
        first_tracks_url = url_for(
            'tracks_bp.search_tracks', search_key=search_key, text=text)

    # Next page exists
    if page * tracks_per_page + tracks_per_page < number_of_searched_tracks:
        next_tracks_url = url_for(
            'tracks_bp.search_tracks', page=page+1, search_key=search_key, text=text)
        # Last page using the last page index
        last_tracks_url = url_for(
            'tracks_bp.search_tracks', page=(number_of_searched_tracks-1)//tracks_per_page, search_key=search_key, text=text)

    # Construct urls for viewing tracks details and reviews.
    for track in searched_page_tracks:
        track['track_detail_url'] = url_for(
            'tracks_bp.track_detail', track_id=track['track_id'])

    return render_template(
        'tracks/browse_tracks.html',
        # Custom page title
        title=f'Tracks By {search_key.capitalize()} | CS235 Music Library',
        # Page heading
        heading='Tracks for',
        # Highlight text on the heading
        highlight=f'{search_key.capitalize()}s based on "{text}"',
        page=page,
        search_form=search_form,
        user_name=user_name,
        tracks=searched_page_tracks,
        number_of_tracks=number_of_searched_tracks,
        first_tracks_url=first_tracks_url,
        prev_tracks_url=prev_tracks_url,
        next_tracks_url=next_tracks_url,
        last_tracks_url=last_tracks_url
    )


@tracks_blueprint.route('/track_detail', methods=['GET'])
def track_detail():
    user_name = session['user_name'] if 'user_name' in session else None
    track_id = get_track_id_arg()

    # Get tracks for the track_id and add its list of reviews to the dict.
    track = get_track_and_reviews(track_id)
    # Current user's review on this track
    user_review = services.get_review_for_track_by_user(track_id, user_name, repo.repo_instance)

    # If track was not found, redirect to the browsing page.
    if track is None:
        flash(f'Track {track_id} was not found...', 'error')
        return redirect(url_for('tracks_bp.browse_tracks'))

    return render_template(
        'tracks/track_detail.html',
        title=f"Track {track['title']} | CS235 Music Library",
        track_review_url=url_for(
            'tracks_bp.track_review', track_id=track['track_id']),
        search_form=SearchForm(),
        user_name=user_name,
        user_review=user_review,
        track=track,
    )


@tracks_blueprint.route('/track_review', methods=['GET', 'POST'])
@login_required
def track_review():
    user_name = session['user_name'] if 'user_name' in session else None
    review_form = ReviewForm()

    if review_form.validate_on_submit():
        # Successful POST, i.e. the rating and review_text have passed data validation.
        track_id = int(review_form.track_id.data)
        review_text = review_form.review_text.data
        rating = review_form.rating.data

        # Use the service function to add the review to the repository
        services.add_review(track_id, user_name, review_text,
                            rating, repo.repo_instance)

        flash(f'Your review has been added!', 'success')
        # Go back to the detail page of this track
        return redirect(url_for('tracks_bp.track_detail', track_id=track_id))

    track_id = None
    if request.method == 'GET':
        track_id = get_track_id_arg()
        # Store the track id in the form.
        review_form.track_id.data = track_id

    else:
        # Request is a HTTP POST where form validation has failed.
        # Request is a HTTP GET to display the form.
        flash(f'Your review could not be added...', 'error')

        # Extract the track id being hidden in form.
        track_id = int(review_form.track_id.data)

    # Get tracks for the track_id and add its list of reviews to the dict.
    track = get_track_and_reviews(track_id)
    # Current user's review on this track
    user_review = services.get_review_for_track_by_user(track_id, user_name, repo.repo_instance)

    return render_template(
        'tracks/track_detail.html',
        title=f"Review on {track['title']} | CS235 Music Library",
        track=track,
        user_name=user_name,
        search_form=SearchForm(),
        user_review=user_review,
        review_form=review_form,
    )


# Helper function to get track_id query param as an integer.
def get_track_id_arg():
    track_id = request.args.get('track_id')
    track_id = int(
        track_id) if track_id is not None and track_id.isdigit() else None
    return track_id


# Helper function for finding track, and add its reviews as its attribute.
# Used in track_detail() and track_review() functions
def get_track_and_reviews(track_id: int):
    track = services.get_track(track_id, repo.repo_instance)
    if track is None:
        return None

    # Get reviews for this track as list of dictionaries
    review_dicts = services.get_reviews_for_track(track_id, repo.repo_instance)
    track['reviews'] = review_dicts
    return track


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    rating = IntegerField('Rating (1 - 5)', [validators.DataRequired(), validators.NumberRange(
        min=1, max=5, message='Your rating should be between 1 and 5')])
    review_text = TextAreaField('Comment', [
        DataRequired(),
        Length(min=5, message='Your review should be at least 5 characters'),
        ProfanityFree(message='Your review must not contain profanity')])
    track_id = HiddenField('Track id')
    submit = SubmitField('Confirm')
