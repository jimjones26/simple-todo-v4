from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager  # Import LoginManager
from flask_migrate import Migrate
from .config import Config

db = SQLAlchemy()
login_manager = LoginManager()  # Initialize LoginManager
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['DEBUG'] = True

    db.init_app(app)

    login_manager.init_app(app)  # Initialize LoginManager with the app
    migrate.init_app(app, db)
    login_manager.login_view = 'login'  # Set the login view

    return app
