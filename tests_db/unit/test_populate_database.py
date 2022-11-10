from sqlalchemy import select, inspect
from music.adapters.orm import metadata


def test_database_populate_inspect_table_names(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    tables = inspector.get_table_names()

    # Check all required tables are there
    assert 'tracks' in tables
    assert 'albums' in tables
    assert 'artists' in tables
    assert 'genres' in tables
    assert 'users' in tables
    assert 'reviews' in tables
    assert 'track_genres' in tables

    assert inspector.get_table_names(
    ) == ['albums', 'artists', 'genres', 'reviews', 'track_genres', 'tracks', 'users']


def test_database_populate_all_tracks(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    # tracks table is at index 5 alphabetically
    tracks_table_name = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        # query for records in table tracks
        select_statement = select([metadata.tables[tracks_table_name]])
        result = connection.execute(select_statement)

        tracks = []
        for row in result:
            tracks.append((row['track_id'], row['title']))

        nr_tracks = len(tracks)
        assert nr_tracks == 10

        # First row is track 'Food' of track_id 2.
        assert tracks[0] == (2, 'Food')


def test_database_populate_all_albums(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    # albums table is at index 0 alphabetically
    tracks_table_name = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        # query for records in table albums
        select_statement = select([metadata.tables[tracks_table_name]])
        result = connection.execute(select_statement)

        albums = []
        for row in result:
            albums.append((row['album_id'], row['title']))

        nr_albums = len(albums)
        assert nr_albums == 5

        # Check the first row of the table
        assert albums[0] == (1, 'AWOL - A Way Of Life')


def test_database_populate_all_artists(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    # artists table is at index 1 alphabetically
    tracks_table_name = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        # query for records in table artists
        select_statement = select([metadata.tables[tracks_table_name]])
        result = connection.execute(select_statement)

        artists = []
        for row in result:
            artists.append((row['artist_id'], row['full_name']))

        nr_artists = len(artists)
        assert nr_artists == 5

        # Check the first row of the table
        assert artists[0] == (1, 'AWOL')


def test_database_populate_all_genres(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    # genres table is at index 2 alphabetically
    tracks_table_name = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # query for records in table genres
        select_statement = select([metadata.tables[tracks_table_name]])
        result = connection.execute(select_statement)

        genres = []
        for row in result:
            genres.append((row['genre_id'], row['name']))

        nr_genres = len(genres)
        # There are total 7 genres in the test dataset
        assert nr_genres == 7

        # Check the first row of the table
        assert genres[0] == (1, 'Avant-Garde')


def test_database_populate_track_genres(database_engine):
    # Test population of association table track_genres
    # track_genres resolve M-t-M relationship between tracks and genres
    # It has track_id to store ref to the track, and genre_id to store ref to the genre

    # Get table information
    inspector = inspect(database_engine)
    # track_genres table is at index 4 alphabetically
    tracks_table_name = inspector.get_table_names()[4]

    with database_engine.connect() as connection:
        # query for records in table genres
        select_statement = select([metadata.tables[tracks_table_name]])
        result = connection.execute(select_statement)

        track_genres = []
        for row in result:
            track_genres.append((row['track_id'], row['genre_id']))

        # Check the first row of the table
        assert track_genres[0] == (2, 21)
