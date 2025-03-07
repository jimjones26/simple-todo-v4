import pytest
from backend.app.models import Team, create_team
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
