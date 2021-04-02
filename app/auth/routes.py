from .forms import LoginForm, RegistrationForm, ManagerRegistrationForm
from flask.helpers import url_for
from app.auth import auth
from flask_login.utils import logout_user
from flask import redirect, url_for, flash
from flask_login import current_user, login_user, login_required
from app.models import Employee, Manager
from flask import request, render_template
from werkzeug.urls import url_parse
from app import login
from app import db

login.login_view = "auth.login"


@auth.route("/")
def index():
    return redirect(url_for("auth.login"))


@auth.route("/login", methods=['GET', 'POST'])
def login():
    # Redirect to HOME page if logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home', role=current_user.role))

    form = LoginForm()
    if form.validate_on_submit():
        # if form valid
        user = Employee.query.filter_by(email=form.email.data).first()
        # check user and password
        if user is None or not user.check_password(form.password.data):
            flash(f"Invalid Email/Password{form.email.data}")
            return redirect(url_for('auth.login'))  # redirect to INDEX page
        #Log in user
        login_user(user, remember=form.remember.data)
        # next page if coming from another page
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.home', role=user.role)  # else HOME page
        # redirect to next_page
        return redirect(next_page)
    # render template
    return render_template('auth/login.html', title='Sign In', form=form)


@auth.route('/logout')
# logout user
def logout():
    logout_user()
    return redirect(url_for('main.index'))  # Redirect to Index page


@auth.route("/register", methods=['GET', 'POST'])
@login_required
def register():
    if current_user.is_authenticated and current_user.role == "employee":
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Employee(name=form.name.data,
                        email=form.email.data, branchID=form.branch.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account for this employee has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('auth/register.html', title='Register', form=form)


@auth.route("/register/manager", methods=['GET', 'POST'])
def registerManager():
    if current_user.is_authenticated:
        return redirect(url_for('main.home', role=current_user.role))
    managers = Employee.query.filter_by(role='manager').first()
    if managers is not None:
        return render_template('auth/noMan.html')
    form = ManagerRegistrationForm()
    if form.validate_on_submit():
        user = Manager(name=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Manager account has been created!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/regMan.html', title='Register', form=form)
