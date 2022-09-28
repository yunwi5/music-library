from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session

from music.adapters.utils import search_string
from music.adapters.repository import AbstractRepository
from music.domainmodel.user import User
from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.review import Review
from music.domainmodel.genre import Genre


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, user_name: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(
                User._User__user_name == user_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def get_tracks(self) -> List[Track]:
        tracks = self._session_cm.session.query(Track).all()
        return tracks

    def get_track(self, track_id: int) -> Track:
        track = None
        try:
            track = self._session_cm.session.query(
                Track).filter(Track._Track__track_id == track_id).one()
        except NoResultFound:
            print(f'Track {track_id} was not found')
            pass

        return track

    def add_track(self, track: Track):
        with self._session_cm as scm:
            scm.session.add(track)
            scm.commit()

    def get_number_of_tracks(self) -> List[Track]:
        num_tracks = self._session_cm.session.query(Track).count()
        return num_tracks

    def get_artists(self) -> List[Artist]:
        artists = self._session_cm.session.query(Artist).all()
        return artists

    def add_artist(self, artist: Artist):
        with self._session_cm as scm:
            scm.session.add(artist)
            scm.commit()

    def get_albums(self) -> List[Album]:
        albums = self._session_cm.session.query(Album).all()
        return albums

    def add_album(self, album: Album):
        with self._session_cm as scm:
            scm.session.add(album)
            scm.commit()

    def get_genres(self) -> List[Genre]:
        genres = self._session_cm.session.query(Genre).all()
        return genres

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.add(genre)
            scm.commit()

    def add_review(self, review: Review):
        super().add_review(review)
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def get_reviews_for_track(self, track_id: str) -> List[Track]:
        track = self.get_track(track_id)
        reviews = self._session_cm.session.query(Review).filter(
            Review._Review__track == track).all()
        return reviews

    def search_tracks_by_title(self, title_string: str) -> List[Track]:
        """Search for the tracks whose title includes the parameter title_string.
        It searches for the track title in case-insensitive and without trailing space.
        For example, the title 'Empire' will be searched if the title_string is 'empir'. """
        return []

    def search_tracks_by_artist(self, artist_name: str) -> List[Track]:
        tracks = self._session_cm.session.query(Track).all()
        searched_tracks = list(filter(lambda track: search_string(
            track.artist.full_name if track.artist is not None else '', artist_name), tracks))

        return searched_tracks

    def search_tracks_by_album(self, album_string: str) -> List[Track]:
        """Search for the tracks of which album contains the input album_name string.
        It searches for album names in case-insensitive and without trailing spaces.
        Returns searched tracks as a list
        """
        return []

    def search_tracks_by_genre(self, genre_string: str) -> List[Track]:
        """Search for the tracks of which genres contains the input genre_string.
        If any of the track's genres contain the substring genre_string, that track should be selected for the search.
        It searches for genre names in case-insensitive and without trailing spaces.
        Returns searched tracks as a list
        """
        return []
