from flask import Flask, render_template, request, url_for, flash, redirect
from markupsafe import escape
import sqlite3


app = Flask(__name__)
app.config['SECRET_KEY'] = "your secret key"

def get_db_connection():
    conn = sqlite3.connect('database.db')   
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
@app.route('/index/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/about/')
def about():
    return '<h1>This is a Flask web application.</h1>'

@app.route('/capitalize/<word>')
def capitalize(word):
    return '<h1>{}</h1>'.format(escape(word.capitalize()))

@app.route('/add/<int:n1>/<int:n2>/')
def add(n1, n2):
    return '<h1>{}</h1>'.format(n1 + n2)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')