#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json, datetime
from collections import defaultdict
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
context = app.app_context()

# COMPLETED: Add local database URI to config file


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # newly implemented fields, including child relationship to Show
    website_link = db.Column(db.String(120))
    genres = db.Column(db.PickleType)
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref="venue", lazy=True)

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.PickleType)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # newly implemented fields, including child relationship to Show
    # database best practice suggests using bit instead of Bool, but chose Bool
    # because it's in SQLAlchemy docs
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref="artist", lazy=True)

class Show(db.Model):
    __tablename__ = 'Show'

    #may need to make id into tuple (artist_id, venue_id, start_time)
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)


#instantiate all models in local database
with context:
  db.drop_all() #when testing use this
  db.create_all()
  #instantiate mock data through models
  #use mock data to test before database migration
  venue1 = Venue(name="The Musical Hop", genres= ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  address="1015 Folsom Street", city="San Francisco", state="CA", phone="123-123-1234",
  website_link="https://www.themusicalhop.com", facebook_link="https://www.facebook.com/TheMusicalHop", seeking_talent=True,
  seeking_description="We are on the lookout for a local artist to play every two weeks. Please call us.", image_link="https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60")
  venue2 = Venue(name="The Dueling Pianos Bar", genres= ["Classical", "R&B", "Hip-Hop"],
  address="335 Delancey Street", city="New York", state="NY", phone="914-003-1132",
  website_link="https://www.theduelingpianos.com", facebook_link="https://www.facebook.com/theduelingpianos", seeking_talent=False,
  image_link="https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80")
  venue3 = Venue(name="Park Square Live Music & Coffee", genres=["Rock n Roll", "Jazz", "Classical", "Folk"],
  address="34 Whiskey Moore Ave", city="San Francisco", state="CA", phone="415-000-1234",
  website_link="https://www.parksquarelivemusicandcoffee.com", facebook_link="https://www.facebook.com/ParkSquareLiveMusicAndCoffee", seeking_talent=False,
  image_link="https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80")
  artist1 = Artist(name="Guns N Petals", genres=["Rock n Roll"], city="San Francisco", state="CA", phone="326-123-5000", website_link="https://www.gunsnpetalsband.com",
  facebook_link="https://www.facebook.com/GunsNPetals", seeking_venue=True, seeking_description="Looking for shows to perform at in the San Francisco Bay Area!",
  image_link="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80")
  artist2 = Artist(name="Matt Quevedo", genres=["Jazz"], city="New York", state="NY", phone="300-400-5000",
  facebook_link="https://www.facebook.com/mattquevedo923251523", seeking_venue=False, image_link="https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80")
  artist3 = Artist(name="The Wild Sax Band", genres=["Jazz", "Classical"], city="San Francisco", state="CA", phone="432-325-5432",
  seeking_venue=False, image_link="https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80")
  show1 = Show(venue_id = 1, artist_id = 1, start_time = "2019-05-21T21:30:00.000Z")
  show2 = Show(venue_id = 3, artist_id = 2, start_time = "2019-06-15T23:00:00.000Z")
  show3 = Show(venue_id = 3, artist_id = 3, start_time = "2035-04-01T20:00:00.000Z")
  show4 = Show(venue_id = 3, artist_id = 3, start_time = "2035-04-08T20:00:00.000Z")
  show5 = Show(venue_id = 3, artist_id = 3, start_time = "2035-04-15T20:00:00.000Z")
  db.session.add_all([venue1, venue2, venue3, artist1, artist2, artist3, show1, show2, show3, show4, show5])
  db.session.commit()


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

# NOTE: debug print queries is best with print(val, flush=True)

