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

def test_remove_users_from_team_updates_membership(app):
    """Test that remove_users_from_team correctly removes users from a team"""
    with app.app_context():
        # Create test team and users
        test_team = create_team(name="Test Team", description="Team for removal testing")
        user1 = create_user(username="remove1", email="remove1@test.com", password="pass", role="user")
        user2 = create_user(username="remove2", email="remove2@test.com", password="pass", role="user")
        user3 = create_user(username="remain", email="remain@test.com", password="pass", role="user")
        
        # Add all users to team
        test_team.add_users([user1, user2, user3])
        db.session.commit()

        # Remove first two users via function under test
        from backend.app.models import remove_users_from_team
        remove_users_from_team(team_id=test_team.id, user_ids=[user1.id, user2.id])

        # Verify updated membership
        updated_team = Team.query.get(test_team.id)
        assert len(updated_team.users) == 1
        assert user3 in updated_team.users
        assert user1 not in updated_team.users
        assert user2 not in updated_team.users
