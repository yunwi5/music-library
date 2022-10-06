import pytest

from music.adapters.repository import RepositoryException
from music.adapters.memory_repository import MemoryRepository
from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.user import User
from music.domainmodel.review import Review
from music.domainmodel.genre import Genre


def test_repository_can_add_a_user(memory_repo: MemoryRepository):
    user = User('denis', 'Denis9389')
    memory_repo.add_user(user)

    assert memory_repo.get_user('denis') is user


def test_repository_can_retrieve_a_user(memory_repo: MemoryRepository):
    user = User('denis', 'Denis9389')
    memory_repo.add_user(user)

    # Retrieving an added user should return the correct object
    user2 = memory_repo.get_user('denis')
    assert user2 == user

    # Retrieving user is case-insensitive without trailing spaces.
    user2 = memory_repo.get_user(' Denis ')
    assert user2 == user


def test_repository_does_not_retrieve_a_non_existent_user(memory_repo: MemoryRepository):
    # Retrieving unknown user should return None
    user1 = memory_repo.get_user('maximilian')
    assert user1 == None


def test_repository_can_add_track(memory_repo: MemoryRepository):
    article = Track(5001, 'My new track 101')
    memory_repo.add_track(article)

    assert memory_repo.get_track(5001) is article


def test_repository_can_retrieve_track(memory_repo: MemoryRepository):
    track_id = 2
    track = memory_repo.get_track(track_id)

    # Check that the track has the expected title.
    assert track.title == 'Food'

    # Check that the track has expected album.
    assert track.album.title == 'AWOL - A Way Of Life'

    # Check that the track has expected artist.
    assert track.artist.full_name == 'AWOL'

    # Check that the track has expected genre(s).
    # This track is expected to have genre 'Hip-Hop' inside its genre list.
    assert 'Hip-Hop' in [genre.name for genre in track.genres]


def test_repository_does_not_retrieve_a_non_existent_track(memory_repo: MemoryRepository):
    track = memory_repo.get_track(10201901)  # Non-existing track id
    assert track is None


def test_repository_can_retrieve_track_count(memory_repo: MemoryRepository):
    number_of_tracks = memory_repo.get_number_of_tracks()

    # Check that the query returned 10 tracks
    assert number_of_tracks == 10


def test_repository_can_retrieve_all_tracks(memory_repo: MemoryRepository):
    # Check that the memory repository has all 10 tracks from test csv
    tracks = memory_repo.get_tracks()
    assert len(tracks) == 10


def test_repository_can_add_a_genre(memory_repo: MemoryRepository):
    genre = Genre(3031, 'New Genre')
    memory_repo.add_genre(genre)

    # Test repo has added a new genre and its number of genre increased from 7 to 8.
    assert len(memory_repo.get_genres()) == 8


def test_repository_can_retrieve_genres(memory_repo: MemoryRepository):
    genres = memory_repo.get_genres()

    # Test there are total 7 unique genres in the test dataset.
    assert len(genres) == 7


def test_repository_can_add_album(memory_repo: MemoryRepository):
    album = Album(15212, 'Justice')
    memory_repo.add_album(album)

    # Test repo has a new album inside
    albums = memory_repo.get_albums()
    assert album in albums


def test_repository_can_retrieve_albums(memory_repo: MemoryRepository):
    albums = memory_repo.get_albums()
    # Test there are total 5 albums inside the test csv file.
    assert len(albums) == 5


def test_repository_can_add_artist(memory_repo: MemoryRepository):
    artist = Artist(923892, 'A new artist')
    memory_repo.add_artist(artist)

    # Test repo has a new artist inside
    assert artist in memory_repo.get_artists()


def test_repository_can_retrieve_artists(memory_repo: MemoryRepository):
    artists = memory_repo.get_artists()

    # Test there are total 5 artits inside the test csv file.
    assert len(artists) == 5


