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
    else:
        print('DATABASE MODE POPULATE')
        albums_dict = reader.read_albums_file_as_dict()
        track_rows = reader.read_tracks_file()

        album_tracks = dict()
        artist_tracks = dict()
        genre_tracks = dict()

        for track_row in track_rows:
            track = create_track_object(track_row)

            album_id = int(
                track_row['album_id']) if track_row['album_id'].isdigit() else None
            album = albums_dict[album_id] if album_id in albums_dict else None

            artist = create_artist_object(track_row)

            if album in album_tracks:
                album_tracks[album].append(track.track_id)
            else:
                album_tracks[album] = [track.track_id]

            if artist in artist_tracks:
                artist_tracks[artist].append(track.track_id)
            else:
                artist_tracks[artist] = [track.track_id]

            # Extract track_genres attributes
            track_genres = extract_genres(track_row)
            for genre in track_genres:
                if genre in genre_tracks:
                    genre_tracks[genre].append(track.track_id)
                else:
                    genre_tracks[genre] = [track.track_id]

            repo.add_track(track)

        for artist in artist_tracks:
            if artist is None:
                continue
            for track_id in artist_tracks[artist]:
                track = repo.get_track(track_id)
                track.artist = artist

            repo.add_artist(artist)

        for album in album_tracks:
            if album is None:
                continue
            for track_id in album_tracks[album]:
                track = repo.get_track(track_id)
                track.album = album

            repo.add_album(album)

        for genre in genre_tracks:
            if genre is None:
                continue
            for track_id in genre_tracks[genre]:
                track = repo.get_track(track_id)
                track.add_genre(genre)

            repo.add_genre(genre)
