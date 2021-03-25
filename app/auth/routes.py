from .forms import LoginForm
from flask.helpers import url_for
from app.auth import auth
from flask_login.utils import logout_user
from flask import redirect, url_for, flash
from flask_login import current_user
from .forms import RegistrationForm
from app.models import User
from app import db
from flask_login import login_user
from flask import request,render_template
from werkzeug.urls import url_parse


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(f"Login requested for user{form.username.data}")
            return redirect(url_for('main.index'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.home')
        return redirect(next_page)
    # if form.validate_on_submit():
    return render_template('auth/login.html', title='Sign In', form=form )


# @auth.route("/register", methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for("main.home"))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = User(username=form.username.data, email=form.email.data)
#         user.set_password(form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         # flash

from app import login
login.login_view = "auth.login"


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))