def test_repository_can_add_review(memory_repo: MemoryRepository):
    # Get a sample track
    track_id = 2
    track = memory_repo.get_track(track_id)

    review1 = Review(track, 'My review 1', 5)
    review2 = Review(track, 'My review 2', 1)

    memory_repo.add_review(review1)
    memory_repo.add_review(review2)

    # Retrieve all reviews for this track and test if new reviews exist.
    reviews = memory_repo.get_reviews_for_track(track_id)
    assert review1 in reviews
    assert review2 in reviews

    # Review without track should not be added to repo
    review3 = Review(None, 'My review 3', 2)

    # RepositoryException should be raised if trying to add review without a track
    with pytest.raises(RepositoryException):
        memory_repo.add_review(review3)


def test_repository_can_retrieve_review_for_a_track(memory_repo: MemoryRepository):
    # Get a sample track
    track_id = 2
    track = memory_repo.get_track(track_id)

    # Initially there are no reviews for a track
    assert len(memory_repo.get_reviews_for_track(track_id)) == 0

    review = Review(track, 'My review 1', 5)
    memory_repo.add_review(review)

    # After adding a review, there should be one review for the track
    assert len(memory_repo.get_reviews_for_track(track_id)) == 1


# Test repository search tracks by title
def test_repository_can_search_tracks_by_title(memory_repo: MemoryRepository):
    # Create sample tracks
    track1 = Track(29149, 'New track 1')
    track2 = Track(2914997, 'New track 2')
    track3 = Track(2914998, 'Random track')

    memory_repo.add_track(track1)
    memory_repo.add_track(track2)
    memory_repo.add_track(track3)

    # Search tracks based on artist name - no extra whitespace and case in-sensitive
    searched_tracks = memory_repo.search_tracks_by_title(
        '  new track  ')
    # Based on the search string, track1 and track2 should be searched, but not track3
    assert sorted(searched_tracks) == [track1, track2]


# Test repository search tracks by artist
def test_repository_can_search_tracks_by_artist(memory_repo: MemoryRepository):
    # Create a sample artist for testing purpose
    artist = Artist(2918392, 'New Test Artist')

    # Create sample tests for this artist
    track1 = Track(29149939, 'New track 1')
    track2 = Track(29149940, 'New track 2')
    track3 = Track(29149949, 'Track not by this artist')

    track1.artist = artist
    track2.artist = artist

    memory_repo.add_artist(artist)
    memory_repo.add_track(track1)
    memory_repo.add_track(track2)
    memory_repo.add_track(track3)

    # Search tracks based on artist name - no extra whitespace and case in-sensitive
    searched_tracks = memory_repo.search_tracks_by_artist(
        '  new test artist  ')
    # track1 and track2 should be searched, but not track3
    assert sorted(searched_tracks) == [track1, track2]


# Test repository search tracks by album
def test_repository_can_search_tracks_by_album(memory_repo: MemoryRepository):
    # Create a sample album for testing purpose
    album = Album(2918392, 'New Test Album')

    # Create sample tests for this artist
    track1 = Track(29149939, 'New track 1')
    track2 = Track(29149940, 'New track 2')

    track1.album = album
    track2.album = album

    memory_repo.add_album(album)
    memory_repo.add_track(track1)
    memory_repo.add_track(track2)

    # Search tracks based on album name - no extra whitespace and case-insensitive
    searched_tracks = memory_repo.search_tracks_by_album(' new test album ')
    assert sorted(searched_tracks) == [track1, track2]


# Test repository search tracks by genre name
def test_repository_can_search_tracks_by_genre(memory_repo: MemoryRepository):
    # Create a sample genre for testing purpose
    genre = Genre(2918392, 'New Test Genre')

    # Create sample tests for this artist
    track1 = Track(29149939, 'New track 1')
    track2 = Track(29149940, 'New track 2')

    track1.add_genre(genre)
    track2.add_genre(genre)

    memory_repo.add_genre(genre)
    memory_repo.add_track(track1)
    memory_repo.add_track(track2)

    # Search tracks based on genre name - no extra whitespace and case-insensitive
    searched_tracks = memory_repo.search_tracks_by_genre(' new test genre ')
    assert sorted(searched_tracks) == [track1, track2]
