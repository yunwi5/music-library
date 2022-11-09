from typing import List

from music.adapters.repository import AbstractRepository
from music.domainmodel.album import Album
import music.tracks.services as tracks_services

class NonExistentAlbumException(Exception):
    pass

class InvalidPageException(Exception):
    pass

def get_number_of_albums(repo: AbstractRepository)->int:
    return len(repo.get_albums())


def get_albums_for_page(page_index: int, albums_per_page: int, repo: AbstractRepository)->List[dict]:
    if type(page_index) is not int:
        raise InvalidPageException("Page should be of type integer.")
    if page_index < 0:
        raise InvalidPageException('Negative page does not exist.')

    albums = repo.get_albums()

     # Find the start index of the albums for the current page.
    start_index = page_index * albums_per_page
    if start_index >= len(albums):
        raise InvalidPageException('The page does not exist.')
        
    # Retrieve albums list for the curent page
    albums_for_page = albums[start_index:start_index+albums_per_page]
    return albums_to_dict(albums_for_page, start_index)


def get_album(album_id: int, repo: AbstractRepository) -> dict:
    album = repo.get_album(album_id)
    if album is None:
        raise NonExistentAlbumException

    # Convert album to album dict
    album_dict = album_to_dict(album)

    # List of tracks of this album
    album_tracks = repo.get_tracks_by_album(album_id)
    # Convert tracks to track dicts
    album_track_dicts = tracks_services.tracks_to_dicts(album_tracks)
    # Insert tracks as its attribute so that the album page can display its tracks
    album_dict['tracks'] = album_track_dicts
    return album_dict


def album_to_dict(album: Album, index: int = None)->dict:
    album_dict = {
        'album_id': album.album_id,
        'title': album.title,
        'album_url': album.album_url,
        'release_year': album.release_year,
        'album_type': album.album_type,
        'index': index
    }
    return album_dict

def albums_to_dict(albums: List[Album], start_index: int)-> List[dict]:
    return [album_to_dict(album, start_index + index) for index, album in enumerate(albums)]
