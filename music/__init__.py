"""Initialize Flask app."""

from flask import Flask, render_template
from pathlib import Path

import music.adapters.repository as repo
from music.adapters.memory_repository import MemoryRepository, populate


def create_app(test_config=None):
    """Construct the core application."""

    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = Path('music') / 'adapters' / 'data'
    testing = False

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']
        testing = True

    # Create the MemoryRepository implementation for a memory-based repository.
    repo.repo_instance = MemoryRepository()
    # fill the content of the repository from the provided csv files
    populate(data_path, repo.repo_instance, testing)

    # Build the application - these steps require an application context.
    with app.app_context():
        # Register the blueprints to the app instance.
        from .home import home
        app.register_blueprint(home.home_blueprint)

        # Authentication blueprint
        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        # Track blueprint
        from .tracks import tracks
        app.register_blueprint(tracks.tracks_blueprint)

        # Utility blueprint
        from .utilities import utilities
        app.register_blueprint(utilities.utilities_blueprint)

    return app
