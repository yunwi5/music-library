from pathlib import Path
from music.adapters.repository import AbstractRepository
from music.adapters.csvdatareader import TrackCSVReader


# Populate the memory repository with the data from the csv files using the csv reader.
def populate(data_path: Path, repo: AbstractRepository, testing: bool, database_mode: bool):
    if testing:
        # Different files for the testing mode.
        albums_filename = str(Path(data_path) / "raw_albums_test.csv")
        tracks_filename = str(Path(data_path) / "raw_tracks_test.csv")
    else:
        albums_filename = str(Path(data_path) / "raw_albums_excerpt.csv")
        tracks_filename = str(Path(data_path) / "raw_tracks_excerpt.csv")

    # Construct a track csv reader class object.
    reader = TrackCSVReader(albums_filename, tracks_filename)

    # Populate repository data (including database if it is a database mode)
    populate_repository(reader, repo)

# Populate repository for both memory and database mode
def populate_repository(reader: TrackCSVReader, repo: AbstractRepository):
    # Read two csv files tracks and albums csv.
    reader.read_csv_files()

    albums = reader.dataset_of_albums
    artists = reader.dataset_of_artists
    genres = reader.dataset_of_genres
    tracks = reader.dataset_of_tracks

    # Add albums to the repo
    repo.add_many_albums(albums)

    # Add artists to the repo
    repo.add_many_artists(artists)

    # Add genres to the repo
    repo.add_many_genres(genres)

    # Add tracks to the repo
    repo.add_many_tracks(tracks)
