import pytest
from backend.app.models import Team, create_team, create_user
from backend.app import db

def test_create_team_saves_to_db(app):
    """Test that create_team correctly persists a team to the database"""
    with app.app_context():
        # Create test data
        test_name = "Alpha Team"
        test_description = "First testing team"
        
        # Create team via function under test
        created_team = create_team(name=test_name, description=test_description)
        
        # Query database for the new team
        saved_team = Team.query.filter_by(name=test_name).first()
        
        # Verify persistence and data integrity
        assert saved_team is not None
        assert saved_team.id == created_team.id
        assert saved_team.description == test_description

def test_add_users_to_team(app):
    """Test that add_users correctly adds users to a team"""
    with app.app_context():
        # Create test data
        test_team = create_team(name="Test Team", description="Test Description")
        user1 = create_user(username="user1", email="user1@test.com", password="pass", role="user")
        user2 = create_user(username="user2", email="user2@test.com", password="pass", role="user")

        # Add users to team
        test_team.add_users([user1, user2])
        db.session.commit()

        # Verify database state
        saved_team = Team.query.get(test_team.id)
        assert len(saved_team.users) == 2
        assert user1 in saved_team.users
        assert user2 in saved_team.users
