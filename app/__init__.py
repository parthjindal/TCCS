import os
from flask import Flask
# from config import Config
app = Flask(__name__)
# app.config.from_object(Config)
app.config.from_json("../config.json")

from app import routes


