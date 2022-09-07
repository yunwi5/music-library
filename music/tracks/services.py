from typing import List, Iterable

from music.adapters.repository import AbstractRepository
from music.domainmodel.user import User, Track
from music.domainmodel.review import Review
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
    return tracks_to_dicts(tracks_for_page)


def get_tracks_for_search(search_key: str, text: str, repo: AbstractRepository):
    search_key = search_key.strip().lower()
    searched = []
    # Only three types of search keys: 'artist' | 'album' | 'genre'. Otherwise, they are invalid search keys.
    if search_key == 'album':
        searched = repo.search_tracks_by_album(text)

    elif search_key == 'artist':
        searched = repo.search_tracks_by_artist(text)

    elif search_key == 'genre':
        searched = repo.search_tracks_by_genre(text)

    else:
        raise InvalidSearchKeyException(f'Search key {search_key} is invalid')

    return tracks_to_dicts(searched)


def add_review(track_id: int,  user_name: str, review_text: str, rating: int,  repo: AbstractRepository):
    track = repo.get_track(track_id)
    user = repo.get_user(user_name)

    if track is None:
        raise NonExistentTrackException
    if user is None:
        raise UnknownUserException

    review = Review(track, review_text, rating)
    review.user = user
    repo.add_review(review)


def get_reviews_for_track(track_id: int, repo: AbstractRepository):
    track_reviews = repo.get_reviews_for_track(track_id)
    return reviews_to_dicts(track_reviews)


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


def tracks_to_dicts(tracks: List[Track]) -> List[dict]:
    return [track_to_dict(track) for track in tracks]


def review_to_dict(review: Review) -> dict:
    date_format = review.timestamp.strftime('%d %b, %Y')
    review_dict = {
        'review_text': review.review_text,
        'rating': review.rating,
        'user': review.user.user_name if review.user else None,
        'track': review.track.title if review.track else None,
        'timestamp': date_format
    }
    return review_dict


def reviews_to_dicts(reviews: List[Review]) -> List[dict]:
    return [review_to_dict(review) for review in reviews]
