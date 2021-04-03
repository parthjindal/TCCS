from flask.blueprints import Blueprint
from flask import render_template, flash, url_for
from flask_login import current_user, login_required
from werkzeug.utils import redirect
from werkzeug.urls import url_parse
from app.models import Consignment, BranchOffice, Truck

main = Blueprint("main", import_name = __name__,template_folder="templates")

@main.route('/')
def index():
    return render_template("about.html",title = "TL;DR")

@main.route('/home')
def home():
    if current_user.is_authenticated and current_user.role=="manager":
        return render_template('manager.html', title='TL;DR')
    elif current_user.is_authenticated and current_user.role=="employee":
        return render_template('employee.html', title='TL;DR')
    return render_template('index.html', title='TL;DR', user= current_user)

@main.route('/consignments')
@login_required
def consignments():
    if current_user.is_authenticated and current_user.role == "employee":
        consigns = Consignment.query.filter_by(srcBranchId=current_user.branchID).all()
    elif current_user.is_authenticated and current_user.role == "manager":
        consigns = Consignment.query.all()
    return render_template('consignments.html', data=consigns)

@main.route('/branches')
@login_required
def branches():
    if current_user.is_authenticated and current_user.role == "manager":
        branches = BranchOffice.query.all()
        return render_template('branches.html', data=branches)
    flash('You are not authorized to access this page', 'warning')
    return redirect(url_for('main.home', role=current_user.role))

@main.route('/branches/<token>')
@login_required
def branch(token):
    if current_user.is_authenticated and current_user.role == "manager":
        brnch = BranchOffice.query.filter_by(id=token).first()
        return render_template('branch.html', name=brnch.name, trck=brnch.trucks, consign=brnch.consignments)
    flash('You are not authorized to access this page', 'warning')
    return redirect(url_for('main.home', role=current_user.role))

@main.route('/trucks')
@login_required
def trucks():
    if current_user.is_authenticated and current_user.role == "manager":
        trucks = Truck.query.all()
    elif current_user.is_authenticated and current_user.role == "employee":
        trucks = Truck.query.filter_by(branchId=current_user.branchID)
    return render_template('trucks.html', data=trucks)

@main.route('/trucks/<token>')
@login_required
def truck(token):
    if current_user.is_authenticated and current_user.role == "manager":
        truck = Truck.query.filter_by(id=token).first()
        return render_template('truck.html', trck=truck, consign=truck.consignments)
    flash('You are not authorized to access this page', 'warning')
    return redirect(url_for('main.home', role=current_user.role))

# @main.route('/manager')
# @login_required
# def manager():
#     if current_user.is_authenticated and current_user.role == "manager":
#         return render_template('manager.html')
#     flash('You are not authorized to access this page', 'warning')
#     return redirect(url_for('main.home', role=current_user.role))

# @main.route('/employee')
# @login_required
# def employee():
#     if current_user.is_authenticated and current_user.role == "employee":
#         return render_template('employee.html')
#     flash('You are not authorized to access this page', 'warning')
#     return redirect(url_for('main.home', role=current_user.role))