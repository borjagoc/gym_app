import os
import re
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db,  Teacher, Discipline, Session, Gym

managers_token = os.environ['MANAGERS_TOKEN']
teachers_token = os.environ['TEACHERS_TOKEN']


class GymAppTestCase(unittest.TestCase):
    """This class represents the Gym App test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstonedb_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        
        #Dummy data to post
        self.manager_auth_header = {'Content-Type': 'application/json', 'Authorization': 'Bearer '+ managers_token }
        self.teacher_auth_header = {'Content-Type': 'application/json', 'Authorization': 'Bearer '+ teachers_token }

        self.new_teacher = {
            "name": "John Doe",
            "discipline_id": 1,
            "instagram_account": "@JDoe"
        }

        self.amended_teacher = {
            "name": "Crystal Clear",
            "instagram_account": "@CClear"
        }
    
        self.new_teacher = {
            "name": "John Doe",
            "discipline_id": 1,
            "instagram_account": "@JDoe"
        }

        self.new_discipline = {
            "name": 'Calisthenics'
        }

        self.new_session = {
            "name": "Yoga with Francesco on Wednesday",
            "gym_id": 1,
            "teacher_id": 2,
            "discipline_id": 2,
            "start_time": "Wed, 02 Jun 2022 17:20:00 GMT",
            "length_in_minutes": 60
        }


    def tearDown(self):
        """Executed after reach test"""
        pass


    """
    One test for each endpoint for successful operation and for expected errors.
    """

    #POST '/api/teachers' (Sucessful)
    def test_post_new_teacher_with_auth(self):
        req = self.client().post('/teachers', headers=self.manager_auth_header, json=self.new_teacher)
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['teachers']))
    
    #POST '/api/teachers' (No auth error)
    def test_post_new_teacher_no_auth(self):
        req = self.client().post('/teachers', json=self.new_teacher)
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data["message"], "Authorization is not present in the header")
    
    #POST '/api/disciplines' (Sucessful)
    def test_post_new_discipline_with_auth(self):
        req = self.client().post('/disciplines', headers=self.manager_auth_header, json=self.new_discipline)
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['disciplines']))
    
    #POST '/api/disciplines' (No auth error)
    def test_post_new_discipline_no_auth(self):
        req = self.client().post('/disciplines', json=self.new_discipline)
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data["message"], "Authorization is not present in the header")
    
    #GET '/api/teachers' (Sucessful)
    def test_get_all_teachers(self):
        req = self.client().get('/teachers')
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['teachers']))
    
    #GET '/api/disciplines' (Sucessful)
    def test_get_all_disciplines(self):
        req = self.client().get('/disciplines')
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['disciplines']))
    
    #GET '/api/sessions' (Sucessful)
    def test_get_all_sessions(self):
        req = self.client().get('/sessions')
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['sessions']))
    
    #PATCH '/api/teachers' (Sucessful)
    def test_patch_teacher_with_auth(self):
        req = self.client().patch('/teachers/2', headers=self.manager_auth_header, json=self.amended_teacher)
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['teachers']))
    
    #PATCH '/api/teachers' (No auth error)
    def test_patch_teacher_no_auth(self):
        req = self.client().patch('/teachers/2', json=self.amended_teacher)
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data["message"], "Authorization is not present in the header")

    #PATCH '/api/teachers' (Wrong teacher id error)
    def test_patch_teacher_wrong_id(self):
        req = self.client().patch('/teachers/100', headers=self.manager_auth_header, json=self.amended_teacher)
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data["message"], "resource not found")
    
    #DELETE '/api/teachers' (Sucessful)
    def test_delete_teacher_with_auth(self):
        req = self.client().delete('/teachers/1', headers=self.manager_auth_header)
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['teachers']))
    
    #DELETE '/api/teachers' (No auth error)
    def test_delete_teacher_no_auth(self):
        req = self.client().delete('/teachers/1')
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data["message"], "Authorization is not present in the header")

    #DELETE '/api/teachers' (Wrong teacher id error)
    def test_delete_teacher_wrong_id(self):
        req = self.client().delete('/teachers/100', headers=self.manager_auth_header)
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data["message"], "resource not found")

    #POST '/api/sessions' (Sucessful)
    def test_post_new_session_with_auth(self):
        req = self.client().post('/sessions', headers=self.teacher_auth_header, json=self.new_session)
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['sessions']))
    
    #POST '/api/sessions' (No auth error)
    def test_post_new_session_no_auth(self):
        req = self.client().post('/sessions', json=self.new_session)
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data["message"], "Authorization is not present in the header")

# Make the tests conveniently executable
if __name__ == '__main__':
    unittest.main()