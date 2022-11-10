# COMPSCI 235 Model Answer for Assignment 2
This is a model answer repository for the assignment 2 of CompSci 235 in Semester 2, 2022.


## Description

### Content from Assignment 1
This repository contains an implementation of the domain model from Assignment 1. It contains unit tests on domain models which can be run through pytest.

### Content from Assignment 2
This branch contains MVP features for a music library application such as browsing tracks with pagination, 
searching tracks based on artists, albums and genres, authentication (login & register), and reviews on tracks.

It contains unit tests, integration tests and e2e tests that will test domain models, memory repository methods,
 services, and a web app as a whole through pytest. The tests are located in `/tests` directory.

 <br />

## Installation

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

After you have configured pytest as the testing tool for PyCharm (File - Settings - Tools - Python Integrated Tools - Testing), you can then run tests from within PyCharm by right clicking the tests folder and selecting "Run pytest in tests".

Alternatively, from a terminal in the root directory of the project, you can also call 'python -m pytest tests' to run all the tests.

````shell
# Runs all tests locatd in /tests directory with pytest
$ python -m pytest tests
```` 

This will run all unit, integration and e2e tests for domain models, memory repository, services and the web app.

<br />

## Technologies Used

### Programming Language
* Python (3.10)

### Framework
* Flask (2.0.3) - Web framework

### Libraries
* flask-wtf (0.15.0)
* python-dotenv (0.19.0)
* better-profanity (0.7.0)
* password-validator (1.0)

### Web Technologies
* HTML
* CSS

You can view the full list of dependencies in `requirements.txt` file.

<br />

## Data sources

The data files are modified excerpts downloaded from:
https://www.loc.gov/item/2018655052  or
https://github.com/mdeff/fma 

We would like to acknowledge the authors of these papers for introducing the Free Music Archive (FMA), an open and easily accessible dataset of music collections: 

Defferrard, M., Benzi, K., Vandergheynst, P., & Bresson, X. (2017). FMA: A Dataset for Music Analysis. In 18th International Society for Music Information Retrieval Conference (ISMIR).

Defferrard, M., Mohanty, S., Carroll, S., & Salathe, M. (2018). Learning to Recognize Musical Genre from Audio. In The 2018 Web Conference Companion. ACM Press.
