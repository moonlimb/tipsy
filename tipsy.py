"""
tipsy.py -- A flask-based todo list
"""
from flask import Flask, render_template, redirect, request, session, g
import model
#g is a special global variable that lets us have multiple users signed on at the same time

app = Flask(__name__)

#This will be executed every time before any view is called
@app.before_request
def set_up_db():
    g.db = model.connect_db()

@app.route("/")
def index():
    return render_template("index.html", user_name="chriszf")

@app.route("/save_task", methods=["POST"])
def save_task():
    title = request.form['title']
    model.new_task(g.db, title)
    return redirect("/tasks")

@app.route("/tasks")
def list_tasks():
    tasks_from_db = model.get_tasks(g.db, None)
    return render_template("list_tasks.html", tasks=tasks_from_db)

@app.route("/task/<int:id>", methods=["GET"])
def view_task(id):
    task_from_db = model.get_task(g.db, id)
    return render_template("view_task.html", task=task_from_db)

@app.route("/task/<int:id>", methods=["POST"])
def complete_task(id):
    model.complete_task(g.db, id)
    return redirect("/tasks")

#executed after each view; closes connection to our database
@app.teardown_request
def disconnect_db(exception):
    g.db.close()

if __name__ == "__main__":
    app.run(debug=True)
