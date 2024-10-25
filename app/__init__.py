import os
from flask import Flask
from .database import init_db, get_vote_count

def load_env():
    """Load variables from a .env file into environment variables."""
    env_path = os.path.join(os.path.dirname(__file__), '../.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                name, value = line.strip().split('=', 1)
                os.environ[name] = value

def create_app():
    load_env()
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
    app.config['DATABASE'] = 'site.db'

    with app.app_context():
        init_db()

    from .routes import main
    app.register_blueprint(main)

    app.jinja_env.globals['get_vote_count'] = get_vote_count

    return app
