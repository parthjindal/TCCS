from flask.blueprints import Blueprint
from flask import render_template, flash, url_for
from flask_login import current_user, login_required
from werkzeug.utils import redirect
from werkzeug.urls import url_parse
from app.models import Consignment, BranchOffice, Truck, Office

main = Blueprint("main", import_name=__name__, template_folder="templates")


@main.route('/')
def about():
    '''
        The function displays the About page of the website to the user
    '''
    return render_template("about.html", title="TL;DR"), 200


@main.route('/home')
@login_required
def home():
    '''
        The function displays the Home page of the website to the user
    '''
    return render_template(f"{current_user.role}.html", title='TL;DR'), 200


@main.route('/branches')
@login_required
def branches():
    '''
        If the user is the manager, this function allows him to view the records of all the branches
        Else the access is forbidden and error 403 is displayed
    '''
    if current_user.role == "manager":
        branches = Office.query.all()
        return render_template('branches.html', data=branches), 200

    return render_template('errors/403.html'), 403


@main.route('/branches/<token>')
@login_required
def branch(token):
    '''
        If the user is an employee, access is denied to him and error 403 is displayed
        Else the user is redirected to a page where all the records of the office, 
                with the given token as id, are displayed
        ....

        Parameters:
            token: int
                stores the id of the branch which is enquired

    '''
    if current_user.role == "manager":
        branch = Office.query.filter_by(id=token).first()
        return render_template('branch.html', name= branch.address.city, trck=branch.trucks, consign=branch.consignments), 200
    # flash('You are not authorized to access this page', 'warning')
    # return redirect(url_for('main.home', role=current_user.role), code=302)
    return render_template('errors/403.html'), 403
