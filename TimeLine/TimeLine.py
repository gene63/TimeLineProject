import os
import sys
import sqlite3
from datetime import timedelta
from flask import Flask, request, session, render_template, flash, redirect, url_for, g

app = Flask(__name__)
app.secret_key = 'eQv3$2neLj'
app.permanent_session_lifetime = timedelta(hours=2)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('db/TimeLine.db')
    return db

@app.before_first_request
def initiate_db():
    conn = get_db()
    cur = conn.cursor()
    cur.executescript(open('db/schema.sql').read())
    # TODO : by sys argv, dropping database


@app.route('/login', methods=['GET', 'POST'])
def login():
    cur = get_db().cursor()
    if request.method == 'POST':
        print(request.form['userid'])
        cur.execute('SELECT PASSWORD FROM USER where UID=?', (request.form['userid'],))
        pw = cur.fetchall()
        print('timeline', request.form['userid'] == pw[0][0])
        if len(pw) > 0 and request.form['password'] == pw[0][0]:
            print('login success')
            session['userid'] = request.form['userid']
        return redirect(url_for('index'))
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'userid' in session:
        del session['userid']
    return redirect(url_for('index'))

@app.route('/')
def index():
    if 'userid' in session:
        username = session['userid']
        return render_template('index.html', name=username)
    return render_template('landing.html')

@app.teardown_appcontext
def close_connection(exception):
    db = get_db()
    db.close()