from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from flask_migrate import Migrate
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import DATE, DateTime, Integer, SMALLINT, SmallInteger, String

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    #db.create_all() => use migrate 

def db_refresh_with_mock_data():
    db.drop_all()
    db.create_all()


class MovieActorDetails(db.Model):
    __tablename__ = 'movieactordetails'
    __table_args__ = (db.UniqueConstraint('movie_id', 'actor_id', name='unique_constraint_movieactordetails'), )

    id = Column(Integer, primary_key=True,autoincrement=True)
    actor_id  = Column(Integer, db.ForeignKey('actors.id'),nullable=False)
    movie_id = Column(Integer, db.ForeignKey('movies.id'),nullable=False)
    role = Column(String,nullable=False)

    movie = db.relationship('Movies',backref='movie_info',cascade='all, delete') # added cascade to delete when reference data deleted
    actor = db.relationship('Actors',backref='actor_info',cascade='all, delete')  # added cascade to delete when reference data deleted
    
class Movies(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer,primary_key=True,autoincrement=True)
    title = Column(String)
    release_date = Column(DATE,nullable=false)
    actors = db.relationship('MovieActorDetails', backref=db.backref('Movies'))

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
       db.session.add(self)
       db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'id': self.id,
        'title': self.title,
        'release_date': self.release_date,
        }

class Actors(db.Model): 
    __tablename__ = 'actors'

    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String,nullable=False)
    age = Column(Integer,nullable=False)
    gender = Column(String,nullable=False)
    movies = db.relationship('MovieActorDetails', backref=db.backref('Actors'))

    def __init__(self, name, age,gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
       db.session.add(self)
       db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'id': self.id,
        'name': self.name,
        'age': self.age,
        'gender': self.gender,
        }

