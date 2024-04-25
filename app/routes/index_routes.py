from flask import request, redirect, render_template, flash
from app import db
from app.models import Todo
from app.forms import TaskForm, CompleteForm

def register_index_routes(app):

    @app.route('/')
    def home():
        form = TaskForm()
        return render_template('home.html', form=form)

    @app.route('/tasks')
    def tasks():
        form = CompleteForm()
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('tasks.html', tasks=tasks, form=form, title='All Tasks')
    
    @app.route('/pending')
    def pending():
        form = CompleteForm()
        tasks = Todo.query.filter_by(completed=False).order_by(Todo.date_created).all()
        return render_template('tasks.html', tasks=tasks, form=form, title="Pending Tasks")
    
    @app.route('/completed')
    def completed():
        form = CompleteForm()
        tasks = Todo.query.filter_by(completed=True).order_by(Todo.date_created).all()
        return render_template('tasks.html', tasks=tasks, form=form, title="Completed Tasks")
    
    @app.route('/about')
    def about():
        return render_template('about.html')