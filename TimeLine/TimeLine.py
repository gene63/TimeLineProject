import os
import sqlite3
from datetime import timedelta
from flask import Flask, request, session, render_template, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'eQv3$2neLj'
app.permanent_session_lifetime = timedelta(hours=2)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == 'timeline' and request.form['userid'] == 'timeline':
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