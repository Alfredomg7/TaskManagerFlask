from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class TaskForm(FlaskForm):
    content = StringField('Task', validators=[
        DataRequired(),
        Length(max=50, message='50 characters max.')
    ])
    submit = SubmitField('Add Task')