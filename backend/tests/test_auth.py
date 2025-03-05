import pytest
from backend.app import create_app, login_manager  # Import login_manager
from flask_login import LoginManager

def test_login_manager():
    app = create_app()
    #login_manager = LoginManager() #remove this line
    #login_manager.init_app(app)  # Remove this line

    with app.app_context():
        assert login_manager.login_view == 'login'
