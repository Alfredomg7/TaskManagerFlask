from flask import request, redirect, render_template, flash
from app import db
from app.models import Todo
from app.forms import TaskForm, CompleteForm

def register_index_routes(app):
    
    @app.route('/', methods=['POST', 'GET'])
    def index():
        task_form = TaskForm()
        complete_form = CompleteForm()

        if request.method == 'POST' and task_form.validate_on_submit():
            task_content = task_form.content.data
            new_task = Todo(content=task_content)

            try:
                db.session.add(new_task)
                db.session.commit()
                flash('Task added!', 'success')
                return redirect('/')
            except:
                flash('There was an issue adding your task', 'error')
                return redirect('/')
        
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks, task_form=task_form, complete_form=complete_form)
        