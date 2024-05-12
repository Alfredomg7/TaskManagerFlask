from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
import os
from dotenv import load_dotenv
from config import DevelopmentConfig, TestingConfig, ProductionConfig

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def setup_database(application):
    with application.app_context():
        if application.config['TESTING']:
            db.session.remove()
            db.drop_all()
        db.create_all()

def create_app(config_name='default'):
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(basedir, '.env'))

    configs = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
        'default': DevelopmentConfig
    }

    config_class = configs.get(config_name, DevelopmentConfig)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    mail.init_app(app)

    from app.routes import register_index_routes, register_todo_routes, register_user_routes, register_error_routes
    register_index_routes(app)
    register_todo_routes(app)
    register_user_routes(app)
    register_error_routes(app)

    from app.models import Todo, User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    setup_database(app)
    
    return app

    