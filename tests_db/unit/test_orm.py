import pytest
from sqlalchemy.exc import IntegrityError


from music.domainmodel.user import User
from music.domainmodel.track import Track
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review


def make_user() -> User:
    return User('denis', 'denis98989')


def make_track() -> Track:
    track = Track(2, "Shivers")
    track.track_url = 'http://freemusicarchive.org/music/shivers'
    track.track_duration = 200
    track.album = make_album()
    track.artist = make_artist()
    return track


def make_genre() -> Genre:
    genre = Genre(1, 'Pop')
    return genre


def make_album() -> Album:
    album = Album(1, '=')
    album.album_url = 'http://freemusicarchive.org/music/albums/='
    album.album_type = 'Album'
    album.release_year = 2022
    return album


def make_artist():
    artist = Artist(1, 'Ed Sheeran')
    return artist


def make_review():
    track = make_track()
    review = Review(track, 'Denis\'s review', 5)
    review.user = make_user()
    return review


def insert_user(empty_session, values=None):
    new_name = "denis"
    new_password = "denis98989"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                          {'user_name': new_name, 'password': new_password})
    row = empty_session.execute('SELECT user_id from users where user_name = :user_name',
                                {'user_name': new_name}).fetchone()
    return row[0]


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                              {'user_name': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT user_id from users'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_track(empty_session, track: Track):
    empty_session.execute(
        'INSERT INTO tracks (track_id, title, track_url, track_duration) VALUES '
        f'({track.track_id}, "{track.title}", '
        f'"{track.track_url}", {track.track_duration})'
    )
    row = empty_session.execute('SELECT track_id from tracks').fetchone()
    return row[0]


def insert_genres(empty_session):
    empty_session.execute(
        'INSERT INTO genres (genre_id, name) VALUES (1, "Hip-Hop"), (2, "Rap")'
    )
    rows = list(empty_session.execute('SELECT genre_id from genres'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_track_genre_associations(empty_session, track_key, genre_keys):
    stmt = 'INSERT INTO track_genres (track_id, genre_id) VALUES (:track_id, :genre_id)'
    for genre_key in genre_keys:
        empty_session.execute(
            stmt, {'track_id': track_key, 'genre_id': genre_key})


def insert_reviewed_track(empty_session, review: Review):
    track_key = insert_track(empty_session, review.track)
    user_key = insert_user(
        empty_session, (review.user.user_name, review.user.password))

    timestamp_format = review.timestamp.strftime('%Y-%m-%d %H:%M:%S')

    empty_session.execute(
        'INSERT INTO reviews (user_id, track_id, review_text, rating, timestamp) VALUES '
        f'({user_key}, {track_key}, "{review.review_text}", {review.rating}, "{timestamp_format}")'
    )

    review_key = empty_session.execute(
        'SELECT review_id FROM reviews').fetchone()

    return track_key, review_key


def insert_album(empty_session, album: Album):
    empty_session.execute(
        'INSERT INTO albums (album_id, title, album_url, album_type, release_year) VALUES '
        f'({album.album_id}, "{album.title}", '
        f'"{album.album_url}", "{album.album_type}", {album.release_year})'
    )
    row = empty_session.execute('SELECT album_id from albums').fetchone()
    return row[0]


def insert_artist(empty_session, artist: Artist):
    empty_session.execute(
        'INSERT INTO artists (artist_id, full_name) VALUES '
        f'({artist.artist_id}, "{artist.full_name}")'
    )
    row = empty_session.execute('SELECT artist_id from artists').fetchone()
    return row[0]


def test_loading_of_users(empty_session):
    users = list()
    users.append(("denis", "denis98989"))
    users.append(("roger", "roger78787"))
    insert_users(empty_session, users)

    expected = [
        User("denis", "denis98989"),
        User("roger", "roger78787")
    ]
    assert empty_session.query(User).all() == expected


def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_name, password FROM users'))
    assert rows == [(user.user_name, user.password)]


def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session, ("denis", "denis98989"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("denis", "denis090909")
        empty_session.add(user)
        empty_session.commit()


def test_loading_of_artists(empty_session):
    artist = make_artist()
    artist_key = insert_artist(empty_session, artist)
    fetched_album = empty_session.query(Artist).one()

    # Confirm the fetched artist has the same id as expected
    assert artist_key == fetched_album.artist_id
    # Test the fetched artist is identical to the artist we created in advance
    assert artist == fetched_album


def test_saving_of_artist(empty_session):
    artist = make_artist()
    empty_session.add(artist)
    empty_session.commit()

    # Fetch the artist we just added
    rows = list(empty_session.execute(
        'SELECT artist_id, full_name FROM artists'))

    # Confirm all the artist attributes were saved successfully
    assert rows == [(artist.artist_id, artist.full_name)]


def test_artist_track_relationship(empty_session):
    # Test one-to-many relationship between Artist and Track
    artist = make_artist()
    track = make_track()
    # make_track() function already establishes relationship between the sample Track and Artist.
    # However, set artist object explicitly here to make sure they have the relationship we expect.
    track.artist = artist

    # Add the Track object (and artist).
    # Note that persisting either one will persist the other.
    empty_session.add(track)
    empty_session.commit()

    rows = list(empty_session.execute(
        'SELECT track_id, artist_id FROM tracks'))
    assert rows == [(track.track_id, artist.artist_id)]


def test_loading_of_albums(empty_session):
    album = make_album()
    album_key = insert_album(empty_session, album)
    fetched_album = empty_session.query(Album).one()

    # Confirm the fetched album has the same id as expected
    assert album_key == fetched_album.album_id
    # Test the fetched album is identical to the album we created in advance
    assert album == fetched_album


def test_saving_of_albums(empty_session):
    album = make_album()
    empty_session.add(album)
    empty_session.commit()

    # Fetch the album we just added
    rows = list(empty_session.execute(
        'SELECT album_id, title, album_url, album_type, release_year FROM albums'))

    # Confirm all the album attributes were saved successfully
    assert rows == [(album.album_id, album.title, album.album_url,
                     album.album_type, album.release_year)]


def test_album_track_relationship(empty_session):
    # Test one-to-many relationship between Album and Track
    album = make_album()
    track = make_track()
    # make_track() function already establishes relationship between the sample Track and Album.
    # However, set album object explicitly here again to make sure they have the relationship we expect.
    track.album = album

    # Add the Track object (and album).
    # Note that persisting either one will persist the other.
    empty_session.add(track)
    empty_session.commit()

    rows = list(empty_session.execute(
        'SELECT track_id, album_id FROM tracks'))
    assert rows == [(track.track_id, album.album_id)]


def test_loading_of_track(empty_session):
    track = make_track()
    track_key = insert_track(empty_session, track)
    fetched_track = empty_session.query(Track).one()

    # Confirm the fetched track has the same track_id as expected
    assert track_key == fetched_track.track_id
    # Test the fetched track is identical to the track we created in advance
    assert track == fetched_track


def test_saving_of_track(empty_session):
    track = make_track()
    empty_session.add(track)
    empty_session.commit()

    rows = list(empty_session.execute(
        'SELECT title, track_url, track_duration, artist_id, album_id FROM tracks'))

    # Confirm all the track attributes were saved successfully including artist_id and album_id foreign keys
    assert rows == [(track.title, track.track_url, track.track_duration,
                     track.artist.artist_id, track.album.album_id)]


def test_loading_of_tracks_with_genres(empty_session):
    track = make_track()
    track_key = insert_track(empty_session, track)
    genre_keys = insert_genres(empty_session)
    insert_track_genre_associations(empty_session, track_key, genre_keys)

    fetched_track = empty_session.query(Track).get(track_key)
    fetched_genres = [empty_session.query(
        Genre).get(key) for key in genre_keys]

    for genre in fetched_genres:
        assert genre in fetched_track.genres


def test_saving_of_tracks_with_genres(empty_session):
    track = make_track()
    genre = make_genre()

    # Establish the relationship between track and genre.
    track.add_genre(genre)

    # Persist the track and genre.name
    # Note: it doesn't matter whether we add the Track or the Genre.
    # They are connected bidirectionally, so persisting either one will persist the other.
    empty_session.add(track)
    empty_session.commit()

    # Check that the tracks table has a new record.
    rows = list(empty_session.execute('SELECT track_id FROM tracks'))
    track_key = rows[0][0]

    # Check that the genres table has a new record.
    rows = list(empty_session.execute('SELECT genre_id, name FROM genres'))
    genre_key = rows[0][0]
    assert rows == [(genre.genre_id, genre.name)]

    # Check that the track_genres table has a new record.
    rows = list(empty_session.execute(
        'SELECT track_id, genre_id from track_genres'))
    track_foreign_key = rows[0][0]
    genre_foreign_key = rows[0][1]

    # Check that the track_id and genre_id foreign keys match the initial track and genre objects we created.
    assert track_key == track_foreign_key
    assert genre_key == genre_foreign_key


def test_loading_of_tracks_with_reviews(empty_session):
    review = make_review()
    insert_reviewed_track(empty_session, review)

    # Get the Track object we just inserted.
    track_rows = empty_session.query(Track).all()
    track = track_rows[0]

    # Get the Review object we just inserted.
    review_rows = empty_session.query(Review).all()
    review = review_rows[0]

    # Confirm that the fetched review object has the correct
    # track object populated
    assert review.track == track


def test_saving_of_tracks_with_reviews(empty_session):
    # Create track, user and review objects
    # make_review() function automatically creates track and user objects and
    # make associations with the review.
    review = make_review()

    # Add and save the new track
    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT track_id FROM tracks'))
    track_key = rows[0][0]

    rows = list(empty_session.execute('SELECT user_id FROM users'))
    user_key = rows[0][0]

    # Check that the reviews table has a new record that
    # links to the tracks and users tables.
    rows = list(empty_session.execute(
        'SELECT user_id, track_id, review_text, rating FROM reviews'))
    assert rows == [(user_key, track_key, review.review_text, review.rating)]
