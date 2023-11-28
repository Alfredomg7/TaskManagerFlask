from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# Define the Todo model for SQLAlchemy
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Unique ID for each task
    content = db.Column(db.String(200), nullable=False) # Task content
    date_created = db.Column(db.DateTime, default=datetime.utcnow) # Timestamp

    # Representation method for the model
    def __repr__(self):
        return '<Task %r>' % self.id

# Route for the index page, supports both POST and GET methods
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        # Get task content from form
        task_content = request.form['content']
        # Create new Todo item
        new_task = Todo(content=task_content)

        # Add new task to the database and commit
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error adding your task'
    else:
        # Retrieve all tasks from the database, ordered by creation date
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

# Route to delete a task, <int:id> ensures the id is an integer
@app.route('/delete/<int:id>')
def delete(id):
    # Retrieve task by id or return 404
    task_to_delete = Todo.query.get_or_404(id)

    # Delete task from the database and commit
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an error deleting that task'

# Route to update a task, supports both GET and POST methods
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    # Retrieve task by id or return 404
    task = Todo.query.get_or_404(id)

    # Update task content and commit to the database
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except: 
            return "There was an error updating your task"
    else:
        # Render the update task template
        return render_template("update.html", task=task)

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)
