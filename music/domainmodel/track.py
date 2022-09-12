from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.album import Album


class Track:
    def __init__(self, track_id: int, track_title: str):
        if type(track_id) is not int or track_id < 0:
            raise ValueError
        self.__track_id = track_id

        self.__title = None
        if type(track_title) is str:
            self.__title = track_title.strip()

        self.__artist = None
        self.__album: Album | None = None
        self.__track_url: str | None = None
        # duration in seconds
        self.__track_duration: int | None = None
        self.__genres: list = []

    @property
    def track_id(self) -> int:
        return self.__track_id

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, book_title: str):
        self.__title = None
        if type(book_title) is str and book_title.strip() != '':
            self.__title = book_title.strip()

    @property
    def artist(self) -> Artist:
        return self.__artist

    @artist.setter
    def artist(self, new_artist):
        if isinstance(new_artist, Artist):
            self.__artist = new_artist
        else:
            self.__artist = None

    @property
    def album(self) -> Album:
        return self.__album

    @album.setter
    def album(self, new_album):
        if isinstance(new_album, Album):
            self.__album = new_album
        else:
            self.__album = None

    @property
    def track_url(self) -> str:
        return self.__track_url

    @track_url.setter
    def track_url(self, new_track_url: str):
        if type(new_track_url) is str:
            self.__track_url = new_track_url.strip()
        else:
            self.__track_url = None

    @property
    def track_duration(self) -> int:
        return self.__track_duration

    @track_duration.setter
    def track_duration(self, new_duration: int):
        self.__track_duration = None
        if type(new_duration) is int and new_duration >= 0:
            self.__track_duration = new_duration
        else:
            raise ValueError

    @property
    def genres(self) -> list:
        return self.__genres

    def add_genre(self, new_genre):
        if not isinstance(new_genre, Genre) or new_genre in self.__genres:
            return
        self.__genres.append(new_genre)

    def __repr__(self):
        return f"<Track {self.title}, track id = {self.track_id}>"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.track_id == other.track_id

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return True

        # Check non-empty title exists in either track first to prevent errors when calling string methods.
        if other.title is None or len(other.title) == 0:
            return True
        if self.title is None or len(self.title) == 0:
            return False

        # In ASCII, numeric characters and special characters come before alphabetical characteres in ordering.
        # However, in this application, titles starting with alphabets should come first in ordering.
        if self.title[0].isalpha() and other.title[0].isalpha():
            return self.title.strip().lower() < other.title.strip().lower()
        elif self.title[0].isalpha():
            return True
        elif other.title[0].isalpha():
            return False
        else:
            return self.title.strip().lower() < other.title.strip().lower()

    def __hash__(self):
        return hash(self.track_id)
