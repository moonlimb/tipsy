"""
model.py
"""
import sqlite3
import datetime

def connect_db():
    return sqlite3.connect("tipsy.db")


def insert_into_db(db, table_name, table_columns, values):
    c = db.cursor()
    query_template = """INSERT INTO %s VALUES(%s)"""

    num_question_marks = len(table_columns) - 1
    question_marks_list = ["NULL"] + (["?"] * num_question_marks)
    question_marks_string = ', '.join(question_marks_list)

    query = query_template % (table_name, question_marks_string)

    #c.execute returns another cursor
    res = c.execute(query, tuple(values))   #need to wrap tuple around values because we are passing in a list

    if res:
        db.commit()
        return res.lastrowid


def get_from_table_by_id(db, table_name, target_id, make_user_or_task):
    c = db.cursor()
    
    query_template = """SELECT * from %s WHERE id = ?"""
    query = query_template %(table_name)

    c.execute(query, (target_id,))
    row = c.fetchone()

    if row:

        resulting_user = User(row[0], row[1], row[2], row[3])

    return None


class User(object):

    COLS = ['id', 'email', 'password', 'username']
    TABLE_NAME = "Users"

    def __init__(self, id, email, password, name):
        self.id = id
        self.email = email
        self.password = password
        self.name = name

    @classmethod
    def new(cls, db, email, password, name):
        values = [email, password, name]
        return insert_into_db(db, cls.TABLE_NAME, cls.COLS, values)

    @classmethod
    def authenticate(cls, db, email, password):
        c = db.cursor()
        query = """SELECT * from %s WHERE email=? AND password=?""" %(cls.TABLE_NAME)
        c.execute(query, (email, password))
        result = c.fetchone()
        if result:
            return cls(*result)

        return None

    @classmethod
    def get(cls, db, user_id):
        return cls
        return get_from_table_by_id(db, cls.TABLE_NAME, user_id, )


def get_user(db, user_id):
    """Gets a user dictionary out of the database given an id"""
    return get_from_table_by_id(db, "Users", user_id, make_user)


# class Task(object):
    COLS = ['id','title','created_at','completed_at','user_id']]

#ORM = object relational mapping?



TASK_COLS = ['id','title','created_at','completed_at','user_id']



def new_task(db, title, user_id):
    values = [title, datetime.datetime.now(), None, user_id]
    return insert_into_db(db, "Tasks", TASK_COLS, values)





def make_task(row):
    columns = ["id", "title", "created_at", "completed_at", "user_id"]
    return dict(zip(columns, row))


def get_task(db, task_id):
    """Gets a single task, given its id. Returns a dictionary of the task data."""
    return get_from_table_by_id(db, "Tasks", task_id, make_task)

def get_tasks(db, user_id=None):
    """Get all the tasks matching the user_id, getting all the tasks in the system if the user_id is not provided. Returns the results as a list of dictionaries."""
    c = db.cursor()
    if user_id:
        query = """SELECT * from Tasks WHERE user_id = ?"""
        c.execute(query, (user_id,))
    else:
        query = """SELECT * from Tasks"""
        c.execute(query)
    tasks = []
    rows = c.fetchall()
    for row in rows:
        task = make_task(row)
        tasks.append(task)

    return tasks

def complete_task(db, task_id):
    """Mark the task with the given task_id as being complete."""
    c = db.cursor()
    query = """UPDATE Tasks SET completed_at=DATETIME('now') WHERE id=?"""
    res = c.execute(query, (task_id,))
    if res:
        db.commit()
        return res.lastrowid
    else:
        return None










