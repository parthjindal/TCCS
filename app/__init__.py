import os
from flask import Flask
from flask.helpers import url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login = LoginManager()

from app.auth import auth
from app.routes import main


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(auth)
    app.register_blueprint(main)
    db.init_app(app)
    login.init_app(app)
    return app
