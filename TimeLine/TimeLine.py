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

@app.route('/register', methods=['GET', 'POST'])
def createaccount():
    obj = {'email' : '', 'name' : ''}
    if request.method == 'GET':
        return render_template('register.html', **obj)
    print(request.form)
    print( 'verify' in request.form )
    if 'verify' in request.form:
        # 아이디 중복 검사
        if 'email' in request.form:
            obj['email'] = request.form['email']
        if 'name' in request.form:
            obj['name'] = request.form['name']
        print(obj)
        cur = get_db().cursor()
        cur.execute('SELECT UID FROM USER where UID = ?', (request.form['email'],))
        uid = cur.fetchall()
        if len(uid) > 0:
            return render_template('register.html', verify=False, **obj)
        else:
            return render_template('register.html', verify=True, **obj)

    elif 'register' in request.form:
        # TODO (minor) 회원 가입 데이터 유효성 검사
        cur = get_db().cursor()
        cur.execute('INSERT INTO USER (UID, PASSWORD, NAME) VALUES(?,?,?)', (request.form['email'], request.form['password'], request.form['name']))
        get_db().commit()
        # TODO (trivial) 가입시 바로 세션 전달 하면 좋을 것 같다.
        return redirect(url_for('index'))
    return render_template('register.html', **obj)


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
