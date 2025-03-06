import pytest
from backend.app import db
from backend.app.models import User

def test_database_connection(app):
    """Test that we can connect to the database and perform operations"""
    with app.app_context():
        # Try to add and remove a test user
        test_user = User(username='dbtest', email='dbtest@example.com')
        test_user.set_password('testpass')
        
        db.session.add(test_user)
        db.session.commit()
        
        # Verify user was added
        user = User.query.filter_by(username='dbtest').first()
        assert user is not None
        assert user.username == 'dbtest'
        
        # Clean up
        db.session.delete(user)
        db.session.commit()

def test_database_rollback(app):
    """Test database rollback functionality"""
    with app.app_context():
        # Start with a clean state
        initial_count = User.query.count()
        
        # Try to add a user with invalid data to force an error
        test_user = User(username=None, email='invalid@test.com')  # username cannot be None
        db.session.add(test_user)
        
        try:
            db.session.commit()
            assert False  # Should not reach this line
        except:
            db.session.rollback()
        
        # Verify the database was rolled back
        final_count = User.query.count()
        assert final_count == initial_count