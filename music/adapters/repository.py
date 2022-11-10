import abc
from typing import List

from music.domainmodel.user import User
from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.review import Review
from music.domainmodel.genre import Genre

repo_instance = None


class RepositoryException(Exception):
    def __init__(self, message=None):
        print(f'RepositoryException: {message}')


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        """ Returns the User named user_name from the repository.

        If there is no User with the given user_name, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks(self, sorting: bool) -> List[Track]:
        """ Returns the list of tracks. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_track(self, track_id: int) -> Track:
        """ Reutrns the track of the parameter track_id.
        If the track of the specified track_id does not exist, returns None. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_track(self, track: Track):
        """ Add a track to the repository list of tracks. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_tracks(self):
        """ Returns a number of tracks exist in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks_by_album(self, album_id: int)->List[Album]:
        """ Return a list of tracks associated with the album of the param id. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_artists(self) -> list:
        """ Returns artists as a list from the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_artist(self, artist: Artist):
        """ Add an artist to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_albums(self, sorting: bool) -> list:
        """ Returns albums as a list from the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_album(self, album_id: int) -> Album:
        """ Return a specific album of the album_id param from the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_album(self, album: Album):
        """ Add an album to the repository. """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_number_of_albums(self)->int:
        """ Return the number of albums in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self, genre: Genre) -> List[Genre]:
        """ Return all genres that exist in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        """ Add a genre to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a Review to the repository.
        If the Review doesn't have a link to the track, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if review.track is None:
            raise RepositoryException(
                'Review not currently attched to a Track')

    @abc.abstractmethod
    def get_reviews_for_track(self, track_id: str) -> List[Review]:
        """ Receives track_id, and searches for reviews for the track of this id.
        Returns a list of reviews for this track as a list. """
        raise NotImplementedError

    @abc.abstractmethod
    def search_tracks_by_artist(self, artist_name: str) -> List[Track]:
        """Search for the tracks whose artist contains the input artist_name string.
        It searches for artist names in case-insensitive and without trailing spaces.
        Returns searched tracks as a list
        """
        raise NotImplementedError

    @abc.abstractmethod
    def search_tracks_by_title(self, title_string: str) -> List[Track]:
        """Search for the tracks whose title includes the parameter title_string.
        It searches for the track title in case-insensitive and without trailing space.
        For example, the title 'Empire' will be searched if the title_string is 'empir'. """
        raise NotImplementedError

    @abc.abstractmethod
    def search_tracks_by_album(self, album_string: str) -> List[Track]:
        """Search for the tracks of which album contains the input album_name string.
        It searches for album names in case-insensitive and without trailing spaces.
        Returns searched tracks as a list
        """
        raise NotImplementedError

    @abc.abstractmethod
    def search_tracks_by_genre(self, genre_string: str) -> List[Track]:
        """Search for the tracks of which genres contains the input genre_string.
        If any of the track's genres contain the substring genre_string, that track should be selected for the search.
        It searches for genre names in case-insensitive and without trailing spaces.
        Returns searched tracks as a list
        """
        raise NotImplementedError
