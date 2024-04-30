from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
from app import app, db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    email_verified = db.Column(db.Boolean, default=False)
    email_token = db.Column(db.String(150))
    todos = db.relationship('Todo', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.id} - {self.username} - {self.email}'
        
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def email_exists(email):
        return User.query.filter_by(email=email).first() is not None
    
    def generate_confirmation_token(self):
        s = Serializer(app.config['SECRET_KEY'], salt=app.config['SECURITY_PASSWORD_SALT'])
        return s.dumps(self.email)

    @staticmethod
    def verify_confirmation_token(token, expiration=3600):
        s = Serializer(app.config['SECRET_KEY'], salt=app.config['SECURITY_PASSWORD_SALT'])
        try:
            email = s.loads(token, max_age=expiration)
            if email:
                return User.query.filter_by(email=email).first()
        except:
            return None    

    def generate_reset_token(self):
        s = Serializer(app.config['SECRET_KEY'])
        token = s.dumps({'user_id': str(self.id)})
        return token

    @staticmethod
    def verify_reset_token(token, expiration=600):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=expiration)
            user_id = data.get('user_id')
            return User.query.get(user_id)
        except:
            return None
        
