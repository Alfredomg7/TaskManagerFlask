import pytest
from flask import url_for
from app.models import Todo
from datetime import datetime

def test_add_task(logged_in_client, session):
    """
    Test adding a new task through the 'add' route.
    Verifies that the task is correctly added to the database and the appropriate success message is displayed.
    """
    due_date = datetime.strptime('2023-12-31', '%Y-%m-%d').date()
    response = logged_in_client.post(url_for('add'), data={'content': 'New Task', 'due_date': due_date}, follow_redirects=True)
    assert response.status_code == 200
    assert 'Task added!' in response.get_data(as_text=True)

    task = session.query(Todo).filter_by(content='New Task').first()
    assert task is not None
    assert task.due_date == due_date

def test_update_task(logged_in_client, session, add_user):
    """
    Test updating an existing task through the 'update' route.
    Checks that the task content and due date are updated in the database and confirms the success message.
    """
    due_date = datetime.strptime('2023-12-31', '%Y-%m-%d').date()
    task = Todo(content='Old Task', due_date=due_date, user_id=add_user.id)
    session.add(task)
    session.commit()

    new_due_date = datetime.strptime('2024-01-01', '%Y-%m-%d').date()
    response = logged_in_client.post(url_for('update', id=task.id), data={'content': 'Updated Task', 'due_date': new_due_date}, follow_redirects=True)
    assert response.status_code == 200
    assert 'Task updated!' in response.get_data(as_text=True)

    updated_task = session.get(Todo, task.id)
    assert updated_task.content == 'Updated Task'
    assert updated_task.due_date == new_due_date

def test_delete_task(logged_in_client, session, add_user):
    """
    Test deleting a task through the 'delete' route.
    Ensures that the task is removed from the database and a confirmation message is displayed.
    """
    task = Todo(content='Task to Delete', due_date=datetime.strptime('2023-12-31', '%Y-%m-%d').date(), user_id=add_user.id)
    session.add(task)
    session.commit()

    response = logged_in_client.get(url_for('delete', id=task.id), follow_redirects=True)
    assert response.status_code == 200
    assert 'Task deleted!' in response.get_data(as_text=True)
    
    deleted_task = session.get(Todo, task.id)
    assert deleted_task is None

def test_complete_task(logged_in_client, session, add_user):
    """
    Test marking a task as completed through the 'complete' route.
    Validates that the task's 'completed' status is updated in the database.
    """
    task = Todo(content='Task to Complete', due_date=datetime.strptime('2023-12-31', '%Y-%m-%d').date(), user_id=add_user.id, completed=False)
    session.add(task)
    session.commit()

    response = logged_in_client.post(url_for('complete', id=task.id), follow_redirects=True)
    assert response.status_code == 200

    completed_task = session.get(Todo, task.id)
    assert completed_task.completed == True