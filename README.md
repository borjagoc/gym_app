# Gym App Project
Udacity Full-Stack Web Developer Nanodegree Program Final Project

## Project Motivation
The Gym App Project models a company that is responsible for organising sessions and connecting teachers, disciplines and gyms. You are an Executive Producer within the company and are creating a system to simplify and streamline your process. 


This project is simply a workspace for practicing and showcasing different set of skills related with web development. These include data modelling, API design, authentication and authorization and cloud deployment.

## Getting Started

The project adheres to the PEP 8 style guide and follows common best practices, including:

* Variable and function names are clear.
* Endpoints are logically named.
* Code is commented appropriately.
* Secrets are stored as environment variables.


### Key Dependencies & Platforms

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

- [Auth0](https://auth0.com/docs/) is the authentication and authorization system we'll use to handle users with different roles with more secure and easy ways

- [PostgreSQL](https://www.postgresql.org/) this project is integrated with a popular relational database PostgreSQL, though other relational databases can be used with a little effort.

- [Heroku](https://www.heroku.com/what) is the cloud platform used for deployment


### Running Locally

#### Installing Dependencies

##### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

##### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

#### Database Setup
With Postgres running, restore a database using the `capstone.psql` file provided. In terminal run:

```bash
createdb capstonedb
psql capstonedb < capstone.psql
```

#### Running Tests
To run the tests, run
```bash
dropdb capstonedb_test
createdb capstonedb_test
psql capstonedb_test < capstone.psql
python3 unit_test.py
```


#### Auth0 Setup

You need to setup an Auth0 account.

Environment variables needed: (setup.sh)

```bash
export DATABASE_URL="postgresql://xxxx@localhost:5432/capstonedb"
export DATABASE_NAME="capstonedb"
export AUTH0_DOMAIN="xxxxxxxxxx.auth0.com"
export AUTH0_API_IDENTIFIER="sweat"
export MANAGERS_TOKEN="xxxx" #See instructions below
export TEACHERS_TOKEN="xxxx" #See instructions below
```


##### Set JWT Tokens in `setup.sh`

Use the following link to create users and sign them in. This way, you can generate 

```
https://dev-9-hxj2sw.us.auth0.com/authorize?audience=sweat&response_type=token&client_id=opwmj0iP4Yk3Hz5PlC1l1Uf0cSBlXnWO&redirect_uri=https://127.0.0.1:8080/callback
```

The below credentials can be used to log in with the different roles:

- Manager

```
    email: borjathemanager@gmail.com
    password: borjathemanager_123
```

- Teacher

```
    email: dantheteacher@gmail.com
    password: dantheteacher_123
```


##### Roles

Create three roles for users under `Users & Roles` section in Auth0

* Gym group manager
	* Add teachers and disciplines
  * Modify teachers
  * Delete teachers and disciplines
* Gym teacher
	* Add sessions
  * Delete sessions


##### Permissions

Following permissions should be created under created API settings.

1. Gym group manager:
  - `add:discipline`
  - `add:teacher`
  - `delete:discipline`
  - `delete:teacher`
  - `patch:teacher`
2. Gym teacher:
  - `add:sessions`
  - `delete:sessions`
  - `patch:sessions`



#### Launching The App

1. Initialize and activate a virtualenv:

   ```bash
   virtualenv --no-site-packages env_capstone
   source env_capstone/bin/activate
   ```

2. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```
3. Configure database path to connect local postgres database in `models.py`

    ```python
    database_path = "postgres://{}/{}".format('localhost:5432', 'capstone')
    ```
**Note:** For default postgres installation, default user name is `postgres` with no password. Thus, no need to speficify them in database path. You can also omit host and post (localhost:5432). But if you need, you can use this template:

```
postgresql://[user[:password]@][netloc][:port][/dbname][?param1=value1&...]
```
For more details [look at the documentation (31.1.1.2. Connection URIs)](https://www.postgresql.org/docs/9.3/libpq-connect.html)

4. Setup the environment variables for Auth0 under `setup.sh` running:
	```bash
	source ./setup.sh 
	```
5.  To run the server locally, execute:

    ```bash
    export FLASK_DEBUG=True
    export FLASK_ENVIRONMENT=debug
    python3 app.py
    ```

    Optionally, you can use `run.sh` script.


## API Documentation

### Models
There are four models:
* Discipline
	* name
* Teacher
	* name
	* discipline_id
	* instagram_account
* Gym
  * name
  * city
  * website
* Session
  * name
  * gym_id
  * teacher_id
  * discipline_id
  * start_time
  * length_in_minutes


### Error Handling

Errors are returned as JSON objects in the following format:
```json
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Resource Not Found
- 422: Not Processable 
- 500: Internal Server Error


### Endpoints

- GET '/api/'
- GET '/api/teachers'
- POST '/api/teachers'
- DELETE '/api/teachers/{teacher_id}'
- PATCH '/api/teachers/{teacher_id}'
- GET '/api/disciplines'
- POST '/api/disciplines'
- GET '/api/sessions'
- POST '/api/sessions'


#### GET '/api/'

- This is the home page where you will receive the following welcome message:

    ```
    !!!!! Welcome to the best Gym app in the world.

    ```

#### GET '/api/teachers'
- Fetches a dictionary of teachers in which the keys are the fields and the value is the corresponding string of the field
- Request Arguments: None
- Returns: Returns a list of teacher objects and a success value.

* **Example Response:**
    ```json
    {
        "success": true,
        "teachers": [
            {
                "discipline_id": 1,
                "id": 1,
                "instagram_account": "@JuanA",
                "name": "Juan Amor"
            },
            {
                "discipline_id": 1,
                "id": 2,
                "instagram_account": "@DanK",
                "name": "Dan K"
            }
        ]
    }
    ```

#### POST '/api/teachers'
- Creates a new teacher in the database
- Request Arguments: name, discipline_id and instagram_account
- Returns: Returns a success value and a list of teacher objects.  

    ```
    curl --location --request POST 'http://127.0.0.1:5000/teachers' \
    --header 'Authorization: Bearer {JWT TOKEN}' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "name": "Dan K",
        "discipline_id": 1,
        "instagram_account": "@DanK"
    }'
    ```

* **Example Response:**
    ```json
    {
        "success": true,
        "teachers": [
            {
                "discipline_id": 1,
                "id": 1,
                "instagram_account": "@JuanA",
                "name": "Juan Amor"
            },
            {
                "discipline_id": 1,
                "id": 2,
                "instagram_account": "@DanK",
                "name": "Dan K"
            }
        ]
    }
    ```

#### DELETE '/api/teachers/{teacher_id}'
- Deletes the teacher of the given ID if it exists.
- Request Arguments: None
- Returns: Returns the list of teachers after deletion.

    ```
    curl --location --request DELETE 'http://127.0.0.1:5000/teachers/2' \
    --header 'Authorization: Bearer {JWT TOKEN}'
    ```

    ```json
    {
        "success": true,
        "teachers": [
            {
                "discipline_id": 1,
                "id": 1,
                "instagram_account": "@JuanA",
                "name": "Juan Amor"
            }
        ]
    }
    ```

#### PATCH '/api/teachers/{teacher_id}'
- Modifies the teacher of the given ID if it exists.
- Request Arguments: name, discipline_id or instagram_account
- Returns: Returns the list of teachers after patching.

    ```
    curl --location --request PATCH 'http://127.0.0.1:5000/teachers/1' \
    --header 'Authorization: Bearer {JWT TOKEN}'\
    --header 'Content-Type: application/json' \
    --data-raw '{
        "name": "Lucy L",
        "discipline_id": 1,
        "instagram_account": "@LucyL"
    }'
    ```

    ```json
    {
        "success": true,
        "teachers": [
            {
                "discipline_id": 1,
                "id": 1,
                "instagram_account": "@LucyL",
                "name": "Lucy L"
            }
        ]
    }
    ```

#### GET '/api/disciplines'
- Fetches a dictionary of disciplines in which the keys are the fields and the value is the corresponding string of the field
- Request Arguments: None
- Returns: Returns a list of disciplines objects and a success value.

    ```json
    {
        "disciplines": [
            {
                "id": 1,
                "name": "Calisthenics"
            },
            {
                "id": 2,
                "name": "Yoga"
            }
        ],
        "success": true
    }
    ```

#### POST '/api/disciplines'
- Creates a new discipline in the database
- Request Arguments: name
- Returns: Returns a success value and a list of discipline objects.  

    ```
    curl --location --request POST 'http://127.0.0.1:5000/disciplines' \
    --header 'Authorization: Bearer {JWT TOKEN}' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "name": "Boxing"
    }'
    ```

    ```json
    {
        "disciplines": [
            {
                "id": 1,
                "name": "Calisthenics"
            },
            {
                "id": 2,
                "name": "Yoga"
            },
            {
                "id": 3,
                "name": "Boxing"
            }
        ],
        "success": true
    }
    ```

#### GET '/api/sessions'
- Fetches a dictionary of sessions in which the keys are the fields and the value is the corresponding string of the field
- Request Arguments: None
- Returns: Returns a list of disciplines objects and a success value.

    ```json
    {
        "sessions": [
            {
            "discipline_id": 2, 
            "gym_id": 1, 
            "id": 1, 
            "length_in_minutes": 90, 
            "name": "Yoga with Francesco on Wed", 
            "start_time": "Wed, 01 Jun 2022 06:30:00 GMT", 
            "teacher_id": 2
            }
        ], 
        "success": true
    }
    ```

#### POST '/api/sessions'
- Creates a new session in the database
- Request Arguments: name, discipline_id, gym_id, teacher_id, length_in_minutes, start_time
- Returns: Returns a success value and a list of session objects.  

    ```
    curl --location --request POST 'http://127.0.0.1:5000/sessions' \
    --header 'Authorization: Bearer {JWT TOKEN}' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "name": "Calisthenics with Dan on Monday", 
        "discipline_id": 1, 
        "gym_id": 1, 
        "length_in_minutes": 60, 
        "start_time": "Mon, 20 Jun 2022 17:20:00 GMT", 
        "teacher_id": 1
    }'
    ```

    ```json
    {
        "sessions": [
            {
            "discipline_id": 2, 
            "gym_id": 1, 
            "id": 1, 
            "length_in_minutes": 90, 
            "name": "Yoga with Francesco on Wed", 
            "start_time": "Wed, 01 Jun 2022 06:30:00 GMT", 
            "teacher_id": 2
            }, 
            {
            "discipline_id": 1, 
            "gym_id": 1, 
            "id": 2, 
            "length_in_minutes": 60, 
            "name": "Calisthenics with Dan on Monday", 
            "start_time": "Mon, 20 Jun 2022 17:20:00 GMT", 
            "teacher_id": 1
            }
        ], 
        "success": true
    }
    ```