# imports
import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = False 
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# finally
app = Flask(__name__)
app.config.from_object(__name__)
def connect_db():
  return sqlite3.connect(app.config['DATABASE'])

def init_db():
  with closing(connect_db()) as db:
    with app.open_resource('schema.sql', mode='r') as f:
      db.cursor().executescript(f.read())
    db.commit()

@app.before_request
def before_request():
  g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
  db = getattr(g, 'db', None)
  if db is not None:
    db.close()

@app.route('/')
def console():
  piece = g.db.execute('select title, text from advice order by random() limit 1')
  support = [dict(title=row[0], text=row[1]) for row in piece.fetchall()]
  return render_template('console.html', support=support)

@app.route('/add', methods=['POST'])
def add_advice():
  if not session.get('logged_in'):
    abort(401)
  g.db.execute('insert into advice (title, text) values (?, ?)', [request.form['title'], request.form['text']])
  g.db.commit()
  flash('Advice now available to help console all victims of Web 2.0')
  return redirect(url_for('console'))

@app.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
    if request.form['username'] != app.config['USERNAME']:
      error = 'Invalid username'
    elif request.form['password'] != app.config['PASSWORD']:
      error = 'Invalid password'
    else:
      session['logged_in'] = True
      flash('You were logged in')
      return redirect(url_for('console'))
  return render_template('login.html', error=error)

@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  flash('You were logged out')
  return redirect(url_for('console'))

# run this shit
if __name__ == '__main__':
  app.run()
