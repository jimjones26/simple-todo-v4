import unittest
from backend.app import create_app
from backend.app import db
from backend.app.models import User, Team, Task  # Import the models

class TestModels(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for testing
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_model_exists(self):
        with self.app.app_context():
            self.assertTrue(hasattr(User, '__tablename__'))

    def test_team_model_exists(self):
        with self.app.app_context():
            self.assertTrue(hasattr(Team, '__tablename__'))

    def test_task_model_exists(self):
        with self.app.app_context():
            self.assertTrue(hasattr(Task, '__tablename__'))

if __name__ == '__main__':
    unittest.main()
