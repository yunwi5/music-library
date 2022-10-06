from datetime import date, datetime
import pytest

import music.adapters.repository as repo
from music.adapters.database_repository import SqlAlchemyRepository
from music.domainmodel.user import User, Track
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review
from music.adapters.repository import RepositoryException


def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Gabriel', '123456789')
    repo.add_user(user)

    repo.add_user(User('Martin', '123456789'))

    user2 = repo.get_user('Gabriel')
    assert user2 == user and user2 is user


def test_repository_can_get_Tracks(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    tracks = repo.get_tracks()
    assert len(tracks) == 10
