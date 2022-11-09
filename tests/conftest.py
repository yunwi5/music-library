import pytest

from music import create_app
from music.adapters import repository_populate
from music.adapters.memory_repository import MemoryRepository

from utils import get_project_root

# the csv files in the test folder are different from the csv files in the covid/adapters/data folder!
# tests are written against the csv files in tests, this data path is used to override default path for testing
TEST_DATA_PATH = get_project_root() / "tests" / "data"


@pytest.fixture
def memory_repo():
    repo = MemoryRepository()
    repository_populate.populate(TEST_DATA_PATH, repo, testing=True, database_mode=False)
    return repo


@pytest.fixture
def client():
    my_app = create_app({
        # Set to True during testing.
        'TESTING': True,
        # Set REPOSITORY mode to 'memory' always. Otherwise, it results in errors in e2e testing.
        'REPOSITORY': 'memory',
        # Path for loading test data into the repository.
        'TEST_DATA_PATH': TEST_DATA_PATH,
        # test_client will not send a CSRF token, so disable validation.
        'WTF_CSRF_ENABLED': False
    })

    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def login(self, user_name='denis', password='cdanieloFXloS'):
        return self.__client.post(
            'authentication/login',
            data={'user_name': user_name, 'password': password}
        )

    def logout(self):
        return self.__client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
