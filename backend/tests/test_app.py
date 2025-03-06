import pytest
from backend.app import create_app
from backend.tests.config import TestConfig

def test_app_creation():
    """Test that we can create an app instance"""
    app = create_app()
    assert app is not None

def test_app_testing_config():
    """Test that app loads testing config correctly"""
    app = create_app()
    app.config.from_object(TestConfig)
    
    assert app.config['TESTING'] is True
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'

def test_app_request_context(app):
    """Test that app can handle request context"""
    with app.test_request_context('/'):
        assert app.config['TESTING'] is True

def test_app_error_handlers(client):
    """Test app error handlers"""
    response = client.get('/nonexistent-route')
    assert response.status_code == 404