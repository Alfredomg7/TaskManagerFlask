from flask import request, redirect, render_template
from app import db
from app.models import Todo

def register_index_routes(app):
    
    @app.route('/', methods=['POST', 'GET'])
    def index():
        if request.method == 'POST':
            task_content = request.form['content']
            new_task = Todo(content=task_content)

            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')
            except:
                return 'There was an issue adding your task'
        
        else:
            tasks = Todo.query.order_by(Todo.date_created).all()
            return render_template('index.html', tasks=tasks)
        