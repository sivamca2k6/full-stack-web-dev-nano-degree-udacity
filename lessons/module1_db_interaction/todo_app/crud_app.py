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

  def __repr__(self):
    return f'<Todo {self.id} {self.description}>'

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
    print('completed', completed)
    todo = Todo.query.get(todo_id)
    todo.completed = completed
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('crud_index'))


@app.route('/')
def crud_index():
  return render_template('crud_index.html', todos=Todo.query.order_by('id').all())