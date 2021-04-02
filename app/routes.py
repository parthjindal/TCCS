from flask.blueprints import Blueprint
from flask import render_template
from flask_login import current_user, login_required
from werkzeug.utils import redirect
from app.models import Consignment

main = Blueprint("main", import_name = __name__,template_folder="templates")

@main.route('/')
def index():
    return render_template("about.html",title = "TL;DR")

@main.route('/home')
def home():
    return render_template('index.html', title='TL;DR', user= current_user)

@main.route('/consignments')
@login_required
def consignments():
    if current_user.is_authenticated and current_user.role == "employee":
        consigns = Consignment.query.filter_by(srcBranchId=current_user.branchID).all()
    elif current_user.is_authenticated and current_user.role == "manager":
        consigns = Consignment.query.all()
    return render_template('consignments.html', data=consigns)