import pytest
from backend.app.models import User
from backend.app import db

class TestMigrations:
    @pytest.fixture(autouse=True)
    def setup_db(self, app):
        self.app = app
        self.db = db
        with app.app_context():
            yield

    def test_tables_exist(self):
        with self.app.app_context():
            user_count = User.query.count()
            assert user_count >= 0