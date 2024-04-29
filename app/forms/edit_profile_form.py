from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, Length
from flask_login import current_user
from werkzeug.security import check_password_hash
from app.models import User

class EditProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Current Password", validators=[DataRequired()])
    submit = SubmitField("Save Changes")

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first() and username.data != current_user.username:
            raise ValidationError("Username already exists. Please choose a different one.")
    
    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first() and email.data != current_user.email:
            raise ValidationError("Email already exists. Please choose a different one.")
    
    def validate_password(self, password):
        if not check_password_hash(current_user.password_hash, password.data):
            raise ValidationError("Incorrect password. Please try again.")  # Error for incorrect password
        return True