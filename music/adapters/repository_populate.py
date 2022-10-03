from operator import ge
from pathlib import Path
from music.adapters.repository import AbstractRepository
from music.adapters.csvdatareader import TrackCSVReader, create_track_object, create_artist_object, extract_genres


# Populate the memory/database repository with the data from the csv files using the csv reader class.
def populate(data_path: Path, repo: AbstractRepository, database_mode: bool):
    albums_filename = str(Path(data_path) / "raw_albums_excerpt.csv")
    tracks_filename = str(Path(data_path) / "raw_tracks_excerpt.csv")

    # Construct a track csv reader class object.
    reader = TrackCSVReader(albums_filename, tracks_filename)

    if database_mode is False:
        populate_memory_repository(reader, repo)

    else:
        populate_database_repository(reader, repo)


# Populate repository for memory_database mode
def populate_memory_repository(reader: TrackCSVReader, repo: AbstractRepository):
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


# Populate repository for dataabase_database mode
def populate_database_repository(reader: TrackCSVReader, repo: AbstractRepository):
    print('DATABASE MODE POPULATE')
    albums_dict = reader.read_albums_file_as_dict()
    track_rows = reader.read_tracks_file()

    # Key is album object, and value is the list of tracks that the key album is associated with.
    album_tracks = dict()
    # Key is artist object, and value is the list of tracks that the key artist is associated with.
    artist_tracks = dict()
    # Key is genre object, and value is the list of tracks that the key genre is associated with.
    genre_tracks = dict()
    # List of all tracks (2000 tracks for the current dataset)
    tracks = []

    for track_row in track_rows:
        track = create_track_object(track_row)
        tracks.append(track)

        album_id = int(
            track_row['album_id']) if track_row['album_id'].isdigit() else None
        album = albums_dict[album_id] if album_id in albums_dict else None

        artist = create_artist_object(track_row)

        if album is not None:
            if album in album_tracks:
                album_tracks[album].append(track.track_id)
            else:
                album_tracks[album] = [track.track_id]

        if artist is not None:
            if artist in artist_tracks:
                artist_tracks[artist].append(track.track_id)
            else:
                artist_tracks[artist] = [track.track_id]

        # Extract track_genres attributes
        track_genres = extract_genres(track_row)
        for genre in track_genres:
            if genre is not None:
                if genre in genre_tracks:
                    genre_tracks[genre].append(track.track_id)
                else:
                    genre_tracks[genre] = [track.track_id]

        repo.add_many_tracks(tracks)

        for artist in artist_tracks:
            if artist is None:
                continue
            for track_id in artist_tracks[artist]:
                track = repo.get_track(track_id)
                track.artist = artist

        repo.add_many_artists(artist_tracks.keys())

        for album in album_tracks:
            if album is None:
                continue
            for track_id in album_tracks[album]:
                track = repo.get_track(track_id)
                track.album = album

        repo.add_many_albums(album_tracks.keys())

        for genre in genre_tracks:
            if genre is None:
                continue
            for track_id in genre_tracks[genre]:
                track = repo.get_track(track_id)
                track.add_genre(genre)

        repo.add_many_genres(genre_tracks.keys())
