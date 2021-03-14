import os
import random
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('caryn', 'caryn','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'Who scored the highest one day cricket runs ? ',
            'answer': 'Sachin Tendulkar',
            'category': '6',
            'difficulty' :'3'
        }
        self.new_question_no_category= {
            'question': 'Who scored the highest one day cricket runs ? ',
            'answer': 'Sachin Tendulkar',
            'category': None,
            'difficulty' :'3'
        }
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

#--------------------GET QUESTIONS --------------- --------------------#
    def test_get_paginated_questions_no_page_number(self):
        res = self.client().get('/questions/')
        data = json.loads(res.data)
        #print(data['current_page_questions_count'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(len(data['categories']),6)
        self.assertEqual(data['current_page_questions_count'],len(data['questions']))
    
    def test_get_paginated_questions_with_page_number(self):
        res = self.client().get('/questions/?page=1')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_page_questions_count'],10)
        self.assertEqual(data['current_page_questions_count'],len(data['questions']))

    def test_error_404__get_question_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions/?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
    
    def test_error_405_get_paginated_questions(self):
        res = self.client().patch('/questions/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], "method not allowed")
        self.assertEqual(data['success'], False)

    def test_get_question_by_category(self):
        category_id = 1
        res = self.client().get(f'/categories/{category_id}/questions/')
        data = json.loads(res.data)
        #print(data['questions'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'] > 0)
        self.assertEqual(len(data['questions']), data['total_questions'])
        self.assertTrue(data['categories']) 

    def test_error_404_get_question_by_invalid_category(self):
        category_id = 60
        res = self.client().get(f'/categories/{category_id}/questions/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Invalid Category id.') 
    


# #--------------------QUESTIONS DELETE--------------- --------------------#
    def test_delete_question(self):

        res = self.client().post('/questions/', json = self.new_question)
        data = json.loads(res.data)
        question_id_to_deleted = data['created'] # contains id from newly created question
        
        res = self.client().delete(f'/questions/{question_id_to_deleted}/')
        data = json.loads(res.data)
        #print(data) 
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id_to_deleted)

    def test_error_404_delete_question_not_exists(self):
        res = self.client().delete('/questions/100/')
        data = json.loads(res.data)
        #print(data) 
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


# #--------------------QUESTIONS POST--------------- --------------------#
    def test_create_question(self):
        res = self.client().post('/questions/',json = self.new_question)
        data = json.loads(res.data)
        #print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_error_404_create_question_no_category(self):
        res = self.client().post('/questions/',json = self.new_question_no_category)
        data = json.loads(res.data)
        #print(data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

# #--------------------QUESTIONS SEARCH--------------- --------------------#
    def test_search_book_question_with_results(self):
        res = self.client().post('/questions/', json={'searchTerm': 'Who'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']) > 0)

    def test_search_book_question_without_results(self):
        res = self.client().post('/questions/', json={'searchTerm': 'CricketTEST'})
        data = json.loads(res.data)
        #print(data)    
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)

# #--------------------CATEGORIES--------------- --------------------#
    def test_get_categories(self):
        res = self.client().get('/categories/')
        data = json.loads(res.data)
        #print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_categories'] > 0)
    
    def test_error_405_get_categories_wrong_http_method(self):
        res = self.client().patch('/categories/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], "method not allowed")
        self.assertEqual(data['success'], False)
    
    
# #--------------------QUIZZ--------------- --------------------#
    def test_get_quizz_random_all_category_no_prev(self):
        res = self.client().post('/quizzes/',json={'previous_questions': [], 'quiz_category': {'type': 'click', 'id': 0}})
        data = json.loads(res.data) 
        #print(data) 
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])  

    def test_get_quizz_random_category_only(self):
        res = self.client().post('/quizzes/',json={'previous_questions': [], 'quiz_category': {'type': 'click', 'id': 5}})
        data = json.loads(res.data)
        #print(data) 
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question']) 
    
    def test_error_404_get_quizz_random_invalid_category(self):
        res = self.client().post('/quizzes/',json={'previous_questions': [], 'quiz_category': {'type': 'Sports', 'id': 50}})
        data = json.loads(res.data)
        #print(data) 
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False) 
        
    def test_get_quizz_random_category_prev_qusestion(self):
        res = self.client().post('/quizzes/',json={'previous_questions': [10, 11], 'quiz_category': {'type': 'Sports', 'id': 5}})
        data = json.loads(res.data)
        print(data) 
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
 
    def test_error_404_get_quizz_random_wrong_http(self):
        res = self.client().get('/quizzes/')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)

    def test_error_404_get_quizz_random_no_body(self):
        res = self.client().post('/quizzes/')
        data = json.loads(res.data)
        #print(data) 
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False) 

# Make the tests conveniently executable
if __name__ == "__main__": 
    unittest.main() 