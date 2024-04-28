from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import timedelta
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ltUN7a9JZcrzQWFmKtU_QA')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '../instance/test.db')
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app.routes import register_index_routes, register_todo_routes, register_user_routes, register_error_routes
register_index_routes(app)
register_todo_routes(app)
register_user_routes(app)
register_error_routes(app)

from app.models import Todo, User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"Error creating database: {e}")