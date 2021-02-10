from flask import Flask, render_template, url_for, request, redirect,jsonify
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, current
from sqlalchemy.orm import joinedload



app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/ToDo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app,db)

class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False)
  completed = db.Column(db.Boolean, nullable=False, default=False)
  list_id =db.Column(db.Integer, db.ForeignKey('todolists.id', ondelete='CASCADE'),nullable=False)

  def __repr__(self):
    return f'<Todo {self.id} {self.description} {self.completed} {self.list_id}>'

class ToDoList(db.Model):
  __tablename__='todolists'
  id = db.Column(db.Integer, primary_key=True)
  listname = db.Column(db.String(), nullable=False)
  todos = db.relationship('Todo',backref='todo_list', passive_deletes=True,lazy = True)
  def __repr__(self):
    return f'<TodoList {self.id} {self.listname}>'

#db.create_all()

#print(Todo.query.first())


@app.route('/todos/create', methods=['POST']) #route method
def create_todo():#route handler
  description = request.get_json()['description']
  selected_list_id = request.get_json()['selected_list_id']
  todo = Todo(description=description,list_id = selected_list_id)
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
  return redirect(url_for('index'))

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


@app.route('/todo_list/create', methods=['POST']) #route method
def create_todo_list():#route handler
  description = request.get_json()['description']
  todo = ToDoList(listname=description)
  db.session.add(todo)
  db.session.commit()
  return jsonify({ 'description': todo.listname})
   

@app.route('/')  
def index():
  return redirect(url_for('index_list',todo_list_id= ToDoList.query.first().id)) # passs default id 1 to select first list item todo's
  
@app.route('/lists/<todo_list_id>') 
def index_list(todo_list_id): 
  #print(Todo.query.filter_by(list_id = todo_list_id).order_by('id').all())  
  selected_list_id = todo_list_id
  return render_template('todo_list_index.html',
   selected_list_name= ToDoList.query.get(todo_list_id).listname,
   selected_list_id= todo_list_id,
   todolists= ToDoList.query.all(),
   todos=Todo.query.filter_by(list_id = selected_list_id).order_by('id').all()
   )

@app.route('/todo_list/<todolistId>/update_completed', methods=['POST'])
def update_completed_todo_list(todolistId):
  try:
    completed = request.get_json()['completed']
    todolist_query =  ToDoList.query.options(joinedload('todos')).get(todolistId) # get all the joined data from sql db
    for todo in todolist_query.todos:
      todo.completed = completed
    db.session.commit()
  except:
    db.session.rollback()
  finally:   
    db.session.close()
  return redirect(url_for('index_list',todo_list_id=todolistId)) 
  #return jsonify({'redirect': '/lists/1'}) #for ajax response

@app.route('/delete_todo_list/<todolistId>', methods=['DELETE'])
def delete_todo_list(todolistId):
  try:
    #ToDoList.query.filter_by(id=todolistId).delete()
    #todo = Todo.query.get(todo_id) ALTERNATE WAY
    db.session.delete(ToDoList.query.get(todolistId))
    db.session.commit()
    #print(ToDoList.query.all())
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return jsonify({ 'success': True }) 
    