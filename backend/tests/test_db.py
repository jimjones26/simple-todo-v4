import pytest
from backend.app import create_app, db
from sqlalchemy import text  # Import the text function

def test_db_connection():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for testing
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        try:
            db.session.execute(text("SELECT 1"))  # Wrap the SQL expression with text()
            db.session.commit()
        except Exception as e:
            assert False, f"Database connection failed: {e}"
        else:
            assert True, "Database connection successful"
