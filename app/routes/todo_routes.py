from flask import request, redirect, render_template, flash
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models import Todo
from app.forms import TaskForm

def register_todo_routes(app):

    @app.route('/add', methods=['GET', 'POST'])
    @login_required
    def add():
        today = datetime.today().date().isoformat()
        form = TaskForm()
        if form.validate_on_submit():
            new_task = Todo(
                content= form.content.data,
                due_date = form.due_date.data,
                user_id = current_user.id,
                )
            try:
                db.session.add(new_task)
                db.session.commit()
                flash('Task added!', 'success')
            except:
                flash(f'There was an issue adding your task', 'error')
            redirect_view = request.form.get('redirect_view', '/')
            return redirect(redirect_view)
        return render_template("add_task.html", form=form, title="Add Task", today=today)
    
    @app.route('/delete/<int:id>')
    @login_required
    def delete(id):
        task_to_delete = Todo.query.filter_by(user_id=current_user.id,id=id).first_or_404()
        try:
            db.session.delete(task_to_delete)
            db.session.commit()
            flash('Task deleted!', 'success')
        except:
            flash('There was a problem deleting that task', 'error')
        redirect_view = request.referrer if request.referrer else '/'
        return redirect(redirect_view)
    
    @app.route('/update/<int:id>', methods=['GET', 'POST'])
    @login_required
    def update(id):
        task = Todo.query.filter_by(user_id=current_user.id, id=id).first_or_404()
        form = TaskForm(content=task.content)
        form.submit.label.text = 'Update Task'

        if form.validate_on_submit():
            task.content = form.content.data
            task.due_date = form.due_date.data
            try:
                db.session.commit()
                flash('Task updated!', 'success')
            except:
                flash('There was an issue updating your task', 'error')
            redirect_view = request.form.get('redirect_view', '/')
            return redirect(redirect_view)        
        return render_template('update.html', task=task, form=form)
    
    @app.route('/complete/<int:id>', methods=['POST'])
    @login_required
    def complete(id):
        task = Todo.query.filter_by(user_id=current_user.id, id=id).first_or_404()
        print(task)
        task.completed = not task.completed
        try:
            db.session.commit()
        except Exception:
            flash(f'There was an issue completing the task')
        redirect_view = request.args.get('redirect_view', '/')
        return redirect(redirect_view)