from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ltUN7a9JZcrzQWFmKtU_QA')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '../instance/test.db')
db = SQLAlchemy(app)

from app.routes import register_index_routes, register_todo_routes
register_index_routes(app)
register_todo_routes(app)

from app.models import Todo
with app.app_context():
    db.create_all()
