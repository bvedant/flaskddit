import sqlite3
from flask import g
from werkzeug.security import generate_password_hash, check_password_hash

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('site.db')
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL
                  )''')
    db.execute('''CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                  )''')
    db.commit()

def add_user(username, email, password):
    db = get_db()
    password_hash = generate_password_hash(password)
    db.execute('INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
               (username, email, password_hash))
    db.commit()

def validate_user(email, password):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    return user if user and check_password_hash(user['password_hash'], password) else None

def add_post(title, content, user_id):
    db = get_db()
    db.execute('INSERT INTO posts (title, content, user_id) VALUES (?, ?, ?)',
               (title, content, user_id))
    db.commit()

def get_posts():
    db = get_db()
    return db.execute('''
        SELECT posts.id, posts.title, posts.content, posts.user_id, users.username
        FROM posts
        JOIN users ON posts.user_id = users.id
    ''').fetchall()
