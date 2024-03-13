from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    # Representation method for the model
    def __repr__(self):
        return '<Task %r>' % self.id