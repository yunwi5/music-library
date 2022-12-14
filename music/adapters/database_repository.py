from typing import List

# from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import scoped_session

from music.adapters.repository import AbstractRepository
from music.adapters.utils import search_string, sort_entities_by_title
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
        # Need to handle the case where user.user_name is not unique.
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, user_name: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(
                User._User__user_name == user_name.strip().lower()).one()
        except NoResultFound:
            # Ignore any exception and return None.
            print(f'User {user_name} was not found')
        return user

    def get_tracks(self, sorting: bool = False) -> List[Track]:
        tracks = self._session_cm.session.query(Track).all()
        if not sorting:
            return tracks
        return sort_entities_by_title(tracks)

    def get_track(self, track_id: int) -> Track:
        track = None
        try:
            track = self._session_cm.session.query(
                Track).filter(Track._Track__track_id == track_id).one()
        except NoResultFound:
            print(f'Track {track_id} was not found')

        return track

    def add_track(self, track: Track):
        with self._session_cm as scm:
            scm.session.merge(track)
            scm.commit()

    def add_many_tracks(self, tracks: List[Track]):
        with self._session_cm as scm:
            for track in tracks:
                scm.session.merge(track)
            scm.commit()

    def get_number_of_tracks(self) -> List[Track]:
        num_tracks = self._session_cm.session.query(Track).count()
        return num_tracks

    def get_tracks_by_album(self, album_id: int)->List[Album]:
        album = self.get_album(album_id)
        album_tracks = self._session_cm.session.query(Track).filter(
            Track._Track__album == album).all()
        return album_tracks

    def get_artists(self) -> List[Artist]:
        artists = self._session_cm.session.query(Artist).all()
        return artists

    def add_artist(self, artist: Artist):
        with self._session_cm as scm:
            scm.session.merge(artist)
            scm.commit()

    def add_many_artists(self, artists: List[Artist]):
        with self._session_cm as scm:
            for artist in artists:
                scm.session.merge(artist)
            scm.commit()

    def get_album(self, album_id: int)-> Album:
        # Get a specific album by id
        album = None
        try:
            album = self._session_cm.session.query(
                Album).filter(Album._Album__album_id == album_id).one()
        except NoResultFound:
            print(f'Album {album_id} was not found')

        return album

    def get_albums(self, sorting: bool = False) -> List[Album]:
        albums = self._session_cm.session.query(Album).all()
        if not sorting:
            return albums
        return sort_entities_by_title(albums)

    def add_album(self, album: Album):
        with self._session_cm as scm:
            scm.session.merge(album)
            scm.commit()

    def add_many_albums(self, albums: List[Album]):
        with self._session_cm as scm:
            for album in albums:
                scm.session.merge(album)
            scm.commit()

    def get_number_of_albums(self) -> int:
        num_albums = self._session_cm.session.query(Album).count()
        return num_albums

    def get_genres(self) -> List[Genre]:
        genres = self._session_cm.session.query(Genre).all()
        return genres

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.merge(genre)
            scm.commit()

    def add_many_genres(self, genres: List[Genre]):
        with self._session_cm as scm:
            for genre in genres:
                scm.session.merge(genre)
            scm.commit()

    def add_review(self, review: Review):
        super().add_review(review)
        with self._session_cm as scm:
            scm.session.merge(review)
            scm.commit()

    def get_reviews_for_track(self, track_id: str) -> List[Track]:
        track = self.get_track(track_id)
        reviews = self._session_cm.session.query(Review).filter(
            Review._Review__track == track).all()
        return reviews

    def search_tracks_by_title(self, title_string: str) -> List[Track]:
        tracks = self._session_cm.session.query(Track).all()
        searched_tracks = list(filter(lambda track: search_string(
            track.title if track.title is not None else '', title_string), tracks))
        return searched_tracks

    def search_tracks_by_artist(self, artist_name: str) -> List[Track]:
        tracks = self._session_cm.session.query(Track).all()
        searched_tracks = list(filter(lambda track: search_string(
            track.artist.full_name if track.artist is not None else '', artist_name), tracks))

        return searched_tracks

    def search_tracks_by_album(self, album_string: str) -> List[Track]:
        tracks = self._session_cm.session.query(Track).all()
        searched_tracks = list(filter(lambda track: search_string(
            track.album.title if track.album is not None else '', album_string), tracks))
        return searched_tracks

    def search_tracks_by_genre(self, genre_string: str) -> List[Track]:
        tracks = self._session_cm.session.query(Track).all()

        searched_tracks = []
        for track in tracks:
            for genre in track.genres:
                if search_string(genre.name, genre_string):
                    searched_tracks.append(track)
                    break

        return searched_tracks
