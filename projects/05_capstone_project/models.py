from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from flask_migrate import Migrate
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import DATE, DateTime, Integer, SMALLINT, SmallInteger, String
import os 

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL','postgresql://postgres:admin@localhost:5432/UdaCastingCompanyDB')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
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

    movieActorDetails = MovieActorDetails.insert().values(actor_id=actor1.id,movie_id=movie1.id,role="Hero")
    db.session.execute(movieActorDetails) 
    movieActorDetails1 = MovieActorDetails.insert().values(actor_id=actor2.id,movie_id=movie1.id,role="Heroine")
    db.session.execute(movieActorDetails1) 
    movieActorDetails2 = MovieActorDetails.insert().values(actor_id=actor1.id,movie_id=movie2.id,role="Hero")
    db.session.execute(movieActorDetails2) 
    movieActorDetails3 = MovieActorDetails.insert().values(actor_id=actor2.id,movie_id=movie2.id,role="Heroine")
    db.session.execute(movieActorDetails3) 
    movieActorDetails4 = MovieActorDetails.insert().values(actor_id=actor3.id,movie_id=movie2.id,role="Comedian")
    db.session.execute(movieActorDetails4) 

    db.session.commit()


MovieActorDetails = db.Table('MovieActorDetails', db.Model.metadata,
    db.Column('actor_id', db.Integer, db.ForeignKey('actors.id')), 
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id')),
    db.Column('role', db.String)
)
 
class Movies(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer,primary_key=True,autoincrement=True)
    title = Column(String)
    release_date = Column(DATE,nullable=false)
    #actors = db.relationship('Actors', secondary=MovieActorDetails, backref=db.backref('MovieActorDetails', lazy='joined'))

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
    movies = db.relationship('Movies', secondary=MovieActorDetails, backref=db.backref('MovieActorDetails', lazy='joined'))

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

