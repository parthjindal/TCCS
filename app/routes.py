from flask.blueprints import Blueprint
from flask_login import login_required
from flask import render_template
from flask_login import current_user
from werkzeug.utils import redirect

main = Blueprint("main",import_name= __name__,template_folder="templates")

@main.route('/')
def index():
    return render_template("about.html",title = "TL;DR")

@main.route('/home')
def home():
    return render_template('index.html', title='TL;DR', user= current_user)



