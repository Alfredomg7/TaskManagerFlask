from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid email address')])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, max=20),
        EqualTo('confirm_password', message='Passwords must be the same')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8, max=20)])
    submit = SubmitField('Sign Up')