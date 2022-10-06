import pytest
from sqlalchemy.exc import IntegrityError


from music.domainmodel.user import User


def insert_user(empty_session, values=None):
    new_name = "Andrew"
    new_password = "1234"

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


# def test_loading_of_users(empty_session):
#     users = list()
#     users.append(("Andrew", "1234"))
#     users.append(("Cindy", "1111"))
#     insert_users(empty_session, users)

#     expected = [
#         User("Andrew", "1234"),
#         User("Cindy", "999")
#     ]
#     assert empty_session.query(User).all() == expected
