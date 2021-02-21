from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()
 
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
  
class Venue(db.Model):
    __tablename__ = 'venues'
    __table_args__ = (db.UniqueConstraint('name'),)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    city = db.Column(db.String(120)) 
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres =  db.Column(db.ARRAY(db.String),server_default="{}")
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    artists = db.relationship('Shows', backref=db.backref('Venue'))

class Artist(db.Model):
    __tablename__ = 'artists'
    __table_args__ = (db.UniqueConstraint('name'),)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres =  db.Column(db.ARRAY(db.String),server_default="{}")
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    venues = db.relationship('Shows', backref=db.backref('Artist'))

class Shows(db.Model):
    __tablename__ = 'shows'
    __table_args__ = (db.UniqueConstraint('venue_id', 'artist_id','start_time', name='unique_constraint_shows'), )

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    venue = db.relationship('Venue',backref='show_venue',cascade='all, delete') # added cascade to delete when reference data deleted
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'),nullable=False)
    artist = db.relationship('Artist',backref='show_artist',cascade='all, delete')  # added cascade to delete when reference data deleted
    artist_id  = db.Column(db.Integer, db.ForeignKey('artists.id'),nullable=False)
    start_time = db.Column(db.DateTime,nullable=False)