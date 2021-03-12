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
  def bad_request(error):
      return jsonify({
      'success' : False , 
      'error' : 400,
      'message' : 'bad request',
    }),400

  @app.errorhandler(404)
  def not_found(error):
    message = error.description
    if message is None :
       message ='resource not found'
    return jsonify({
    'success' : False , 
    'error' : 404,
    'message' : message,
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

#---------------------HELPER FUNCATIONS-------------- --------------------#

  def page_helper(request,search=None,category_id=0):
      page = request.args.get('page', 1, type=int) # handler paging , handle UTL arguments
      start = (page - 1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE
      
      if search :
        questions = Question.query.order_by(Question.id).filter(Question.question.ilike(f'%{search}%')).all()
        #print(f' {search} - {len(questions)}')
        # if len(questions) == 0:
        #   abort(404,f'No questions match with search keyword {search}')
      elif category_id:
        questions = Question.query.filter(Question.category_id == category_id).order_by(Question.id).all()   
      else :
        questions = Question.query.order_by(Question.id).all()   

      current_page_questions = questions[start:end]
      total_questions_count = len(questions)
      current_page_questions_count = len(current_page_questions)
      fomated_paging_questions = [q.format() for q in current_page_questions]

      if current_page_questions_count == 0 and search is None and category_id ==0 :
        abort(404,'No more questions exists for this page.')

      return (fomated_paging_questions,total_questions_count,current_page_questions_count)

#---------------------API END POINTS-------------- --------------------#

  @app.route('/')
  def hello(): 
    return jsonify( {'message': 'hello flask API' }) 

  @app.route('/questions/', methods=['GET'])
  def get_questions():
    categories_formated = [category.type for category in Category.query.order_by(Category.id).all()] 
    result = page_helper(request) 
    #print(categories_formated)
    return jsonify( {'success': True , 
                    'questions': result[0],
                    'total_questions': result[1], 
                    'categories': categories_formated, 
                    'current_category': categories_formated[0], 
                    'current_page_questions_count': result[2], 
                    })

  @app.route('/questions/<int:question_id>/', methods=['DELETE'])   
  def delete_question(question_id):
      question = Question.query.filter(Question.id == question_id).one_or_none()
      print(question)
      if question is None:
         abort(404)

      try:  
        question.delete()
        return jsonify({
          'success': True,
          'deleted': question_id
        })
      except:
        abort(422)
  
  @app.route('/questions/', methods=['POST'])
  def create_question():
      body = request.get_json()
      if body is None:
        abort(404)

      search = body.get('search', None)
      categories_formated = [category.type for category in Category.query.order_by(Category.id).all()] 

      new_question = body.get('question', None)
      new_answer = body.get('answer', None)
      new_category = body.get('category', None)
      new_difficulty = body.get('difficulty', None)

      #try:
      if search:
        result = page_helper(request,search) 

        return jsonify({
          'success': True,
          'questions': result[0],
          'total_questions': result[1], 
          'categories': categories_formated,
        })

      else:

        if new_question is None or  new_answer is None or new_category is None or new_difficulty is None: #validations
          abort(404) 

        question_check = Question.query.filter(Question.question.contains(new_question)).first()
        if question_check: #already question exists
          abort(404,f'question - {new_question} is already exists.')

        category = Category.query.filter(Category.type.contains(new_category)).first() # get category id to store at DB
        if category is None:
          abort(404)
        
        question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty,category_id=category.id)
        question.insert()
          

        result = page_helper(request) 

        return jsonify({
          'success': True,
          'created': question.id,
          'questions': result[0],
          'total_questions': result[1], 
          'categories': categories_formated,
        })

      # except:
      #   abort(422)

  @app.route('/categories/', methods=['GET']) 
  def get_categories():
    categories_formated = [category.format() for category in Category.query.order_by(Category.id).all()] 
    print(len(categories_formated))
    return jsonify( {'success': True , 
                    'categories': categories_formated, 
                    'total_categories' :len(categories_formated)})

  @app.route('/categories/<int:category_id>/questions/', methods=['GET'])
  def get_question_by_category(category_id):

    category_list =  Category.query.filter(Category.id == category_id).order_by(Category.id).all()
    if len(category_list) == 0:
      abort(404,'Invalid Category id.')

    categories_formated = [category.type for category in category_list] 
    result = page_helper(request,None,category_id) 
    
    if result[1] == 0:
        abort(404,'No more questions exists for this category.')
    
    return jsonify( {'success': True , 
                    'questions': result[0],
                    'total_questions': result[1], 
                    'categories': categories_formated, 
                    'current_category': categories_formated[0], 
                    'current_page_questions_count': result[2], 
                    })

  @app.route('/quizz/', methods=['POST']) 
  def get_quizz_random():
    body = request.get_json()
    category_id =  body.get('category_id', None)
    prev_question_id =  body.get('prev_question_id', None)
    
    if category_id is None and prev_question_id is None:
      question_id_list = Question.get_id_list()  
      random_question = Question.query.filter(Question.id == random.choice(question_id_list)).first()
    elif category_id is not None and prev_question_id is None:
      question_id_list = Question.get_id_list(category_id)
      random_question = Question.query.filter(Question.id == random.choice(question_id_list)).first()
    elif category_id is not None and prev_question_id is not None:
      question_id_list = Question.get_id_list(category_id)
      question_id_list.remove(prev_question_id)
      random_question = Question.query.filter(Question.id == random.choice(question_id_list)).first()

    return jsonify({
        'success': True, 
        'random_question': random_question.format(), 
        'category_id': random_question.category_id,
        'question_id': random_question.id
      })
  
  return app
 
    