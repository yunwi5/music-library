import csv
from pathlib import Path
from datetime import date, datetime
from typing import List
from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from music.adapters.repository import AbstractRepository, RepositoryException
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
        self.__tracks_index = dict()

    def add_user(self, user: User):
        self.__users.append(user)
        print('New users:', self.__users)

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)

    def get_tracks(self) -> List[Track]:
        return self.__tracks

    def add_track(self, track: Track):
        insort_left(self.__tracks, track)
        self.__tracks_index[track.track_id] = track

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

    def get_reviews(self) -> List[Review]:
        return self.__reviews


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

    # print('Num artists:', len(artists))
    # print('Num albums:', len(albums))
    # print('Num tracks:', len(tracks))
    # print('Num genres:', len(genres))

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
