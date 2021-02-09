from flask import Flask, render_template,jsonify,request,redirect
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/ToDo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app,db)

class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False)
  completed = db.Column(db.Boolean, nullable=False, default=False)
  list_id =db.Column(db.Integer, db.ForeignKey('todolists.id'),nullable=False)

  def __repr__(self):
    return f'<Todo {self.id} {self.description}>'

class ToDoList(db.Model):
  __tablename__='todolists'
  id = db.Column(db.Integer, primary_key=True)
  listname = db.Column(db.String(), nullable=False)
  todos = db.relationship('Todo',backref='todo_list',lazy = True)

#db.create_all()

#print(Todo.query.first())

@app.route('/todos/create', methods=['POST']) #route method
def create_todo():#route handler
  description = request.get_json()['description']
  todo = Todo(description=description)
  db.session.add(todo)
  db.session.commit()
  return jsonify({
    'description': todo.description
  })


@app.route('/todos/<todo_id>/update_completed', methods=['POST'])
def update_completed_todo(todo_id):
  try:
    completed = request.get_json()['completed']
    todo = Todo.query.get(todo_id)
    todo.completed = completed
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('crud_index'))

@app.route('/delete_todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
  try:
    Todo.query.filter_by(id=todo_id).delete()
    #todo = Todo.query.get(todo_id) ALTERNATE WAY
    #db.session.delete(todo)
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return jsonify({ 'success': True })
  
@app.route('/')
def crud_index():
  print("re")
  return render_template('crud_index.html', todos=Todo.query.order_by('id').all())