from flask import request, redirect, render_template, url_for, flash
from app import db
from app.models import Todo
from app.forms import TaskForm

def register_todo_routes(app):

    @app.route('/add-task', methods=['POST'])
    def add():
        form = TaskForm()
        if request.method == 'POST' and form.validate_on_submit():
            new_task = Todo(
                content= form.content.data,
                due_date = form.due_date.data
                )
            try:
                db.session.add(new_task)
                db.session.commit()
                flash('Task added!', 'success')
                return redirect('/')
            except Exception as e:
                flash(f'There was an issue adding your task: {str(e)}', 'error')
                return redirect(url_for('home'))

    @app.route('/delete/<int:id>')
    def delete(id):
        task_to_delete = Todo.query.get_or_404(id)

        try:
            db.session.delete(task_to_delete)
            db.session.commit()
            flash('Task deleted!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            flash('There was a problem deleting that task', 'error')
            return redirect(url_for('home'))
        
    @app.route('/update/<int:id>', methods=['GET', 'POST'])
    def update(id):
        task = Todo.query.get_or_404(id)
        form = TaskForm(content=task.content)
        form.submit.label.text = 'Update Task'

        if request.method == 'POST' and form.validate_on_submit():
            task.content = form.content.data
            task.due_date = form.due_date.data
            try:
                db.session.commit()
                flash('Task updated!', 'success')
                return redirect(url_for('home'))
            except:
                flash('There was an issue updating your task', 'error')
                return redirect(url_for('home'))
        
        return render_template('update.html', task=task, form=form)
    
    @app.route('/complete/<int:id>', methods=['POST'])
    def complete(id):
        task = Todo.query.get_or_404(id)
        task.completed = not task.completed
        db.session.commit()
        redirect_view = request.args.get('redirect_view', '/')
        return redirect(redirect_view)