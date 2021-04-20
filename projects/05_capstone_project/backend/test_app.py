import os
import unittest
import json
from flask_migrate import Config
from flask_sqlalchemy import SQLAlchemy
from models import setup_db,db_refresh_with_mock_data,Movies,Actors
from app import create_app

class UdaCastingAgencyTestCase(unittest.TestCase):
    """This class represents the test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        self.new_movie = {
            'title': 'movie test1 ', 
            'release_date': '1991/01/01',
        }
        self.new_actor = {
            'name': 'actor test1 ',
            'age': '44',
            'gender': 'Male',
        }
        
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            #self.db.create_all() # create all tables
    
    def tearDown(self):
        """Executed after reach test"""
        pass

  #------------------ GET TESTING --------------------------------------
    def test_get_movies(self):
        res=self.client().get('/movies/')
        #print(res)
        data= json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertGreater(data['count'],0 )
        self.assertTrue(len(data['movies']))

    def test_get_movies_wrong_url(self):
        res=self.client().get('/movies1123/')
        self.assertEqual(res.status_code, 404)

    def test_get_actors(self):
        res=self.client().get('/actors/')
        #print(res)
        data= json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertGreater(data['count'],0 )
        self.assertTrue(len(data['actors']))

    def test_get_actors_wrong_url(self):
        res=self.client().get('/actors1123/')
        self.assertEqual(res.status_code, 404)

if __name__ == "__main__":
    unittest.main()