@app.route('/venues')
def venues():
  # DONE: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  #       later: see if can aggregate num of upcoming shows using .count() instead of iteration
  cities = set([(v.city, v.state) for v in Venue.query.all()])
  time = datetime.utcnow()
  #create dict of venue to num upcoming shows
  num_upcoming_shows = defaultdict(lambda: 0)
  for v in Venue.query.join(Show).filter(Show.start_time > time):
    num_upcoming_shows[v.id] += 1

  data = [{"city": c[0], "state": c[1], "venues": [{"id": v.id, "name": v.name, "num_upcoming_shows": num_upcoming_shows[v.id]}
    for v in Venue.query.filter_by(city= c[0], state = c[1])
    ]} for c in cities]

  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # DONE: replace with real venue data from the venues table, using venue_id
  # check if for joins what type of join
  # later, see if can do it without list comprehension using group_by etc and avoid two Artist.query.gets
  v = Venue.query.get(venue_id)
  time = datetime.utcnow()
  shows = Show.query.join(Venue).filter(Venue.id == venue_id).all()
  upcoming_shows = [{"artist_id": s.artist_id, "artist_name": Artist.query.get(s.artist_id).name, "artist_image_link":
  Artist.query.get(s.artist_id).image_link, "start_time": str(s.start_time)} for s in shows if s.start_time > time]
  past_shows = [{"artist_id": s.artist_id, "artist_name": Artist.query.get(s.artist_id).name, "artist_image_link":
    Artist.query.get(s.artist_id).image_link, "start_time": str(s.start_time)} for s in shows if s.start_time <= time]
  data = {
    "id": v.id,
    "name": v.name,
    "genres": v.genres,
    "address": v.address,
    "city": v.city,
    "state": v.state,
    "phone": v.phone,
    "website": v.website_link,
    "facebook_link": v.facebook_link,
    "seeking_talent": v.seeking_talent,
    "seeking_description": v.seeking_description,
    "image_link": v.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # DONE: insert form data as a new Venue record in the db, instead
  # NEED FURTHER CLARIFICATION ON THIS: modify data to be the data object returned from db insertion
  seeking_talent = False if "seeking_talent" not in request.form.keys() else False
  v = Venue(name=request.form['name'],
   city=request.form['city'],
   state=request.form['state'],
   address=request.form['address'],
   phone=request.form['phone'],
   facebook_link=request.form['facebook_link'],
   image_link=request.form['image_link'],
   website_link=request.form['website_link'],
   seeking_talent=seeking_talent,
   seeking_description=request.form['seeking_description'])
  try:
    db.session.add(v)
    db.session.commit()
  except:
    flash('An error occurred. Venue ' + v.name + ' could not be listed.')
  else:
    flash('Venue ' + v.name + ' was successfully listed!')
  # on successful db insert, flash success
  # DONE: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # DONE: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    v = Venue.query.get(venue_id)
    if v:
        db.session.delete(v)
        db.session.commit()
  except:
    flash("Unable to delete venue.")
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return render_template('/pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # DONE: replace with real data returned from querying the database
  data = [{"id": a.id, "name": a.name} for a in Artist.query.all()]
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # DONE: replace with real artist data from the artist table, using artist_id - note if can optimize
  # similarly to /venues/<int:venue_id>
  a = Artist.query.get(artist_id)
  time = datetime.utcnow()
  shows = Show.query.join(Artist).filter(Artist.id == artist_id).all()
  upcoming_shows = [{"venue_id": s.venue_id, "venue_name": Venue.query.get(s.venue_id).name, "venue_image_link":
  Venue.query.get(s.venue_id).image_link, "start_time": str(s.start_time)} for s in shows if s.start_time > time]
  past_shows = [{"venue_id": s.venue_id, "venue_name": Venue.query.get(s.venue_id).name, "venue_image_link":
  Venue.query.get(s.venue_id).image_link, "start_time": str(s.start_time)} for s in shows if s.start_time <= time]
  data = {
    "id": a.id,
    "name": a.name,
    "genres": a.genres,
    "city": a.city,
    "state": a.state,
    "phone": a.phone,
    "website": a.website_link,
    "facebook_link": a.facebook_link,
    "seeking_venue": a.seeking_venue,
    "seeking_description": a.seeking_description,
    "image_link": a.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }
  return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  a = Artist.query.get(artist_id)
  if not a:
    flash("Artist ID invalid.")
    return render_template('pages/artists')
  artist={
    "id": artist_id,
    "name": a.name,
    "genres": a.genres,
    "city": a.city,
    "state": a.state,
    "phone": a.phone,
    "website": a.website_link,
    "facebook_link": a.facebook_link,
    "seeking_venue": a.seeking_venue,
    "seeking_description": a.seeking_description,
    "image_link": a.image_link
  }
  # DONE: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # DONE: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  data = {}
  for key, value in request.form.items():
    if value:
        data[key] = value
  db.session.query(Artist).filter(Artist.id==artist_id).update(data)
  db.session.commit()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  v = Venue.query.get(venue_id)
  if not v:
    flash("Venue ID invalid.")
    return render_template('pages/venues')
  venue={
    "id": venue_id,
    "name": v.name,
    "genres": v.genres,
    "address": v.address,
    "city": v.city,
    "state": v.state,
    "phone": v.phone,
    "website": v.website_link,
    "facebook_link": v.facebook_link,
    "seeking_talent": v.seeking_talent,
    "seeking_description": v.seeking_description,
    "image_link": v.image_link
  }
  # DONE: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # DONE: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  data = {}
  for key, value in request.form.items():
    if value:
        data[key] = value
  db.session.query(Venue).filter(Venue.id==venue_id).update(data)
  db.session.commit()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # DONE: insert form data as a new Artist record in the db, instead
  # outdated?: modify data to be the data object returned from db insertion
  seeking_venue = False if 'seeking_venue' not in request.form.keys() else request.form['seeking_venue']
  a = Artist(
    name=request.form['name'],
    city=request.form['city'],
    state=request.form['state'],
    phone=request.form['phone'],
    genres=request.form['genres'],
    image_link=request.form['image_link'],
    facebook_link=request.form['facebook_link'],
    website_link=request.form['website_link'],
    seeking_venue=seeking_venue,
    seeking_description=request.form['seeking_description']
  )
  try:
    if not a.name:
        raise ValueError("Artist name cannot be None")
    db.session.add(a)
    db.session.commit()
  except:
    flash('An error occurred. Artist ' + a.name + ' could not be listed.')
  else:
    flash('Artist ' + a.name + ' was successfully listed!')

  # on successful db insert, flash success
  # DONE: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # DONE: replace with real venues data.
  shows = Show.query.all()
  data = [{"venue_id": s.venue_id,
  "venue_name": Venue.query.get(s.venue_id).name,
  "artist_id": s.artist_id,
  "artist_name": Artist.query.get(s.artist_id).name,
  "artist_image_link": Artist.query.get(s.artist_id).image_link,
   "start_time": str(s.start_time)} for s in shows]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # DONE: insert form data as a new Show record in the db, instead
  artist_id, venue_id = int(request.form['artist_id']), int(request.form['venue_id'])
  s = Show(artist_id=artist_id, venue_id=venue_id,start_time=request.form['start_time'])
  try:
    if not artist_id or not Artist.query.get(artist_id):
        raise ValueError("Artist ID invalid.")
    if not venue_id or not Venue.query.get(venue_id):
        raise ValueError("Venue ID invalid.")
    db.session.add(s)
    db.session.commit()
  except:
    flash('An error occurred. Show could not be listed.')
  else:
      # on successful db insert, flash success
      flash('Show was successfully listed!')
  # DONE: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
