import os
from flask import Flask
from flask.helpers import url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
login = LoginManager()
mail = Mail()

from app.routes import main
from app.auth import auth
from app.cart import cart

def create_app(config = Config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(cart)
    db.init_app(app)
    login.init_app(app)
    mail.init_app(app)

    return app
