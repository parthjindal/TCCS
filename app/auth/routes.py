from app.auth import auth
from .forms import LoginForm, RegistrationForm, ManagerRegistrationForm, RequestResetForm, ResetPasswordForm
from flask_login import logout_user
from flask import redirect, url_for, flash, request, render_template, abort, current_app
from flask_login import current_user, login_user, login_required
from app.models import Employee, Manager, Office
from werkzeug.urls import url_parse
from flask_mail import Message
from app import login, db, mail


login.login_view = "auth.login"


@auth.route("/")
def index():
    '''

    '''
    return redirect(url_for("auth.login"))


@auth.route("/login", methods=['GET', 'POST'])
def login():
    '''

    '''
    if current_user.is_authenticated:
        return redirect(url_for('main.home', role=current_user.role))

    form = LoginForm()
    if form.validate_on_submit():

        user = Employee.query.filter_by(email=form.email.data).first()

        if user is None or not user.check_password(form.password.data):
            flash(f"Invalid Email/Password", category='warning')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember.data)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.home', role=user.role)
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@auth.route('/logout')
@login_required
def logout():
    '''

    '''
    logout_user()
    return redirect(url_for('main.about'))


@auth.route("/register", methods=['GET', 'POST'])
@login_required
def register():
    '''

    '''
    if current_user.role == "employee":
        flash("Access Denied")
        return redirect(url_for('main.home'), code=302)

    form = RegistrationForm()
    if form.validate_on_submit():

        user = Employee(name=form.name.data, email=form.email.data, branchID=form.branch.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('Employee added')
        return redirect(url_for('main.home'))

    return render_template('register.html', title='Register', form=form)


@auth.route("/register/manager", methods=['GET', 'POST'])
def registerManager():
    '''

    '''
    if current_user.is_authenticated:
        flash("Access Denied")
        return redirect(url_for('main.home', role=current_user.role))

    manager = Employee.query.filter_by(role='manager').first()
    if manager is not None:
        return render_template('noMan.html')

    form = ManagerRegistrationForm()
    if form.validate_on_submit():

        headOffice = Office.query.filter_by(type="head").first()
        manager = Manager(name=form.name.data, email=form.email.data, branchID=headOffice.id)
        manager.set_password(form.password.data)

        db.session.add(manager)
        db.session.commit()

        flash('Manager account created!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('regMan.html', title='Register', form=form)


def send_reset_email(user: Employee):
    '''

    '''
    token = user.get_reset_token(expires_sec=300)

    msg = Message('Password Reset Request',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[user.email],
                  body=render_template("resetPassword.txt", user=user, token=token))

    mail.send(msg)


@auth.route("/reset-password", methods=['GET', 'POST'])
def reset_request():
    '''

    '''
    if current_user.is_authenticated:
        flash("Already Logged in, Logout to reset password", category='info')
        return redirect(url_for('main.home'))

    form = RequestResetForm()
    if form.validate_on_submit():

        user = Employee.query.filter_by(email=form.email.data).first()
        send_reset_email(user)

        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('auth.login'), code=302)

    return render_template('reset_request.html', title='Reset Password', form=form)


@auth.route("/reset-password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    '''

    '''
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    employee = Employee.verify_reset_token(token)

    if employee is None:
        flash('Invalid/Expired Token', 'warning')
        return redirect(url_for('reset_request'), code=302)

    form = ResetPasswordForm()
    if form.validate_on_submit():

        employee.set_password(form.password.data)
        db.session.commit()

        flash('Password Updated!', 'success')
        return redirect(url_for('auth.login'), code=302)

    return render_template('reset_token.html', title='Reset Password', form=form)
