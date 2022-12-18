## Fyyur

Fyyur is a Flask web application project for viewing venues, musicians, and shows by musicians at venues. 

Front-end templating of views and a backend structure were given. 

I did the following:
- Set up a local PostgreSQL database
- Wrote the data models using SQLAlchemy
- Populated the database with mock data
- Implemented backend server logic for CRUD functions on musician, show, and venue data using SQLAlchemy
- Used Flask-Migrate to perform a database migration after updating database table schema

### Backend Dependencies

 - virtualenv
 - SQLAlchemy ORM
 - PostgreSQL
 - Python 3.6 and Flask 
 - Flask-Migrate 

## Local Deployment Setup

1. **Initialize and activate a virtualenv using:**
```
python -m virtualenv env
```

To activate the virtual environment, use `source env/bin/activate` in Linux or
MacOS and `source env/Scripts/activate` in Windows.

2. **Install the dependencies:**
```
pip install -r requirements.txt
```

3. **Run the development server:**

Use `python3` or `python` depending on which points to version 3.6.
```
export FLASK_APP=app.py
export FLASK_ENV=development # enables debug mode
python app.py 
```
Replace `export` with `set` in Windows terminal (Powershell or Command Prompt).

6. **Verify on the Browser**<br>
Navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000) 

