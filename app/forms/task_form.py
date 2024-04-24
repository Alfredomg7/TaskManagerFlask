from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired, Length

class TaskForm(FlaskForm):
    content = StringField('Task', validators=[
        DataRequired(),
        Length(max=50, message='50 characters max.')
    ])
    
    due_date = DateField('Due Date', format='%Y-%m-%d', 
                         validators=[DataRequired()])
    
    submit = SubmitField('Add Task')