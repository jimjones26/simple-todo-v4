from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS
from .config import Config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for all routes and origins
    CORS(app, supports_credentials=True, origins=['http://localhost:5173', 'http://127.0.0.1:5173', 'http://localhost:5001', 'http://127.0.0.1:5001'])

    db.init_app(app)

    # Import models to register them with db
    from . import models

    login_manager.init_app(app)
    migrate.init_app(app, db)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(id):
        return models.User.query.get(int(id))

    from . import views
    app.register_blueprint(views.bp)

    return app
