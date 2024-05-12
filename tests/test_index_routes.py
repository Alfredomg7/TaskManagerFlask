import pytest
from flask import url_for

def test_home_page_not_logged_in(client):
    """Test that the home page displays correctly for not logged-in users."""
    response = client.get(url_for('home'))
    assert response.status_code == 200
    data = response.get_data(as_text=True)
    assert 'Welcome to Task Manager' in data
    assert 'Log In' in data
    assert 'Sign Up' in data
    assert 'About' in data

def test_home_page_logged_in(logged_in_client, add_user):
    """Test that the home page displays user-specific content when logged in."""    
    response = logged_in_client.get(url_for('home'))
    assert response.status_code == 200
    data = response.get_data(as_text=True)
    assert f'Welcome {add_user.username}' in data
    assert 'Add New Task' in data
    assert 'All Tasks' in data
    assert 'Pending Tasks' in data

def test_all_tasks_page(logged_in_client, tasks):
    """Verify that all types of tasks are listed correctly on the tasks page."""
    response = logged_in_client.get(url_for('tasks'))
    assert response.status_code == 200
    data = response.get_data(as_text=True)
    assert 'All Tasks' in data
    assert 'Task for Yesterday' in data
    assert 'Task for Today' in data
    assert 'Task for Tomorrow' in data
    assert 'Task Already Completed' in data

@pytest.mark.parametrize("filter_type, expected_in, expected_not_in", [
    ('expired', ['Task for Yesterday'], ['Task for Today', 'Task for Tomorrow', 'Task Already Completed']),
    ('today', ['Task for Today'], ['Task for Yesterday', 'Task for Tomorrow', 'Task Already Completed']),
    ('upcoming', ['Task for Tomorrow'], ['Task for Yesterday', 'Task for Today', 'Task Already Completed']),
    ('all', ['Task for Yesterday', 'Task for Today', 'Task for Tomorrow'], ['Task Already Completed'])])
def test_pending_tasks_page(logged_in_client, tasks, filter_type, expected_in, expected_not_in):
    """Test filtering of tasks by their due dates."""
    response = logged_in_client.get(url_for('pending', filter=filter_type))
    assert response.status_code == 200
    data = response.get_data(as_text=True)
    assert 'Pending Tasks' in data

    for content in expected_in:
        assert content in data

    for content in expected_not_in:
        assert content not in data

def test_completed_tasks_page(logged_in_client, tasks):
    """Ensure that only completed tasks are displayed on the completed tasks page."""
    response = logged_in_client.get(url_for('completed'))
    assert response.status_code == 200
    data = response.get_data(as_text=True)
    assert 'Completed Tasks'  in data
    assert 'Task Already Completed' in data
    
    assert 'Task for Yesterday' not in data
    assert 'Task for Today' not in data
    assert 'Task for Tomorrow' not in data
   
def test_about_page(client):
    """Verify that the about page is displayed."""
    response = client.get(url_for('about'))
    assert response.status_code == 200
    assert 'About this App' in response.get_data(as_text=True)