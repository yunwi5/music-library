# Implement testing on the service layer
import pytest


from music.authentication.services import AuthenticationException

from music.tracks import services as tracks_services
from music.authentication import services as auth_services
from music.tracks.services import NonExistentTrackException, InvalidSearchKeyException, InvalidPageException, UnknownUserException


def test_can_add_user(memory_repo):
    new_user_name = 'denis'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, memory_repo)

    user_as_dict = auth_services.get_user(new_user_name, memory_repo)
    assert user_as_dict['user_name'] == new_user_name

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')

    # Adding the user with existing name throws NameNotUniqueException
    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(new_user_name, new_password, memory_repo)


def test_can_get_user(memory_repo):
    new_user_name = 'denis2'
    new_password = 'abcd1A23'
    auth_services.add_user(new_user_name, new_password, memory_repo)

    # Test the service layer correctly retrieves the user that was added previosly
    user_as_dict = auth_services.get_user('denis2', memory_repo)
    assert user_as_dict['user_name'] == 'denis2'


def test_authentication_with_valid_credentials(memory_repo):
    new_user_name = 'denis2'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, memory_repo)

    try:
        auth_services.authenticate_user(
            new_user_name, new_password, memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(memory_repo):
    new_user_name = 'denis2'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(
            new_user_name, 'invalid password', memory_repo)


def test_get_track(memory_repo):
    track_id = 2

    # Test service layer returns an existing track
    track = tracks_services.get_track(track_id, memory_repo)
    assert track['title'] == 'Food'
    assert track['album'] == 'AWOL - A Way Of Life'
    assert track['artist'] == 'AWOL'

    # Test non-existing track id returns None
    track = tracks_services.get_track(10291092, memory_repo)
    assert track == None


def test_get_number_of_tracks(memory_repo):
    num_tracks = tracks_services.get_number_of_tracks(memory_repo)

    # Test service layer retrieves correct number of tracks (total 10 in testing mode)
    assert num_tracks == 10


def test_get_tracks_for_page(memory_repo):
    page_tracks = tracks_services.get_tracks_for_page(0, 10, memory_repo)
    # Test only 10 tracks are retrieved from the service layer
    assert len(page_tracks) == 10

    page_tracks = tracks_services.get_tracks_for_page(0, 5, memory_repo)
    # Test only 5 tracks are retrieved from the service layer
    assert len(page_tracks) == 5


def test_cannot_get_tracks_for_invalid_page(memory_repo):
    # Test inserting page of invalid type throws exception
    with pytest.raises(InvalidPageException):
        tracks_services.get_tracks_for_page('Invalid page', 10, memory_repo)

    # Test inserting negative page throws exception
    with pytest.raises(InvalidPageException):
        tracks_services.get_tracks_for_page(-1, 10, memory_repo)

    # Test inserting non-existing page throws exception
    with pytest.raises(InvalidPageException):
        tracks_services.get_tracks_for_page(float('inf'), 10, memory_repo)


def test_can_get_tracks_for_search(memory_repo):
    # Test getting tracks for a search_key 'album'
    searched_tracks = tracks_services.get_tracks_for_search(
        'album', 'awol', memory_repo)
    assert type(searched_tracks) is list
    assert len(searched_tracks) > 0

    # Test getting tracks for a search_key 'artist'
    searched_tracks = tracks_services.get_tracks_for_search(
        'artist', 'awol', memory_repo)
    assert type(searched_tracks) is list
    assert len(searched_tracks) > 0

    # Test getting tracks for a search_key 'genre'
    searched_tracks = tracks_services.get_tracks_for_search(
        'genre', 'hip-hop', memory_repo)
    assert type(searched_tracks) is list
    assert len(searched_tracks) > 0


def test_cannot_get_tracks_for_invalid_search_key(memory_repo):
    search_key = 'Invalid search key'
    # Test inserting non-existing search key throws exception
    with pytest.raises(InvalidSearchKeyException):
        tracks_services.get_tracks_for_search(search_key, 'text', memory_repo)


def test_add_and_get_reviews_for_track(memory_repo):
    track_id = 2

    # Add the user who will write the review
    user_name = 'denis'
    auth_services.add_user(user_name, 'De39sjl3dj', memory_repo)

    tracks_services.add_review(
        track_id, user_name, 'My new review', 5, memory_repo)

    # Check the review was added correctly.
    review_dicts = tracks_services.get_reviews_for_track(track_id, memory_repo)

    # One of the reviews contains the review text we inserted above
    assert 'My new review' in [review['review_text']
                               for review in review_dicts]
    # One of the reviews contains the rating we inserted above
    assert 5 in [review['rating'] for review in review_dicts]


def test_cannot_add_review_for_non_existing_track(memory_repo):
    # Add the user who will write the review
    user_name = 'denis'
    auth_services.add_user(user_name, 'De39sjl3dj', memory_repo)

    track_id = 132401.23  # Non existing track id

    # Inserting a review of non-existing track throws NonExistentTrackException
    with pytest.raises(NonExistentTrackException):
        tracks_services.add_review(
            track_id, user_name, 'My new review', 3, memory_repo)


def test_cannot_add_review_for_non_existing_user(memory_repo):
    track_id = 2  # existing track id

    # Inserting a review of non-existing user throws UnknownUserException
    with pytest.raises(UnknownUserException):
        tracks_services.add_review(
            track_id, 'Unkown user', 'My new review', 3, memory_repo)
