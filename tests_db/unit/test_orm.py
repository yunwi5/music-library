import pytest
from sqlalchemy.exc import IntegrityError


from music.domainmodel.user import User


def insert_user(empty_session, values=None):
    new_name = "Denis"
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


def insert_track(empty_session):
    pass


def insert_genres(empty_session):
    pass


def insert_track_genre_associations(empty_session, track_keys, genre_keys):
    pass


def insert_album(empty_session):
    pass


def insert_artist(empty_session):
    pass


def insert_review(empty_session):
    pass


def make_track():
    pass


def make_user():
    pass


def make_genre():
    pass


def make_album():
    pass


def make_artist():
    pass


def make_review():
    pass


def test_loading_of_users(empty_session):
    users = list()
    users.append(("Denis", "denis98989"))
    users.append(("Cindy", "1111"))
    insert_users(empty_session, users)

    expected = [
        User("Denis", "denis98989"),
        User("Cindy", "999")
    ]
    assert empty_session.query(User).all() == expected


def test_saving_of_users(empty_session):
    pass


def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session, ("Denis", "denis98989"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("Denis", "111")
        empty_session.add(user)
        empty_session.commit()


def test_loading_of_artists(empty_session):
    pass


def test_saving_of_artists(empty_session):
    pass


def test_loading_of_albums(empty_session):
    pass


def test_saving_of_albums(empty_session):
    pass


def test_loading_of_tracks(empty_session):
    pass


def test_loading_of_tracks_with_genres(empty_session):
    pass


def test_loading_of_tracks_with_reviews(empty_session):
    pass


def test_saving_of_reviews(empty_session):
    pass


def test_saving_of_track(empty_session):
    pass


def test_saving_of_tracks_with_genres(empty_session):
    pass


def test_saving_of_tracks_with_reviews(empty_session):
    pass
