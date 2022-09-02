import abc
from typing import List
from datetime import date

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


# TODO: Need to add more methods as we implement more features.
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
    def get_tracks(self) -> List[Track]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_track(self, track: Track):
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_tracks(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_artists(self) -> list:
        raise NotImplementedError

    @abc.abstractmethod
    def add_artist(self, artist: Artist):
        raise NotImplementedError

    @abc.abstractmethod
    def get_albums(self) -> list:
        raise NotImplementedError

    @abc.abstractmethod
    def add_album(self, album: Album):
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a Review to the repository.

        If the Review doesn't have bidirectional links with an Article and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if review.track is None:
            raise RepositoryException(
                'Review not currently attched to a Track')

    @abc.abstractmethod
    def get_reviews(self) -> List[Review]:
        raise NotImplementedError
