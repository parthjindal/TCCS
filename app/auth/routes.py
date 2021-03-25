from .forms import LoginForm
from flask.helpers import url_for
from app.auth import auth
from flask_login.utils import logout_user
from flask import redirect, url_for, flash
from flask_login import current_user
from app.models import Employee
from flask_login import login_user
from flask import request, render_template
from werkzeug.urls import url_parse
from app import login

login.login_view = "auth.login"

@auth.route("/")
def index():
    return redirect(url_for("auth.login"))
    
@auth.route("/login", methods=['GET', 'POST'])
def login():
    # Redirect to HOME page if logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home',role = current_user.role))

    form = LoginForm()
    if form.validate_on_submit():
        # if form valid
        user = Employee.query.filter_by(email=form.email.data).first()
        # check user and password
        if user is None or not user.check_password(form.password.data):
            flash(f"Login requested for user{form.email.data}")
            return redirect(url_for('main.index'))  # redirect to INDEX page

        #Log in user
        login_user(user, remember=form.remember.data)
        # next page if coming from another page
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.home',role = user.role)  # else HOME page

        # redirect to next_page
        return redirect(next_page)

    # render template
    return render_template('auth/login.html', title='Sign In', form=form)


@auth.route('/logout')
# logout user
def logout():
    logout_user()
    return redirect(url_for('main.index'))  # Redirect to Index page
