import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

from werkzeug.exceptions import abort

database_name = "trivia"
database_path = "postgres://{}:{}@{}/{}".format('caryn', 'caryn','localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
Category

'''
class Category(db.Model):  
  __tablename__ = 'categories'

  id = Column(Integer, primary_key=True)
  type = Column(String)
  questions = db.relationship('Question', backref='questions_list', lazy=True)

  def __init__(self, type):
    self.type = type

  def format(self):
    return {
      'id': self.id,
      'type': self.type
    }

'''
Question

'''
class Question(db.Model):  
  __tablename__ = 'questions'

  id = Column(Integer, primary_key=True)
  question = Column(String)
  answer = Column(String)
  category_id = db.Column(db.Integer, db.ForeignKey( 'categories.id'), nullable=False)
  difficulty = Column(Integer)
  category = db.relationship('Category', backref='category', lazy=True)
  
  def __init__(self, question, answer, category_id, difficulty):
    self.question = question
    self.answer = answer
    self.category_id = category_id 
    self.difficulty = difficulty

  def get_id_list(category_id=None): 
    if category_id is None:
      return [q.id for q in Question.query.order_by(Question.id).all()]
    else:
      category_list =  Category.query.filter(Category.id == category_id).order_by(Category.id).all()
      if len(category_list) == 0:
        abort(404,'Invalid Category id.')

      return [q.id for q in category_list]

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
      'question': self.question,
      'answer': self.answer,
      'category_id': self.category_id,
      'category': self.category.type,
      'difficulty': self.difficulty
    }

