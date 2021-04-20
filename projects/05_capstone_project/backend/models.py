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
    
    movie1 = Movies(title="movie1",release_date='1991/01/01')
    movie1.insert()
    movie2 = Movies(title="movie2",release_date='1992/01/01')
    movie2.insert()
    movie3 = Movies(title="movie3",release_date='1993/01/01')
    movie3.insert()
    movie4 = Movies(title="movie4",release_date='1994/01/01')
    movie4.insert()
    movie5 = Movies(title="movie5",release_date='1995/01/01')
    movie5.insert()

    actor1 = Actors(name="actor1",age=50,gender="Male")
    actor1.insert()
    actor2= Actors(name="actor2",age=35,gender="FeMale")
    actor2.insert()
    actor3 = Actors(name="actor3",age=40,gender="Male")
    actor3.insert()
    actor4 = Actors(name="actor4",age=55,gender="FeMale")
    actor4.insert()
    actor5 = Actors(name="actor5",age=60,gender="Male")
    actor5.insert()

    movieActorDetails  = MovieActorDetails(actor_id=actor1.id,movie_id=movie1.id,role="Hero")
    movieActorDetails1 = MovieActorDetails(actor_id=actor2.id,movie_id=movie1.id,role="Heroine")
    movieActorDetails2 = MovieActorDetails(actor_id=actor1.id,movie_id=movie2.id,role="Hero")
    movieActorDetails3 = MovieActorDetails(actor_id=actor2.id,movie_id=movie2.id,role="Heroine")
    movieActorDetails4 = MovieActorDetails(actor_id=actor3.id,movie_id=movie2.id,role="Comedian")
    objs=[movieActorDetails,movieActorDetails1,movieActorDetails2,movieActorDetails3,movieActorDetails4]
    db.session.bulk_save_objects(objs)

    db.session.commit()


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

