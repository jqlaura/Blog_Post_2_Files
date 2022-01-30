from flask import Flask, g, render_template, request

import sklearn as sk
import matplotlib.pyplot as plt
import numpy as np
import pickle
import sqlite3

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import io
import base64

# here's how we could initialize our SQL database using Flask
def init_auth_db():
    db = get_auth_db()

    with current_app.open_resource('init.sql') as f:
        db.executescript(f.read().decode('utf8'))


# Create web app, run with flask run
# (set "FLASK_ENV" variable to "development" first!!!)

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('main.html')

@app.route('/submit/', methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        get_message_db()
        insert_message(request)
        return render_template('submit.html', thank = True)

@app.route('/view/')


def view():
   messages = random_messages(5)
   return render_template('view.html', AllMessages = messages)



def get_message_db():
    if 'message_db' not in g:
        g.message_db = sqlite3.connect('message_db.sqlite')
    cursor = g.message_db.cursor()
    cmd = '''CREATE TABLE IF NOT EXISTS messages 
            (id INT, handle TEXT, message TEXT)'''
    cursor.execute(cmd)
    return g.message_db

    
def insert_message(request):
    message = request.form["message"]
    handle = request.form["handle"]
    cursor = g.message_db.cursor()
    cursor.execute("select count(*) from messages")
    id = 1 + cursor.fetchone()[0]
    cmd = '''INSERT INTO messages VALUES 
    ({id},'{handle}','{message}')
    '''.format(id=id, handle=handle, message=message)
    cursor.execute(cmd)
    g.message_db.commit()
    g.message_db.close()


def random_messages(n):
    g.message_db = get_message_db()
    cursor = g.message_db.cursor()
    cursor.execute("select count(*) from messages")
    rows = cursor.fetchone()[0]
    if rows > n:
        rows = n
    cmd = '''
    SELECT message,handle FROM messages ORDER BY RANDOM() LIMIT {rows};
    '''.format(rows=rows)
    cursor.execute(cmd)
    messages = cursor.fetchall()
    g.message_db.close()
    return messages

