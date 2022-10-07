from datetime import date, datetime
import pytest

# import music.adapters.repository as repo
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

    user2 = repo.get_user('Gabriel')
    assert user2 == user and user2 is user


def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('denis', 'Denis9389')
    repo.add_user(user)

    # Retrieving an added user should return the correct object
    user2 = repo.get_user('denis')
    assert user2 == user

    # Retrieving user is case-insensitive without trailing spaces.
    user2 = repo.get_user(' Denis ')
    assert user2 == user


def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # Retrieving unknown user should return None
    user1 = repo.get_user('maximilian')
    assert user1 == None


def test_repository_can_get_Tracks(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    tracks = repo.get_tracks()
    assert len(tracks) == 10


def test_repository_can_add_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track = Track(5001, 'New track 1')
    track2 = Track(5002, 'New track 2')
    repo.add_track(track)
    repo.add_track(track2)

    assert repo.get_track(5001) is track
    assert repo.get_track(5002) is track2


def test_repository_can_retrieve_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track_id = 2
    track = repo.get_track(track_id)

    # Check that the track has the expected title.
    assert track.title == 'Food'

    # Check that the track has expected album.
    assert track.album.title == 'AWOL - A Way Of Life'

    # Check that the track has expected artist.
    assert track.artist.full_name == 'AWOL'

    # Check that the track has expected genre(s).
    # This track is expected to have genre 'Hip-Hop' inside its genre list.
    assert 'Hip-Hop' in [genre.name for genre in track.genres]


def test_repository_does_not_retrieve_a_non_existent_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track = repo.get_track(10201901)  # Non-existing track id
    assert track is None


def test_repository_can_retrieve_track_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    number_of_tracks = repo.get_number_of_tracks()

    # Check that the query returned 10 tracks in the testing file raw_tracks_test.csv.
    assert number_of_tracks == 10


def test_repository_can_retrieve_all_tracks(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # Check that the memory repository has all 10 tracks from csv
    tracks = repo.get_tracks()
    assert len(tracks) == 10


def test_repository_can_add_a_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    genre = Genre(3031, 'New Genre')
    repo.add_genre(genre)

    # Test repo has added a new genre and its number of genre increased from 7 to 8.
    assert len(repo.get_genres()) == 8


def test_repository_can_retrieve_genres(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    genres = repo.get_genres()
    # Test there are total 7 unique genres in the test dataset.
    assert len(genres) == 7


def test_repository_can_add_album(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    album = Album(15212, 'Justice')
    repo.add_album(album)

    # Test repo has a new album inside
    albums = repo.get_albums()
    assert album in albums


def test_repository_can_retrieve_albums(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    albums = repo.get_albums()
    # Test file has total 5 albums
    assert len(albums) == 5


def test_repository_can_add_artist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    artist = Artist(923892, 'A new artist')
    repo.add_artist(artist)

    # Test repo has a new artist inside
    assert artist in repo.get_artists()


def test_repository_can_retrieve_artists(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    artists = repo.get_artists()
    # Test there are total 5 artits inside
    assert len(artists) == 5


def test_repository_can_add_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # Get a sample track
    track_id = 2
    track = repo.get_track(track_id)

    review1 = Review(track, 'My review 1', 5)
    review2 = Review(track, 'My review 2', 1)

    repo.add_review(review1)
    repo.add_review(review2)

    # Retrieve all reviews for this track and test if new reviews exist.
    reviews = repo.get_reviews_for_track(track_id)
    assert review1 in reviews
    assert review2 in reviews

    # Review without track should not be added to repo
    review3 = Review(None, 'My review 3', 2)

    # RepositoryException should be raised if trying to add review without a track
    with pytest.raises(RepositoryException):
        repo.add_review(review3)


def test_repository_can_retrieve_review_for_a_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # Get a sample track
    track_id = 2
    track = repo.get_track(track_id)

    # Initially there are no reviews for a track
    assert len(repo.get_reviews_for_track(track_id)) == 0

    review = Review(track, 'My review 1', 5)
    repo.add_review(review)

    # After adding a review, there should be one review for the track
    assert len(repo.get_reviews_for_track(track_id)) == 1


# Test repository search tracks by title
def test_repository_can_search_tracks_by_title(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # Create sample tracks
    track1 = Track(29149, 'New track 1')
    track2 = Track(2914997, 'New track 2')
    track3 = Track(2914998, 'Random track')

    repo.add_track(track1)
    repo.add_track(track2)
    repo.add_track(track3)

    # Search tracks based on artist name - no extra whitespace and case in-sensitive
    searched_tracks = repo.search_tracks_by_title(
        '  new track  ')
    # Based on the search string, track1 and track2 should be searched, but not track3
    assert sorted(searched_tracks) == [track1, track2]


# Test repository search tracks by artist
def test_repository_can_search_tracks_by_artist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # Create a sample artist for testing purpose
    artist = Artist(2918392, 'New Test Artist')

    # Create sample tests for this artist
    track1 = Track(29149939, 'New track 1')
    track2 = Track(29149940, 'New track 2')
    track3 = Track(29149949, 'Track not by this artist')

    track1.artist = artist
    track2.artist = artist

    repo.add_artist(artist)
    repo.add_track(track1)
    repo.add_track(track2)
    repo.add_track(track3)

    # Search tracks based on artist name - no extra whitespace and case in-sensitive
    searched_tracks = repo.search_tracks_by_artist(
        '  new test artist  ')
    # track1 and track2 should be searched, but not track3
    assert sorted(searched_tracks) == [track1, track2]


# Test repository search tracks by album
def test_repository_can_search_tracks_by_album(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # Create a sample album for testing purpose
    album = Album(2918392, 'New Test Album')

    # Create sample tests for this artist
    track1 = Track(29149939, 'New track 1')
    track2 = Track(29149940, 'New track 2')

    track1.album = album
    track2.album = album

    repo.add_album(album)
    repo.add_track(track1)
    repo.add_track(track2)

    # Search tracks based on album name - no extra whitespace and case-insensitive
    searched_tracks = repo.search_tracks_by_album(' new test album ')
    assert sorted(searched_tracks) == [track1, track2]


# Test repository search tracks by genre name
def test_repository_can_search_tracks_by_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # Create a sample genre for testing purpose
    genre = Genre(2918392, 'New Test Genre')

    # Create sample tests for this artist
    track1 = Track(29149939, 'New track 1')
    track2 = Track(29149940, 'New track 2')

    track1.add_genre(genre)
    track2.add_genre(genre)

    repo.add_genre(genre)
    repo.add_track(track1)
    repo.add_track(track2)

    # Search tracks based on genre name - no extra whitespace and case-insensitive
    searched_tracks = repo.search_tracks_by_genre(' new test genre ')
    assert sorted(searched_tracks) == [track1, track2]
