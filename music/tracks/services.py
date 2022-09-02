from typing import List, Iterable

from music.adapters.repository import AbstractRepository
from music.domainmodel.user import User, Track, Review
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist


class NonExistentTrackException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_comment(track_id: int, review_text: str, rating: int, user_name: str, repo: AbstractRepository):
    pass


def get_track(track_id: int, repo: AbstractRepository):
    pass


def get_number_of_tracks(repo: AbstractRepository):
    return repo.get_number_of_tracks()


def get_tracks_for_page(page_index: int, tracks_per_page, repo: AbstractRepository):
    tracks = repo.get_tracks()
    start_index = page_index * tracks_per_page
    tracks_for_page = tracks[start_index:start_index+tracks_per_page]
    return tracks_to_dict(tracks_for_page)


def get_duration_format(total_seconds: int):
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f'{minutes}:{seconds}'


def track_to_dict(track: Track):
    track_dict = {
        'track_id': track.track_id,
        'title': track.title,
        'artist': track.artist.full_name,
        'album': track.album.title,
        'track_url': track.track_url,
        'track_duration': get_duration_format(track.track_duration),
        'genres': [genre.name for genre in track.genres]
    }
    return track_dict


def tracks_to_dict(tracks: List[Track]) -> List[dict]:
    return [track_to_dict(track) for track in tracks]
