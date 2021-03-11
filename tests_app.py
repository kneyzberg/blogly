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

    def test_ (self):
        with self.client as client:
    def test_ (self):
        with self.client as client:
    def test_ (self):
        with self.client as client:
    def test_ (self):
        with self.client as client: