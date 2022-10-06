import pytest

from flask import session

# Helper function to register and login the sample user (NOT an actual testing function)


def perform_login(client, auth):
    # First register a sample user.
    client.post(
        '/authentication/register',
        data={'user_name': 'denis', 'password': 'D30sadq9a'}
    )
    # Login a user.
    auth.login(user_name='denis', password='D30sadq9a')


def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid user name and password.
    response = client.post(
        '/authentication/register',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )

    # Test that the location of the headers is pointing to the login page after registration
    assert response.headers['Location'] == '/authentication/login'


@pytest.mark.parametrize(('user_name', 'password', 'message'), (
    ('', '', b'Your user name is required'),
    ('cj', '', b'Your user name is too short'),
    ('test', '', b'Your password is required'),
    ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'),
))
def test_register_with_invalid_input(client, user_name, password, message):
    # Check that attempting to register with invalid combinations of user name and password
    # generate appropriate error messages.
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    # First register a sample user.
    client.post(
        '/authentication/register',
        data={'user_name': 'denis', 'password': 'D30sadq9a'}
    )

    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login(user_name='denis', password='D30sadq9a')
    assert response.headers['Location'] == '/'

    # # Check that a session has been created for the logged-in user.
    with client:
        response = client.get('/')
        # Test user_name is in the session
        assert session['user_name'] == 'denis'

        # Test user_name appears on the web page header to indicate login status
        assert b'denis' in response.data


def test_logout(client, auth):
    # First register and login a sample user.
    perform_login(client, auth)

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session


def test_home(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    # Test home page heading is in the response data
    assert b'Feel the extreme joy of music with CS235 Music Library' in response.data


def test_browse_tracks(client):
    # Test /browse_tracks route

    # Check that we can retrieve the browsing page.
    response = client.get('/browse_tracks')
    assert response.status_code == 200

    # Check the browsing page heading is in the response data
    assert b'Browse Tracks' in response.data


def test_track_detail(client):
    # Test /track_detail route

    track_id = 2  # Track id for track 'Food'
    response = client.get(f'/track_detail?track_id={track_id}')

    # Test that we can retrieve the track detail page
    assert response.status_code == 200

    # Test the title of the track is displayed on the page
    assert b'Food' in response.data

    # Test the artist is displayed on the page
    assert b'AWOL' in response.data

    # Test the artist is displayed on the page
    assert b'AWOL - A Way Of Life' in response.data

    # Test the genre of the track is displayed on the page
    assert b'Hip-Hop' in response.data


def test_login_required_to_review(client):
    response = client.post('/track_review')
    assert response.headers['Location'] == '/authentication/login'


def test_review(client, auth):
    # First register and Login a sample user.
    perform_login(client, auth)

    # Check that we can retrieve the review page for track_id=2 (track 'Food').
    response = client.get('/track_review?track_id=2')

    response = client.post(
        '/track_review',
        data={'rating': 5, 'review_text': 'Pretty nice track!', 'track_id': 2}
    )

    # After posting the comment, redirect to the track_detail page.
    assert response.headers['Location'] == '/track_detail?track_id=2'


@pytest.mark.parametrize(('review_text', 'messages'), (
    ('Who thinks this shitty track is a f***wit?',
     (b'Your review must not contain profanity')),
    ('Hey', (b'Your review should be at least 5 characters')),
    ('Ass', (b'Your review should be at least 5 characters',
             b'Your review must not contain profanity')),
))
def test_review_with_invalid_text(client, auth, review_text, messages):
    # This function will only test reviews with invalid review_text
    # Login a user.
    perform_login(client, auth)

    # Attempt to review_text on an article.
    response = client.post(
        '/track_review',
        data={'rating': 5, 'review_text': review_text, 'track_id': 2}
    )
    # Check that supplying invalid review text generates appropriate error messages.
    for message in messages:
        assert message in response.data


@pytest.mark.parametrize(('rating', 'messages'), (
    (-1,
     (b'Your rating should be between 1 and 5')),
    (30, (b'Your rating should be between 1 and 5')),
    (1000, (b'Your rating should be between 1 and 5')),
))
def test_review_with_invalid_rating(client, auth, rating, messages):
    # This function will only test reviews with invalid rating range outside 1-5
    # Login a user.
    perform_login(client, auth)

    # Attempt to review_text on an article.
    response = client.post(
        '/track_review',
        data={'rating': rating, 'review_text': 'Sample review text', 'track_id': 2}
    )
    # Check that supplying invalid review rating generates appropriate error messages.
    for message in messages:
        assert message in response.data


# Test searching
def test_search_tracks_by_title(client):
    title = 'food'
    response = client.get(
        f'/search_tracks?page=0&search_key=title&text={title}')

    assert response.status_code == 200

    # Test the appropirate heading is displayed on the page
    assert b'Titles based on' in response.data

    # Test tracks of the searhed title is displayed on the page
    assert b'Food' in response.data

    # Test the artist is displayed on the page
    assert b'AWOL' in response.data
    # Test the album is displayed on the page
    assert b'AWOL - A Way Of Life' in response.data
    # Test the genre is displayed on the page
    assert b'Hip-Hop' in response.data


def test_search_tracks_by_artist(client):
    artist_name = 'AWOL'
    response = client.get(
        f'/search_tracks?page=0&search_key=artist&text={artist_name}')

    assert response.status_code == 200

    # Test the appropirate heading is displayed on the page
    assert b'Artists based on' in response.data

    # Test tracks of the artist is displayed on the page
    assert b'Food' in response.data

    # Test albums of the artist is displayed on the page
    assert b'AWOL - A Way Of Life' in response.data


def test_search_tracks_by_album(client):
    album_name = 'AWOL - A Way Of Life'
    response = client.get(
        f'/search_tracks?page=0&search_key=album&text={album_name}')

    assert response.status_code == 200

    # Test the appropirate heading is displayed on the page
    assert b'Albums based on' in response.data

    # Test tracks of the album is displayed on the page
    assert b'Food' in response.data
    assert b'Electric Ave' in response.data


def test_search_tracks_by_genre(client):
    genre_name = 'Hip-Hop'
    response = client.get(
        f'/search_tracks?page=0&search_key=genre&text={genre_name}')

    assert response.status_code == 200

    # Test the appropirate heading is displayed on the page
    assert b'Genres based on' in response.data

    # Test tracks of the album is displayed on the page
    assert b'Electric Ave' in response.data
