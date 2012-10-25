"""
tipsy.py -- A flask-based todo list
"""
from flask import Flask, render_template, redirect, request, session, g, flash
import model
#g is a special global variable that lets us have multiple users signed on at the same time

app = Flask(__name__)

SECRET_KEY = 'moon_and_sanby_are_awesome'
app.config.from_object(__name__)

#This will be executed every time before any view is called
@app.before_request
def set_up_db():
    g.db = model.connect_db()

@app.route("/")
def index():
    return render_template("index.html", user_name="chriszf")

@app.route("/set_date")
def set_date():
    session['date'] = datetime.datetime.now()
    return "Date set"

@app.route("/get_date")
def get_date():
    return str(session['date'])

@app.route("/save_task", methods=["POST"])
def save_task():
    current_user_id = session.get("user_id",None)
    title = request.form['title']
    model.new_task(g.db, title, current_user_id)
    return redirect("/tasks")

@app.route("/tasks")
def list_tasks():
    current_user_id = session.get('user_id', None)
    if current_user_id:
        tasks_for_current_user = model.get_tasks(g.db, current_user_id)
        return render_template("list_tasks.html", tasks=tasks_for_current_user)
    else:
        return redirect("/")

@app.route("/task/<int:id>", methods=["GET"])
def view_task(id):
    task_from_db = model.get_task(g.db, id)
    return render_template("view_task.html", task=task_from_db)

@app.route("/task/<int:id>", methods=["POST"])
def complete_task(id):
    model.complete_task(g.db, id)
    return redirect("/tasks")

@app.route("/login", methods=["GET","POST"])
def login():
    return render_template("login.html")

@app.route("/logout", methods=["GET","POST"])
def logout():
    session['user_id'] = None
    return redirect("/login")

@app.route("/authenticate", methods=["GET","POST"])
def authenticate():
    email_entered = request.form['email']
    password_entered = request.form['password']
    logged_in_user = model.authenticate(g.db, email_entered, password_entered)
    
    if logged_in_user:
        logged_in_user_id = logged_in_user['id']
        session['user_id'] = logged_in_user_id
        return redirect("/tasks")
    
    flash("Invalid username or password")
    return redirect("/login")

#executed after each view; closes connection to our database
@app.teardown_request
def disconnect_db(exception):
    g.db.close()

if __name__ == "__main__":
    app.run(debug=True)
