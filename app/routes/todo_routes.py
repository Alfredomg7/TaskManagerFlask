from flask import request, redirect, render_template, url_for
from app import db
from app.models import Todo
from app.forms import TaskForm

def register_todo_routes(app):

    @app.route('/delete/<int:id>')
    def delete(id):
        task_to_delete = Todo.query.get_or_404(id)

        try:
            db.session.delete(task_to_delete)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return 'There was a problem deleting that task'
        
    @app.route('/update/<int:id>', methods=['GET', 'POST'])
    def update(id):
        task = Todo.query.get_or_404(id)
        form = TaskForm(content=task.content)
        form.submit.label.text = 'Update Task'

        if request.method == 'POST' and form.validate_on_submit():
            task.content = form.content.data
            try:
                db.session.commit()
                return redirect(url_for('index'))
            except:
                return 'There was an issue updating your task'
        
        return render_template('update.html', task=task, form=form)