import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  CORS(app) 
  
  # CORS Headers 
  @app.after_request 
  def after_request(response):
      response.headers.add('Access-Control-Allow-Origin', '*')
      response.headers.add('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
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


  def page_helper(request,search=None):
      page = request.args.get('page', 1, type=int) # handler paging , handle UTL arguments
      start = (page - 1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE

      questions = Question.query.order_by(Question.id).all()   

      current_page_questions = questions[start:end]
      total_questions_count = len(questions)
      current_page_questions_count = len(current_page_questions)
      fomated_paging_questions = [q.format() for q in current_page_questions]

      if current_page_questions_count == 0:
        abort(404)

      return (fomated_paging_questions,total_questions_count,current_page_questions_count)
      #return fomated_paging_books

#----------------------------------- --------------------#

  @app.route('/')
  def hello(): 
    return jsonify( {'message': 'hello flask API' }) 

  @app.route('/questions/', methods=['GET'])
  def get_questions():
    categories_formated = [category.type for category in Category.query.order_by(Category.id).all()] 
    result = page_helper(request) 
    print(categories_formated)
    return jsonify( {'success': True , 
                    'questions': result[0],
                    'total_questions': result[1], 
                    'categories': categories_formated, 
                    'current_category': categories_formated[0], 
                    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route('/categories/', methods=['GET']) 
  def get_categories():
    categories_formated = [category.format() for category in Category.query.order_by(Category.id).all()] 
    print(len(categories_formated))
    return jsonify( {'success': True , 
                    'categories': categories_formated, 
                    'total_categories' :len(categories_formated)})
  
  return app

    