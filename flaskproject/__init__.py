from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# to hash and verify pass we should use bcrypt
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flaskproject.config import Config


# create database instance
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    from flaskproject.users.routes import users
    from flaskproject.posts.routes import posts
    from flaskproject.main.routes import main
    from flaskproject.errors.handlers import errors

    app.register_blueprint(users)
    # local host:5000/blog
    app.register_blueprint(posts, url_prefix="/blog")
    app.register_blueprint(main)
    app.register_blueprint(errors)
    return app
