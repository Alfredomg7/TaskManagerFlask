import pytest
from flask import url_for, session as flask_session
from flask_login import current_user
from werkzeug.security import check_password_hash
from app.models import User

def test_signup(client, session):
    """
    Test the signup process to ensure that a new user can register correctly.
    Checks if the user is added to the database and a confirmation message is displayed.
    """
    response = client.post(url_for('signup'), data={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'newpassword123',
        'confirm_password': 'newpassword123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Your account has been created! Please check your email to confirm your email address.' in response.get_data(as_text=True)
    user = session.query(User).filter_by(email='newuser@example.com').first()
    assert user is not None
    assert user.username == 'newuser'
    assert check_password_hash(user.password_hash, 'newpassword123')

def test_login(client, add_user):
    """
    Test the login functionality to ensure users can log in with correct credentials.
    Verifies that the user session is created and a success message is displayed.
    """
    response = client.post(url_for('login'), data={
        'username': 'testuser',
        'password': 'TestPassword'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Logged in succesfully!' in response.get_data(as_text=True)
    client.get('/')
    assert current_user.is_authenticated

def test_logout(logged_in_client):
    """
    Test the logout process to ensure it properly ends the user session.
    Verifies that the user is logged out and a logout message is displayed.
    """
    response = logged_in_client.get(url_for('logout'), follow_redirects=True)
    assert response.status_code == 200
    assert 'You have been logget out.' in response.get_data(as_text=True)
    assert 'user_id' not in flask_session

def test_profile_page(logged_in_client, add_user):
    """
    Test the profile page visibility and content for logged-in users.
    Checks for correct display of user-specific information.
    """
    response = logged_in_client.get(url_for('profile'))
    assert response.status_code == 200
    data = response.get_data(as_text=True)
    assert add_user.username in data
    assert add_user.email in data
    assert 'Expired Tasks' in data
    assert 'Due Today' in data
    assert 'Upcoming Tasks' in data

def test_edit_profile(logged_in_client, session, add_user):
    """
    Test the user is able to update their profile information.
    Verifies that changes are reflected in the database and a success message is displayed.
    """
    new_username = 'updateduser'
    new_email = 'updated@example.com'
    new_password = 'newpassword123'
    response = logged_in_client.post(url_for('edit_profile'), data={
        'username': new_username,
        'email': new_email,
        'current_password': 'TestPassword',
        'new_password': new_password,
        'confirm_password': new_password
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Profile updated succesfully!' in response.get_data(as_text=True)
    updated_user = session.query(User).filter_by(id=add_user.id).first()
    assert updated_user.username == new_username
    assert updated_user.email == new_email

def test_confirm_email_valid_token(client, session, add_user):
    """
    Test the email confirmation process with a valid token.
    Ensures that the user's email is verified and a confirmation message is displayed.
    """
    token = add_user.generate_confirmation_token()
    response = client.get(url_for('confirm_email', token=token), follow_redirects=True)
    session.refresh(add_user)
    assert response.status_code == 200
    assert 'Your email has been confirmed, thank you!' in response.get_data(as_text=True)
    assert add_user.email_verified

def test_confirm_email_invalid_token(client):
    """
    Test the email confirmation process with an invalid token.
    Checks for proper error handling and display of an error message.
    """
    response = client.get(url_for('confirm_email', token='invalid-token'), follow_redirects=True)
    assert response.status_code == 200
    assert 'The confirmation link is invalid or has expired.' in response.get_data(as_text=True)

def test_confirm_email_already_confirmed(client, session, add_user):
    """
    Test the behavior when a user attempts to confirm an email that's already been confirmed.
    Ensures that the system correctly identifies and communicates this state.
    """
    token = add_user.generate_confirmation_token()
    client.get(url_for('confirm_email', token=token))
    response = client.get(url_for('confirm_email', token=token), follow_redirects=True)
    assert response.status_code == 200
    assert 'Account already confirmed. Please log in.' in response.get_data(as_text=True)

def test_reset_password_request(client, session, add_user):
    """
    Test the password reset request process for an existing user.
    Verifies that a reset email is prompted and an appropriate message is displayed.
    """
    response = client.post(url_for('reset_password_request'), data={
        'email': add_user.email
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Check your email for the instructions to reset your password' in response.get_data(as_text=True)

def test_reset_password_request_no_user(client, session):
    """
    Test the password reset request for a non-existent user email.
    Ensures that the system still prompts to check the email, maintaining user privacy.
    """
    response = client.post(url_for('reset_password_request'), data={
        'email': 'nonexistent@example.com'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Check your email for the instructions to reset your password' in response.get_data(as_text=True)

def test_reset_password_valid_token(client, session, add_user):
    """
    Test the password reset process with a valid token.
    Checks that the user's password is successfully reset and a confirmation message is displayed.
    """
    token = add_user.generate_reset_token()
    new_password = 'newpassword123'
    response = client.post(url_for('reset_password', token=token), data={
        'password': new_password,
        'confirm_password': new_password
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Your password has been reset' in response.get_data(as_text=True)
    session.refresh(add_user)
    assert add_user.check_password(new_password)

def test_reset_password_invalid_token(client):
    """
    Test the password reset process with an invalid or expired token.
    Verifies correct handling of invalid tokens and displays an error message.
    """
    token = '1234567'
    new_password = 'newpassword123'
    response = client.post(url_for('reset_password', token=token), data={
        'password': new_password,
        'confirm_password': new_password
    }, follow_redirects=True)    
    assert response.status_code == 200
    assert 'This is an invalid or expired token' in response.get_data(as_text=True)