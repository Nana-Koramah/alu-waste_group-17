import unittest
from app import create_app, db
from app.models import User

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Smart Waste Management', response.data)

    def test_register_login_logout(self):
        response = self.client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to login
        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to dashboard
        with self.client.session_transaction() as session:
            user_id = session['_user_id']
        self.assertIsNotNone(User.query.get(int(user_id)))
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)  # Redirect to index
