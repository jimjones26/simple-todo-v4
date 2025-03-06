from backend.app.config import Config

class TestConfig(Config):
    """Test configuration that uses in-memory SQLite database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False