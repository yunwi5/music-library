from pathlib import Path

from music.adapters.repository import AbstractRepository
from music.adapters.csvdatareader import TrackCSVReader


# Populate the memory repository with the data from the csv files using the csv reader.
def populate(data_path: Path, repo: AbstractRepository, testing: bool = False):
    if testing:
        # Different files for the testing mode.
        albums_filename = str(Path(data_path) / "raw_albums_test.csv")
        tracks_filename = str(Path(data_path) / "raw_tracks_test.csv")
    else:
        albums_filename = str(Path(data_path) / "raw_albums_excerpt.csv")
        tracks_filename = str(Path(data_path) / "raw_tracks_excerpt.csv")

    # Construct a track csv reader class object.
    reader = TrackCSVReader(albums_filename, tracks_filename)

    # Read two csv files tracks and albums csv.
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
