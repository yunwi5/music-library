from flask import Blueprint
from flask import request, render_template, redirect, url_for, session, flash


import music.albums.services as services
import music.adapters.repository as repo
from music.utilities.utilities import SearchForm

# Create a album blueprint
albums_blueprint = Blueprint('albums_bp', __name__)


@albums_blueprint.route('/browse_albums', methods=['GET'])
def browse_albums():
    user_name = session['user_name'] if 'user_name' in session else None
    albums_per_page = 10

    # Current page of browsing which starts from 0
    page = request.args.get('page')
    page = int(page) if page is not None and page.isdigit() else 0

    num_albums = services.get_number_of_albums(repo.repo_instance)
    page_albums = services.get_albums_for_page(page, albums_per_page, repo.repo_instance)

    first_albums_url, prev_albums_url, next_albums_url, last_albums_url = None, None, None, None

    # Previous page exists
    if page > 0:
        prev_albums_url = url_for('albums_bp.browse_albums', page=page - 1)
        first_albums_url = url_for('albums_bp.browse_albums')

    # Next page exists
    if page * albums_per_page + albums_per_page < num_albums:
        next_albums_url = url_for('albums_bp.browse_albums', page=page+1)
        # Last page using the last page index
        last_albums_url = url_for(
            'albums_bp.browse_albums', page=(num_albums-1)//albums_per_page)

    # Construct urls for viewing albums details and reviews.
    for album in page_albums:
        album['album_detail_url'] = url_for(
            'albums_bp.album_detail', album_id=album['album_id'])

    return render_template(
        'albums/browse_albums.html',
        # Custom page title
        title=f'Browse albums | CS235 Music Library',
        # Page heading
        heading='Browse albums',
        page=page,
        search_form=SearchForm(),
        user_name=user_name,
        albums=page_albums,
        number_of_albums=num_albums,
        first_albums_url=first_albums_url,
        prev_albums_url=prev_albums_url,
        next_albums_url=next_albums_url,
        last_albums_url=last_albums_url
    )



@albums_blueprint.route('/album_detail', methods=['GET'])
def album_detail():
    user_name = session['user_name'] if 'user_name' in session else None
    album_id = get_album_id_arg()

    # Get album and with its tracks
    album = services.get_album(album_id, repo.repo_instance)
    album_tracks = services.get_tracks_by_album(album_id, repo.repo_instance)

    # Insert track detail link for each album track
    for track in album_tracks:
        track['track_detail_url'] = url_for(
            'tracks_bp.track_detail', track_id=track['track_id'])

    if album is None:
        flash(f'Album {album_id} was not found...', 'error')                                                          
        return redirect(url_for('albums_bp.browse_albums'))

    return render_template(
        'albums/album_detail.html',
        title=f'Album {album["title"]} | CS235 Music Library',
        album=album,
        album_tracks=album_tracks,
        number_of_tracks=len(album_tracks),
        search_form=SearchForm(),
        user_name=user_name,
    )

# Helper function to get album_id query param as an integer.
def get_album_id_arg():
    album_id = request.args.get('album_id')
    album_id = int(album_id) if album_id is not None and album_id.isdigit() else None
    return album_id