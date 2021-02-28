import os
from types import MethodType
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy #, or_
from flask_cors import CORS
import random
from models import setup_db, Book

BOOKS_PER_SHELF = 8 #paging 

#-------------------------------------------------------#
def create_app(test_config=None):
  app = Flask(__name__) # create and configure the app
  setup_db(app)
  CORS(app)

  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
  
  #Error handlers  
  @app.errorhandler(400)
  def bad_reuest(error):
      return jsonify({
      'success' : False , 
      'error' : 400,
      'message' : 'bad request',
    }),400

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
      'success' : False , 
      'error' : 404,
      'message' : 'resource(book) not found',
    }),404

  @app.errorhandler(405)
  def method_not_allowed(error):
      return jsonify({
      'success' : False , 
      'error' : 405,
      'message' : 'method_not_allowed',
    }),405

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
      'success' : False , 
      'error' : 422,
      'message' : 'unprocessable',
    }),422

  return app
app = create_app() # create app

#----------------------------------- --------------------#

def page_helper(request):
    page = request.args.get('page', 1, type=int) # handler paging , handle UTL arguments
    start = (page - 1) * BOOKS_PER_SHELF
    end = start + BOOKS_PER_SHELF
    
    books = Book.query.order_by(Book.id).all()
    current_page_books = books[start:end]
    total_books_count = len(books)
    current_page_books_count = len(current_page_books)
    fomated_paging_books = [book.format() for book in current_page_books]

    return (fomated_paging_books,total_books_count,current_page_books_count)
    #return fomated_paging_books

@app.route('/')
def hello(): 
  return jsonify( {'message': 'hello flask API' }) 
  
@app.route('/books/') 
def get_books():
  print(request)
  books = page_helper(request) 
  return jsonify( {'success': True , 
                   'books': books[0], 
                   'total_books' : books[1], 
                   'no_of_book_in_page' : books[2] })

@app.route('/books/<int:book_id>/', methods=['GET'])  # to display single bookm info
def get_book_info(book_id):
  book = Book.query.filter(Book.id == book_id).one_or_none()  
  if book is None: # if given id not found in the db then handle it
    abort(404) 
  else   :
    return jsonify({'success': True ,'book' : book.format()})  

@app.route('/books/<int:book_id>', methods=['PATCH']) 
def update_rating(book_id):
  body = request.get_json() # get rating field value from html form
  
  try:
    book = Book.query.filter(Book.id == book_id).one_or_none()
    print(body)
    if book is None or 'rating' not in body: # if given id not found in the db then handle it
      abort(404) 
    
    book.rating = int(body.get('rating')) # get rating attribute from json
    book.update()
    return jsonify({'success': True ,'book_id' : book.id}) 

  except:
      abort(400)

@app.route('/books',methods=['POST'])
def create_book():
  body = request.get_json()
  print(body)
  try :
    title  = body.get('title',None)
    author = body.get('author',None)
    rating = int(body.get('rating',None))
    
    book = Book(title,author,rating)
    book.insert()
    books = page_helper(request) 
    #page not refershing ... but with delete and rating it working
    return jsonify({
      'success' : True , 
      'created' : book.id,
      'books' : books[0],
      'total_books' : books[1],
    })
  except:
      abort(400)   
  
@app.route('/books/<int:book_id>', methods=['DELETE']) 
def delete_book(book_id):
  try:
    book = Book.query.filter(Book.id == book_id).one_or_none()
    if book is None: # if given id not found in the db then handle it
      abort(404) 

    book.delete() 
    books = page_helper(request) 

    return jsonify({
      'success' : True , 
      'deleted' : book.id,
      'books' : books[0],
      'total_books' : books[1],
    })

  except:
      abort(400)

