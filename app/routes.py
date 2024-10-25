from flask import Blueprint, render_template, redirect, url_for, flash, request, session, g
from .database import add_user, validate_user, add_post, get_posts

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    posts = get_posts()
    return render_template('index.html', posts=posts)

@main.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if len(username) < 2 or len(password) < 6:
            flash('Invalid input', 'danger')
            return redirect(url_for('main.register'))

        add_user(username, email, password)
        flash('Account created!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = validate_user(email, password)
        if user:
            session['user_id'] = user['id']
            flash('Login successful!', 'success')
            return redirect(url_for('main.home'))
        flash('Invalid login credentials', 'danger')
    return render_template('login.html')

@main.route("/logout")
def logout():
    session.pop('user_id', None)
    flash('Logged out!', 'info')
    return redirect(url_for('main.home'))

@main.route("/post/new", methods=['GET', 'POST'])
def new_post():
    if 'user_id' not in session:
        flash('Please log in to create a post.', 'warning')
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user_id = session['user_id']
        
        if not title or not content:
            flash('Title and content are required.', 'danger')
            return redirect(url_for('main.new_post'))
        
        add_post(title, content, user_id)
        flash('Post created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('post.html')
