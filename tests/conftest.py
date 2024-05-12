import pytest
from sqlalchemy.orm import scoped_session, sessionmaker
from app import create_app, db
from app.models import User, Todo
from datetime import datetime, timedelta

@pytest.fixture(scope='session')
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture(scope='function')
def session(app):
    connection = db.engine.connect()
    transaction = connection.begin()

    session_factory = sessionmaker(bind=connection)
    Session = scoped_session(session_factory)
    db.session = Session

    yield Session

    Session.remove()
    db.session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope='function')
def add_user(session):
    user = User(username='testuser', email='test@example.com')
    user.set_password('TestPassword')
    user.email_verified = True
    session.add(user)
    session.commit()
    yield user

@pytest.fixture(scope='function')
def logged_in_client(client, add_user):
    client.post('/login', data={
        'username': add_user.username,
        'password': 'TestPassword'
    }, follow_redirects=True)
    yield client

@pytest.fixture(scope='function')
def tasks(add_user, session):
    today = datetime.today().date()
    tasks = [
        Todo(content='Task for Yesterday', user_id=add_user.id, completed=False, due_date=today - timedelta(days=1)),
        Todo(content='Task for Today', user_id=add_user.id, completed=False, due_date=today),
        Todo(content='Task for Tomorrow', user_id=add_user.id, completed=False, due_date=today + timedelta(days=1)),
        Todo(content='Task Already Completed', user_id=add_user.id, completed=True, due_date=today)
    ]
    session.add_all(tasks)
    session.commit()
    return tasks
