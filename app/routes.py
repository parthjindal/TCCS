from flask.blueprints import Blueprint
from flask import render_template, flash, url_for
from flask_login import current_user, login_required
from werkzeug.utils import redirect
from werkzeug.urls import url_parse
from app.models import Consignment, BranchOffice, Truck, Office

main = Blueprint("main", import_name=__name__, template_folder="templates")


@main.route('/')
def about():
    return render_template("about.html", title="TL;DR", code=200)


@main.route('/home')
@login_required
def home():
    return render_template(f"{current_user.role}.html", title='TL;DR', code=200)


# @main.route('/consignments')


@main.route('/branches')
@login_required
def branches():
    if current_user.role == "manager":
        branches = Office.query.all()
        return render_template('branches.html', data=branches, code=200)
    # flash('You are not authorized to access this page', 'warning')
    # return redirect(url_for('main.home', role=current_user.role), code=302)
    return render_template('errors/403.html', code=200)


@main.route('/branches/<token>')
@login_required
def branch(token):
    if current_user.role == "manager":
        branch = Office.query.filter_by(id=token).first()
        return render_template('branch.html', name=branch.name, trck=branch.trucks, consign=branch.consignments, code=200)
    # flash('You are not authorized to access this page', 'warning')
    # return redirect(url_for('main.home', role=current_user.role), code=302)
    return render_template('errors/403.html', code=200)