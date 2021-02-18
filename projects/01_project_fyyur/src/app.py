#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
from types import TracebackType
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate, current
import logging
from logging import Formatter, FileHandler
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app,db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Shows(db.Model):
    __tablename__ = 'Shows'
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
    artist_id  = db.Column(db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
    start_time = db.Column(db.DateTime,nullable=False, primary_key=True)


class Venue(db.Model):
    __tablename__ = 'Venue'
    __table_args__ = (db.UniqueConstraint('name'),)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    city = db.Column(db.String(120)) 
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(240))
    artists = db.relationship('Artist', secondary = 'Shows') # can use back ref = venues

class Artist(db.Model):
    __tablename__ = 'Artist'
    __table_args__ = (db.UniqueConstraint('name'),)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(240))
    venues = db.relationship('Venue', secondary = 'Shows')  # can use back ref = artists


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  res_grpby= (db.session.query(Venue.city,Venue.state).group_by(Venue.city,Venue.state)).all()  #group by city,state
  data = [dict(zip(row.keys(), row)) for row in res_grpby]  #convert tuple result to dic 
  
  for area in data : # build venue data list 
    venues = Venue.query.filter(Venue.city == area['city']).all() # filter all venues for this city
    area['venues'] = [ row.__dict__ for row in venues] #best way to convert row model obj into dic
    for venue in area['venues'] : # add num_upcoming_shows data
       venue['num_upcoming_shows'] = 0 #TODO query shows table # add html placeholder.
       venue['num_past_shows'] = 0

  return render_template('pages/venues.html', areas=data) 

@app.route('/venues/search', methods=['POST'])
def search_venues():
  res = db.session.query(Venue).filter(Venue.name.contains(request.form['search_term'])).all()
  response = { "count" : len(res),"data"  : res}
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue=Venue.query.get(venue_id)
  
  venue.past_shows = [] # TOD0
  venue.past_shows_count =  0 # TOD0
  venue.upcoming_shows = [] # TOD0
  venue.upcoming_shows_count = 0 # TOD0

  return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form(): # this is get called when new venue create url requested(empty form) 
  form = VenueForm() 
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(request.form) # populate local form object with form field values
  if form.validate():
     try :
       venue = Venue()
       form.populate_obj(venue) # populate values of form fields into model object
       db.session.add(venue)
       db.session.commit()
       flash('Venue ' + venue.name + ' was successfully listed!') # on successful db insert, flash success
     except IntegrityError: # handle unique constraint by c
       db.session.rollback()
       flash(request.form['name'] + ' already listed.')
       return redirect(url_for('create_venue_submission')) # how to retain form data ??
     except ():   
       db.session.rollback() 
       #flash(TracebackType.print_exc())
       flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
     finally :
       db.session.close() 
  else :
      flash(form.errors) # validation errror
  #return render_template('pages/home.html')
  return redirect(url_for('venues')) # redirect to venus list page

@app.route('/venues/<venue_id>', methods=['POST']) 
def delete_venue(venue_id):
  try:
        venue = Venue.query.get(venue_id)
        db.session.delete(venue)
        db.session.commit()
  except():
        db.session.rollback()
        flash('An error occurred. Venue ' + venue.name + ' could not be deleted.')
  finally:
        db.session.close()

  return redirect(url_for('venues'))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={ }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data=  Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  res = db.session.query(Artist).filter(Artist.name.contains(request.form['search_term'])).all()
  response = { "count" : len(res),"data"  : res}
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)
  artist.past_shows = [] # TOD0
  artist.past_shows_count =  0 # TOD0
  artist.upcoming_shows = [] # TOD0
  artist.upcoming_shows_count = 0 # TOD
  return render_template('pages/show_artist.html', artist=artist)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={ }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(request.form) # populate local form object with form field values
  if form.validate():
     try :
       artist = Artist()
       form.populate_obj(artist) # populate values of form fields into model object
       db.session.add(artist)
       db.session.commit()
       flash('Artist ' + artist.name + ' was successfully listed!') # on successful db insert, flash success
     except IntegrityError: # handle unique constraint by c
       db.session.rollback()
       flash(request.form['name'] + ' already listed.')
       return redirect(url_for('create_artist_submission')) # how to retain form data ??
     except ():   
       db.session.rollback() 
       #flash(TracebackType.print_exc())
       flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
     finally :
       db.session.close() 
  else :
      flash(form.errors) # validation errror
      return redirect(url_for('create_artist_submission'))
  return render_template('pages/home.html')
  


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data=[]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
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
