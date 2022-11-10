from typing import List

from music.adapters.repository import AbstractRepository
from music.domainmodel.track import Track
from music.domainmodel.review import Review


class NonExistentTrackException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class InvalidPageException(Exception):
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


def get_tracks_for_page(page_index: int, tracks_per_page: int, repo: AbstractRepository):
    if type(page_index) is not int:
        raise InvalidPageException('Page should be a type integer')
    if page_index < 0:
        raise InvalidPageException('Negative page does not exist.')

    tracks = repo.get_tracks(sorting=True)

    # Find the start index of the tracks for the current page.
    start_index = page_index * tracks_per_page
    if start_index >= len(tracks):
        raise InvalidPageException('The page does not exist.')

    # Retrieve tracks list for the current page as a list.
    tracks_for_page = tracks[start_index:start_index+tracks_per_page]
    return tracks_to_dicts(tracks_for_page, start_index)


def get_tracks_for_search(search_key: str, text: str, repo: AbstractRepository):
    search_key = search_key.strip().lower()
    searched = []
    # Only four types of search keys: 'title' | 'artist' | 'album' | 'genre'.
    # Otherwise, they are invalid search keys.
    if search_key == 'title':
        searched = repo.search_tracks_by_title(text)

    elif search_key == 'album':
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

    # Do not allow the user to make review on the same track twice.
    # If there is an existing review by this user, return it.
    user_existing_review = get_review_for_track_by_user(track_id, user_name, repo)
    if user_existing_review is not None:
        return

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


# Get review made by the user for the track of the track_id
def get_review_for_track_by_user(track_id: int, user_name: str, repo: AbstractRepository):
    track_reviews = repo.get_reviews_for_track(track_id)
    # If current user's reviews already exist for the track, do not allow review twice.
    for review in track_reviews:
        if review.user.user_name == user_name:
            return review_to_dict(review)
    return None

# Helper function to calculate the duration format into mm:ss user readable format.
def get_duration_format(total_seconds: int):
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f'{minutes}:{seconds}'


def track_to_dict(track: Track, index: int = None):
    genre_names = [genre.name for genre in track.genres]
    genres_format = ', '.join(genre_names)

    track_dict = {
        'track_id': track.track_id,
        'title': track.title,
        'artist': track.artist.full_name if track.artist is not None else None,
        'album_id': track.album.album_id if track.album is not None else None,
        'album': track.album.title if track.album is not None else None,
        'track_url': track.track_url,
        'track_duration': get_duration_format(track.track_duration),
        'genres': genres_format,
        'index': index
    }
    return track_dict


def tracks_to_dicts(tracks: List[Track], start_index: int = 0) -> List[dict]:
    return [track_to_dict(track, start_index + index) for index, track in enumerate(tracks)]


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
