from unittest import TestCase
from app import app
from flask import session

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class TestBloglyApp(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
    
    def test_index(self):
        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)
            self.assertIn("<h1>", html)
            self.assertEqual(response.status_code, 302)

    def test_users_list(self):
        with self.client as client:
            response = client.get('/users/new')
            html = response.get_data(as_text=True)
            self.assertIn('<label for="fname">', html)
            self.assertEqual(response.status_code, 200)

    def test_process_new_user(self):
        with self.client as client:
            response = client.post("/users/new",
                                   data={'first_name': 'Jim',
                                         'last_name': 'Gaffigan',
                                         'profile_url': ''},
                                   follow_redirects=True)
            html = response.get_data(as_text=True)
            self.assertIn('Jim', html)
            self.assertEqual(response.status_code, 200)
    
    def test_add_post(self):
        with self.client as client: 
            response = client.post("/users/1/posts/new",
                                   data={"post-title": "testing",
                                         "post-content":"test test test"},
                                   follow_redirects=True)
            html = response.get_data(as_text=True)
            self.assertIn("testing", html)
            self.assertEqual(response.status_code, 200)
        
