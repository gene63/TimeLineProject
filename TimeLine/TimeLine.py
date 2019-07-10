import os
import sqlite3
from flask import Flask, request, session, render_template, flash

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')