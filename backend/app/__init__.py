from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS  # Import CORS
from .config import Config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # app.config['SECRET_KEY'] = 'your_secret_key'  <- REMOVE THIS
    # app.config['DEBUG'] = True                    <- REMOVE THIS

    # Enable CORS for all routes and origins
    CORS(app, supports_credentials=True)

    db.init_app(app)
    from . import views

    login_manager.init_app(app)
    migrate.init_app(app, db)
    login_manager.login_view = 'login'

    app.register_blueprint(views.bp)  # Register the blueprint

    return app
