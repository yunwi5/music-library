# Music Library

## Description
This project is a music library application where users can browse various albums and tracks, view the details of albums and tracks, and make reviews.

<br />


## Deployment
### Cloud Platform
<img width="200" height="200" src="https://user-images.githubusercontent.com/86972879/201139651-0ac4b320-3dd6-447b-b8f2-c7c5f5c5350c.png" />

The project has been deployed via <strong>[Railway](https://railway.app/)</strong> that hosts the application on the web.
 
### Deployment URL
[https://music-library.up.railway.app/](https://music-library.up.railway.app/)

<br />

## Installation

Please make sure you have `Python` installed on your machine. This application was developed with Python version 3.10,
but other versions of Python 3 would work as well.

**Installation via requirements.txt**

```shell
# Activate the virtual environment
$ py -3 -m venv venv
$ venv\Scripts\activate
# Install all dependencies in requirements.txt file
$ pip install -r requirements.txt
```

When using PyCharm, set the virtual environment using 'File'->'Settings' and select your project from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add'. Click the 'Existing environment' radio button to select the virtual environment. 

<br />

## Execution

**Running the application**

From the project root directory, and within the activated virtual environment (see *venv\Scripts\activate* above):

````shell
$ flask run
```` 

The flask server will start running on the port [http://127.0.0.1:5000](http://127.0.0.1:5000) by default.

<br />

## Testing

### Unit & e2e testing
After you have configured pytest as the testing tool for PyCharm (File - Settings - Tools - Python Integrated Tools - Testing), you can then run tests from within PyCharm by right clicking the tests folder and selecting "Run pytest in tests".

Alternatively, from a terminal in the root directory of the project, you can also call 'python -m pytest tests' to run all the tests.

````shell
# Runs all tests locatd in /tests directory with pytest
$ python -m pytest tests
```` 

This will run all unit, integration and e2e tests for domain models, memory repository, services and the web app.

### Database Testing
If you want to run the tests for database implementation, you can run the tests from within PyCharm by right clicking the tests folder and selecting "Run pytest in tests_db".

Alternatively, from a terminal in the root directory of the project, you can also call 'python -m pytest tests_db' to run all the tests for the database implementation.

````shell
# Runs all tests locatd in /tests_db directory with pytest
$ python -m pytest tests_db
```` 

This will run all unit and integration tests for ORM, database repository and database populate.

<br />

## Technologies Used

### Programming Language
* Python (3.10)

### Web Framework
* Flask (2.0.3)

### Database
* SQLite3

### Libraries
* flask-wtf (0.15.0)
* python-dotenv (0.19.0)
* better-profanity (0.7.0)
* password-validator (1.0)
* SQLAlchemy (1.4.41)
* pytest

### Web Technologies
* HTML
* CSS

You can view the full list of dependencies in `requirements.txt` file.

<br />

## Features

### Login & Register
<img width="600" height="300" src="https://user-images.githubusercontent.com/86972879/201021556-7d544e5f-d156-494b-b883-8ba0c00db9fc.png" />

Users can login and register to the application, and can logout by clicking the logout button.

### Browsing Tracks
<img width="600" height="300" src="https://user-images.githubusercontent.com/86972879/201022026-5218b48f-a613-4701-aa1b-34e1c86cf58a.png" />

Users can browse the list of tracks with 10 tracks displayed on each page. Users can navigate between pages to browse the tracks they want.

### View Track Detail & Reviews
<img width="490" height="350" src="https://user-images.githubusercontent.com/86972879/201022581-026aa583-6119-4aff-a8bf-fdcd22ecb5f6.png" />

Users can view the details of a track such as genres and duration, and can make reviews. <br />
Only authenticated users can make a review for the track.

### Browsing Albums
<img width="550" height="300" src="https://user-images.githubusercontent.com/86972879/201022756-45244a39-ff23-4d27-8f85-f0254bd991ff.png" />

Users can browse the list of albums with 10 albums displayed on each page. Users can navigate between pages to browse the albums they want.

### View Album Detail
<img width="500" height="360" src="https://user-images.githubusercontent.com/86972879/201022940-378e2ab1-dcb2-4547-a94e-dc8801f8ca9a.png" />

Users can view the details of an album such as album type and release year, and they can view the list of tracks associated with this album.

<br />

## Data sources

The data files are modified excerpts downloaded from:
https://www.loc.gov/item/2018655052  or
https://github.com/mdeff/fma 

We would like to acknowledge the authors of these papers for introducing the Free Music Archive (FMA), an open and easily accessible dataset of music collections: 

Defferrard, M., Benzi, K., Vandergheynst, P., & Bresson, X. (2017). FMA: A Dataset for Music Analysis. In 18th International Society for Music Information Retrieval Conference (ISMIR).

Defferrard, M., Mohanty, S., Carroll, S., & Salathe, M. (2018). Learning to Recognize Musical Genre from Audio. In The 2018 Web Conference Companion. ACM Press.
