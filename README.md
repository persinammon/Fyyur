Fyyur
-----

## Introduction

Fyyur is a web application project for viewing venues, musicians, and shows by musicians at venues. 
Front-end templating of views and a backend structure were given. I set up a local Postgres database, 
wrote the data models, and implemented backend server logic to CRUD musician, show, and venue data 
from the database. I also performed a database migration after updating model columns.

## Tech Stack (Dependencies)

### 1. Backend Dependencies
The tech stack includes the following:
 * **virtualenv** as a tool to create isolated Python environments
 * **SQLAlchemy ORM** to be our ORM library of choice
 * **PostgreSQL** as our database of choice
 * **Python3** and **Flask** as our server language and server framework
 * **Flask-Migrate** for creating and running schema migrations

### 2. Frontend Dependencies
There must be **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for the website's frontend. 

## Development Setup

1. **Fork or clone Git repo for local running**

3. **Initialize and activate a virtualenv using:**
```
python -m virtualenv env
source env/bin/activate
```
>**Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:
```
source env/Scripts/activate
```

4. **Install the dependencies:**
```
pip install -r requirements.txt
```

5. **Run the development server:**
```
export FLASK_APP=myapp
export FLASK_ENV=development # enables debug mode
python3 app.py
```

6. **Verify on the Browser**<br>
Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000) 

