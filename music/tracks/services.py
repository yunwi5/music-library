from typing import List, Iterable

from music.adapters.repository import AbstractRepository
from music.domainmodel.user import User, Track, Review
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist


class NonExistentTrackException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class InvalidSearchKeyException(Exception):
    pass


def get_track(track_id: int, repo: AbstractRepository) -> dict:
    if track_id is None:
        return None
    track = repo.get_track(track_id)
    return track_to_dict(track) if track is not None else None


def get_number_of_tracks(repo: AbstractRepository):
    return repo.get_number_of_tracks()


def get_tracks_for_page(page_index: int, tracks_per_page: str, repo: AbstractRepository):
    tracks = repo.get_tracks()
    start_index = page_index * tracks_per_page
    tracks_for_page = tracks[start_index:start_index+tracks_per_page]
    return tracks_to_dict(tracks_for_page)


def get_tracks_for_search(search_key: str, text: str, repo: AbstractRepository):
    search_key = search_key.strip().lower()
    searched = []
    # Only three types of search keys: 'artist' | 'album' | 'genre'. Otherwise, they are invalid search keys.
    if search_key == 'album':
        searched = repo.search_tracks_by_album(text)

    elif search_key == 'artist':
        searched = repo.seach_tracks_by_artist(text)

    elif search_key == 'genre':
        searched = repo.search_tracks_by_genre(text)

    else:
        raise InvalidSearchKeyException(f'Search key {search_key} is invalid')

    return tracks_to_dict(searched)


def add_review(track_id: int, review_text: str, rating: int, user_name: str, repo: AbstractRepository):
    pass


def get_reviews_for_track(track_id: int, repo: AbstractRepository):
    pass


# Helper function to calculate the duration format into mm:ss user readable format.
def get_duration_format(total_seconds: int):
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f'{minutes}:{seconds}'


def track_to_dict(track: Track):
    genre_names = [genre.name for genre in track.genres]
    genres_format = ', '.join(genre_names)

    track_dict = {
        'track_id': track.track_id,
        'title': track.title,
        'artist': track.artist.full_name if track.artist is not None else None,
        'album': track.album.title if track.album is not None else None,
        'track_url': track.track_url,
        'track_duration': get_duration_format(track.track_duration),
        'genres': genres_format
    }
    return track_dict


def tracks_to_dict(tracks: List[Track]) -> List[dict]:
    return [track_to_dict(track) for track in tracks]
