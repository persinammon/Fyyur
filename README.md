## Fyyur

Fyyur is a Flask web application project for viewing venues, musicians, and shows by musicians at venues. 

Front-end templating of views and a backend structure were given. 

I did the following:
- Set up a local PostgreSQL database
- Wrote the data models using SQLAlchemy
- Populated the database with mock data
- Implemented backend server logic for CRUD functions on musician, show, and venue data using SQLAlchemy
- Used Flask-Migrate to perform a database migration after updating database table schema
- Set up a factory method for production server Waitress

### Backend Dependencies

 - virtualenv (for local development)
 - SQLAlchemy ORM
 - PostgreSQL
 - Python3
 - Flask 
 - Flask-Migrate 
 - Waitress

### Deployment Setup

Run the following command:

```
waitress-serve --port=8000 --call app:create_app
```

There are separate Dockerfiles for a PostgreSQL database and a Flask web app container,
but there is a persistent error where `psycopg2` cannot connect to the database 
(suspected issue with authorization in Postgres database). I think I'll eventually
move from SQLAlchemy to another ORM (Peewee) to test if that allows for database
access in containers.

### Local Development Setup

1. Create a virtualenv using:

```
python3 -m venv env
```

To activate the virtual environment, use `source env/bin/activate` in Linux or
MacOS and `source env/Scripts/activate` in Windows.

2. Activate virtual environment and install dependencies:

```
pip3 install -r requirements.txt
```

3. Create a `config.py` in root directory with the following contents:

```
import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# LOCAL DATABASE URI
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:{POSTGRES_USER_PASSWORD}@localhost:5432/fyyur'
```

4. Run `createdb fyyur`.

5. Run the development server:

```
export FLASK_APP=app.py
export FLASK_ENV=development # enables debug mode
flask run
```
Replace `export` with `set` in Windows terminal.

6. Verify on the Browser

Navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000) 

7. Use `Ctrl+C` to interrupt running and `deactivate` to exit virtual environment.
