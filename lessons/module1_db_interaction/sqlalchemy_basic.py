from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Person(db.Model):
  __tablename__ = 'persons'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False) # can check constrinat before insert

db.create_all() # create table if not exists

@app.route('/')
def index():
  person = Person.query.first()
  person = Person(name='Siva') # insert
  db.session.add(person)
  db.session.commit()
  print(Person.query.count())
  res = Person.query.filter_by(name='Siva')
  print (res)
  return 'Hello ' + person.name