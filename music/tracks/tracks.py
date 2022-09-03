from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

import music.tracks.services as services
import music.adapters.repository as repo
from music.utilities.utilities import SearchForm
from music.authentication.authentication import login_required

# Create a track blueprint
tracks_blueprint = Blueprint('tracks_bp', __name__)


@tracks_blueprint.route('/tracks', methods=['GET'])
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

    # TODO: Construct urls for viewing tracks reviews and adding comments.
    for track in page_tracks:
        pass

    return render_template(
        'tracks/browse.html',
        # Custom page title
        title=f'Browse Tracks | Music Librarian',
        # Page heading
        heading='Browse Tracks',
        page=page,
        search_form=SearchForm(),
        user_name=user_name,
        tracks=page_tracks,
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
        # Search key: 'artist' | 'album' | 'genre'
        search_key = search_form.search_key.data
        text = search_form.text.data
        print(f'key: {search_key}, text: {text}')

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

    # TODO: Construct urls for viewing tracks reviews and adding comments.
    for track in searched_page_tracks:
        pass

    return render_template(
        'tracks/browse.html',
        # Custom page title
        title=f'Tracks By {search_key.capitalize()} | Music Librarian',
        # Page heading
        heading='Tracks for',
        # Highlight text on the heading
        highlight=f'{search_key.capitalize()}s based on "{text}"',
        page=page,
        search_form=search_form,
        user_name=user_name,
        tracks=searched_page_tracks,
        first_tracks_url=first_tracks_url,
        prev_tracks_url=prev_tracks_url,
        next_tracks_url=next_tracks_url,
        last_tracks_url=last_tracks_url
    )
