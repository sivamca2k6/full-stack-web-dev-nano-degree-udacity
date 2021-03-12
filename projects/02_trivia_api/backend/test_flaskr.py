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
            'category': 'Sports',
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

#--------------------QUESTIONS PAGING--------------- --------------------#
    def test_get_paginated_questions_no_page_number(self):
        res = self.client().get('/questions/')
        data = json.loads(res.data)
        #print(data['current_page_questions_count'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(len(data['categories']),7)
        self.assertEqual(data['current_page_questions_count'],len(data['questions']))
    
    def test_get_paginated_questions_with_page_number(self):
        res = self.client().get('/questions/?page=1')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_page_questions_count'],10)
        self.assertEqual(data['current_page_questions_count'],len(data['questions']))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions/?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

#--------------------QUESTIONS DELETE--------------- --------------------#
    # def test_delete_question(self):
    #     question_id_to_deleted = 26
    #     res = self.client().delete(f'/questions/{question_id_to_deleted}/')
    #     data = json.loads(res.data)
    #     #print(data) 
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], question_id_to_deleted)

    def test_404_delete_question_not_exists(self):
        res = self.client().delete('/questions/100/')
        data = json.loads(res.data)
        #print(data) 
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


#--------------------QUESTIONS POST--------------- --------------------#
    # def test_create_question(self):
    #     res = self.client().post('/questions/',json = self.new_question)
    #     data = json.loads(res.data)
    #     #print(data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)

    def test_404_create_question_dublicate(self):
        res = self.client().post('/questions/',json = self.new_question)
        data = json.loads(res.data)
        #print(data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

#--------------------QUESTIONS SEARCH--------------- --------------------#
    def test_search_book_question_with_results(self):
        res = self.client().post('/questions/', json={'search': 'Cricket'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 2)

    def test_search_book_question_without_results(self):
        res = self.client().post('/questions/', json={'search': 'CricketTEST'})
        data = json.loads(res.data)
        #print(data)    
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)

#--------------------CATEGORIES--------------- --------------------#
    def test_get_categories(self):
        res = self.client().get('/categories/')
        data = json.loads(res.data)
        #print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_categories'] > 0)
    
    def test_get_question_by_category(self):
        category_id = 6
        res = self.client().get(f'/categories/{category_id}/questions/')
        data = json.loads(res.data)
        #print(data['questions'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'] > 0)
        self.assertEqual(len(data['questions']), data['total_questions'])
        self.assertTrue(data['categories']) 

    def test_404_get_question_by_invalid_category(self):
        category_id = 60
        res = self.client().get(f'/categories/{category_id}/questions/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Invalid Category id.') 

    def test_404_no_question_category(self):
        category_id = 7
        res = self.client().get(f'/categories/{category_id}/questions/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'No more questions exists for this category.') 
    
    
#--------------------QUIZZ--------------- --------------------#
    def test_get_quizz_no_param(self):
        res = self.client().post('/quizz/',json={})
        data = json.loads(res.data)
        #print(data) 
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['random_question']) 

    def test_get_quizz_category_only(self):
        res = self.client().post('/quizz/',json={'category_id' : 6})
        data = json.loads(res.data)
        #print(data) 
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['category_id'], 6)
        self.assertTrue(data['random_question'])
        
    def test_get_quizz_category_prev_qusestion(self):
        prev_question_id = random.choice([10,11,24,27])
        res = self.client().post('/quizz/',json={'category_id' : 6,'prev_question_id' : prev_question_id })
        data = json.loads(res.data)
        print(data) 
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['category_id'], 6)
        self.assertTrue(data['random_question'])
        self.assertTrue(data['question_id'] != prev_question_id)
 
    def test_405_get_quizz(self):
        res = self.client().get('/quizz/')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)

# Make the tests conveniently executable
if __name__ == "__main__": 
    unittest.main() 