import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Book

class BookTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "bookshelf_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'admin','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_book = {
            'title': 'Anansi Boys',
            'author': 'Neil Gaiman',
            'rating': 5
        }
        
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()  # create all tables
    
    def tearDown(self):
        print(Book.query.all())
        """Executed after reach test"""
        pass
    
    def test_create_new_book(self):
        res = self.client().get('/books/',json = self.new_book)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)    
        self.assertEqual(data['success'], True)
        #self.assertTrue(data['created'])
        self.assertTrue (len(data['books']))

    def test_get_paginated_books(self):
        res = self.client().get('/books/')
        data = json.loads(res.data)
        #print(data)    
        self.assertEqual(res.status_code, 200)      
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_books'] , 0)
        self.assertTrue (len(data['books']) == 0)

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/books/?page=1')
        data = json.loads(res.data)
        print(data)    
        self.assertEqual(res.status_code, 404)    
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main() 