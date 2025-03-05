import unittest
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sqlalchemy
import pytest
from alembic.config import Config
from alembic import command

# Initialize Flask and SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for testing
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import models (after db is defined)
from backend.app.models import User, Team, Task, user_team

class TestMigrations(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def setup_db(self, app):
        with app.app_context():
            # Initialize Flask-Migrate
            migrate.init_app(app, db)

            # Create Alembic configuration
            alembic_cfg = Config()
            alembic_cfg.set_main_option("script_location", "backend/migrations")
            alembic_cfg.set_main_option("sqlalchemy.url", app.config['SQLALCHEMY_DATABASE_URI'])

            # Run migrations
            command.upgrade(alembic_cfg, "head")

            yield

            # Drop all tables after the test
            db.session.remove()
            db.drop_all()


    def test_tables_exist(self):
        self.db.reflect()  # Reflect the database schema
        table_names = self.db.metadata.tables.keys()

        self.assertIn('user', table_names)
        self.assertIn('team', table_names)
        self.assertIn('task', table_names)
        self.assertIn('user_team', table_names)

if __name__ == '__main__':
    unittest.main()
