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

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(cart)
    db.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    # app.config['MAIL_USERNAME'] = 'egret.tccs@gmail.com'
    # app.config['MAIL_PASSWORD'] = 'Egret1234'
    # app.config['MAIL_USE_TLS'] = False
    # app.config['MAIL_USE_SSL'] = True
    # mail = Mail(app)

    return app
