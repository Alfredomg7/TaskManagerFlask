from flask import render_template, request
from flask_login import login_required, current_user
from datetime import datetime
from app.models import Todo
from app.forms import TaskForm, CompleteForm

def register_index_routes(app):

    @app.route('/')
    def home():
        form = TaskForm()
        return render_template('home.html', form=form, title="Home")

    @app.route('/tasks/all')
    @login_required
    def tasks():
        form = CompleteForm()
        tasks = Todo.query.filter_by(user_id=current_user.id).order_by(Todo.date_created).all()
        return render_template('tasks.html', tasks=tasks, form=form, title='All Tasks')
    
    @app.route('/tasks/pending')
    @login_required
    def pending():
        filter_type = request.args.get('filter', 'all')
        form = CompleteForm()
        today = datetime.today().date()
        if filter_type == 'expired':
            tasks = Todo.query.filter_by(user_id=current_user.id, completed=False).filter(Todo.due_date < today).order_by(Todo.date_created).all()
        elif filter_type == 'today':
            tasks = Todo.query.filter_by(user_id=current_user.id, completed=False).filter(Todo.due_date == today).order_by(Todo.date_created).all()
        elif filter_type == 'upcoming':
            tasks = Todo.query.filter_by(user_id=current_user.id, completed=False).filter(Todo.due_date > today).order_by(Todo.date_created).all()
        else:
            tasks = Todo.query.filter_by(user_id=current_user.id, completed=False).order_by(Todo.date_created).all() 
        return render_template('tasks.html', tasks=tasks, form=form, title="Pending Tasks", filter_type=filter_type)
    
    @app.route('/tasks/completed')
    def completed():
        form = CompleteForm()
        tasks = Todo.query.filter_by(user_id=current_user.id, completed=True).order_by(Todo.date_created).all()
        return render_template('tasks.html', tasks=tasks, form=form, title="Completed Tasks")
    
    @app.route('/about')
    def about():
        return render_template('about.html')