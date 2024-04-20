from flask_wtf import FlaskForm
from wtforms import BooleanField

class CompleteForm(FlaskForm):
    completed = BooleanField('Completed')