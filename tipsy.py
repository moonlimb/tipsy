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
    model.Task.new(g.db, title, current_user_id)
    return redirect("/tasks")

@app.route("/tasks")
def list_tasks():
    current_user_id = session.get('user_id', None)
    if current_user_id:
        tasks_for_current_user = model.Task.get_all(g.db, current_user_id)
        return render_template("list_tasks.html", tasks=tasks_for_current_user)
    else:
        return redirect("/")

@app.route("/complete_task/<int:id>", methods=["GET","POST"])
def complete_task(id):
    model.Task.complete(g.db,id)
    return redirect("/tasks")

@app.route("/delete_task/<int:id>", methods=["GET","POST"])
def delete_task(id):
    model.Task.delete(g.db,id)
    return redirect("/tasks")

@app.route("/login", methods=["GET","POST"])
def login():
    return render_template("login.html")

@app.route("/logout", methods=["GET","POST"])
def logout():
    session['user_id'] = None
    return redirect("/login")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/signup_complete", methods=["GET", "POST"])
def signup_complete():
    name_given = request.form['signup-name']
    email_given = request.form['signup-email']
    password_given = request.form['signup-password']

    user_already_exists = model.User.exists(g.db, email_given)

    if user_already_exists:
        flash("There is an existing user associated with this email. Please log in below or sign up with a different email.")
        return redirect("/login")

    model.User.new(g.db,email_given, password_given, name_given)
    flash("New account successfully created! Please log in below.")
    return redirect("/login")

@app.route("/", methods=["GET","POST"])
def authenticate():
    email_entered = request.form['email']
    password_entered = request.form['password']
    logged_in_user = model.User.authenticate(g.db, email_entered, password_entered)
    
    if logged_in_user:
        logged_in_user_id = logged_in_user.id
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
