"""App entry point."""
from music import create_app
from os import environ

app = create_app()

if __name__ == "__main__":
    port = environ.get('PORT')
    print(f"port: {port}")
    app.run(host=f'0.0.0.0:{port}')
    # app.run(host='localhost', port=5000, threaded=False)
