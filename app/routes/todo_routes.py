from flask import request, redirect, render_template, url_for
from app import db
from app.models import Todo

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
        
    @app.route('/update/<int:id>', methods=['GET, POST'])
    def update(id):
        task = Todo.query.get_or_404(id)

        if request.method == 'POST':
            task_content = request.form['content']
            try:
                db.session.commit()
                return redirect(url_for('index'))
            except:
                return 'There was an issue updating your task'
        
        return render_template('update.html', task=task)