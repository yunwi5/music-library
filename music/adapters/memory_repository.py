from pathlib import Path
from typing import List
from bisect import insort_left

from werkzeug.security import generate_password_hash

from music.adapters.repository import AbstractRepository
from music.adapters.csvdatareader import TrackCSVReader
from music.domainmodel.user import User
from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.review import Review
from music.domainmodel.genre import Genre


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__users = list()
        self.__tracks = list()
        self.__artists = set()
        self.__albums = set()
        self.__genres = set()
        self.__reviews = list()

    def add_user(self, user: User):
        self.__users.append(user)
        print('New users:', self.__users)

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)

    def get_track(self, track_id: int) -> Track:
        # Get a specific track by id
        return next((track for track in self.__tracks if track.track_id == track_id), None)

    def get_tracks(self) -> List[Track]:
        return self.__tracks

    def add_track(self, track: Track):
        # When inserting the track, keep the track list sorted alphabetically by the title.
        insort_left(self.__tracks, track, key=lambda t: t.title)

    def get_number_of_tracks(self):
        return len(self.__tracks)

    def get_artists(self) -> list:
        return list(self.__artists)

    def add_artist(self, artist: Artist):
        self.__artists.add(artist)

    def get_albums(self) -> list:
        return list(self.__albums)

    def add_album(self, album: Album):
        self.__albums.add(album)

    def add_genre(self, genre: Genre):
        self.__genres.add(genre)

    def add_review(self, review: Review):
        # call parent class first, add_review relies on implementation of code common to all derived classes
        super().add_review(review)
        self.__reviews.append(review)

    def get_reviews_for_track(self, track_id: str) -> List[Track]:
        # Get reviews for track. Select reviews that have a track and its track_id matches the input track_id
        track_reviews = [
            review for review in self.__reviews if review.track and review.track.track_id == track_id]
        return track_reviews

    def seach_tracks_by_artist(self, artist_name: str):
        searched_tracks = list(filter(lambda track: search_string(
            track.artist.full_name if track.artist is not None else '', artist_name), self.__tracks))

        return searched_tracks

    def search_tracks_by_album(self, album_string: str):
        searched_tracks = list(filter(lambda track: search_string(
            track.album.title if track.album is not None else '', album_string), self.__tracks))

        return searched_tracks

    def search_tracks_by_genre(self, genre_string: str):
        searched_tracks = []
        for track in self.__tracks:

            contained = False
            for genre in track.genres:
                if search_string(genre.name, genre_string):
                    contained = True

            if contained:
                searched_tracks.append(track)

        return searched_tracks


# Case insensitive search
def search_string(name: str, substring: str):
    return substring.strip().lower() in name.lower()

# Populate the memory repository with the data from the csv files using the csv reader.


def populate(data_path: Path, repo: MemoryRepository):

    albums_filename = str(Path(data_path) / "raw_albums_excerpt.csv")
    tracks_filename = str(Path(data_path) / "raw_tracks_excerpt.csv")
    reader = TrackCSVReader(albums_filename, tracks_filename)

    reader.read_csv_files()

    albums = reader.dataset_of_albums
    artists = reader.dataset_of_artists
    genres = reader.dataset_of_genres
    tracks = reader.dataset_of_tracks

    # Add albums to the repo
    for album in albums:
        repo.add_album(album)

    # Add artists to the repo
    for artist in artists:
        repo.add_artist(artist)

    # Add genres to the repo
    for genre in genres:
        repo.add_genre(genre)

    # Add tracks to the repo
    for track in tracks:
        repo.add_track(track)
