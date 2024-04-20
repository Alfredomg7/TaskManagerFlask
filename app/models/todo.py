from datetime import datetime
from app import db

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    completed = db.Column(db.Boolean, default=False)

    # Representation method for the model
    def __repr__(self):
        return f'<Task {self.id} - {"Completed" if self.completed else "Pending"}>'