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
        The function to redirect the user to the login page location

    '''
    return redirect(url_for("auth.login"), code=302)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    '''
        This function is used by the user to login to the software
        If the credentials provided by the user are valid, he successfully logs in and
                    is redirected to the home page
        
        The user is redirected to the login page and asked to enter the data again in case
                    any of the credentials provided by him are invalid
        
        The user can also be directed to the next page, in case if it exists, if 
                    the user requests to do so once he is logged in
    '''
    if current_user.is_authenticated:
        return redirect(url_for('main.home', role=current_user.role), code=302)

    form = LoginForm()
    if form.validate_on_submit():

        user = Employee.query.filter_by(email=form.email.data).first()

        if user is None or not user.check_password(form.password.data):
            flash(f"Invalid Email/Password", category='warning')
            return redirect(url_for('auth.login'), code=302)

        login_user(user, remember=form.remember.data)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.home', role=user.role)
        return redirect(next_page, code=302)

    return render_template('login.html', title='Sign In', form=form), 200


@auth.route('/logout')
@login_required
def logout():
    '''
        This function is used by the user to log out from the software if he is currently logged in

        It redirects the user to the About page location
    '''
    logout_user()
    return redirect(url_for('main.about'), code=302)


@auth.route("/register", methods=['GET', 'POST'])
@login_required
def register():
    '''
        The function is used to register a new user

        Since only a manager can register a new user, access is denied whenever an employee tries to do so

        If the current user is the manager, the credentials of the new user are checked,
                    if the credentials are valid, an account for the new user is created else
                    the manager is asked to enter the credentials again
        The function redirects the user to the home page after successfully adding the new user to the database 
            
    '''
    if current_user.role == "employee":
        # flash("Access Denied")
        # return redirect(url_for('main.home'), code=302)
        return render_template('errors/403.html'), 403

    form = RegistrationForm()
    if form.validate_on_submit():

        user = Employee(name=form.name.data, email=form.email.data, branchID=form.branch.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('Employee added')
        return redirect(url_for('main.home'), code=302)

    return render_template('register.html', title='Register', form=form), 200


@auth.route("/register/manager", methods=['GET', 'POST'])
def registerManager():
    '''
        The function creates an account for the manager provided it does not exist already
        An employee cannot create an account for the Manager and accessed will be denied
                    if an employee tries to do so
        If the data submitted in the form are valid, account is created successfully and
                    the manager is directed to the login page
        In case of invalid credentials, the user needs to fill the form again
    '''
    if current_user.is_authenticated:
        # flash("Access Denied")
        # return redirect(url_for('main.home', role=current_user.role), code=302)
        return render_template('errors/403.html'), 403

    manager = Employee.query.filter_by(role='manager').first()
    if manager is not None:
        return render_template('noMan.html'), 200

    form = ManagerRegistrationForm()
    if form.validate_on_submit():

        headOffice = Office.query.filter_by(type="head").first()
        manager = Manager(name=form.name.data, email=form.email.data, branchID=headOffice.id)
        manager.set_password(form.password.data)

        db.session.add(manager)
        db.session.commit()

        flash('Manager account created!', 'success')
        return redirect(url_for('auth.login'), code=302)

    return render_template('regMan.html', title='Register', form=form), 200


def send_reset_email(user: Employee):
    '''
        This function is used to send an email to the users who wish to reset their password
        ....

        Parameters:
            user: Employee
                the user whose password needs to be reset
        ....

        A token is sent to the user via an email which is valid for a limited period of time 
                (for 300 sec, here)
        This token is used by the user to request the system for permission to reset his password

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
        This function allows the users to request to reset the password
        The user needs to be logged out in order to do so

        If the credentials of the form filled by the user to reset password are valid, 
                an email is sent to the user by calling the send_reset_email(user) function
                and the user is directed to the login page

        In case of inalid credentials, the user needs to fill the form again
        
    '''
    if current_user.is_authenticated:
        flash("Already Logged in, Logout to reset password", category='info')
        return redirect(url_for('main.home'), code=302)

    form = RequestResetForm()
    if form.validate_on_submit():

        user = Employee.query.filter_by(email=form.email.data).first()
        send_reset_email(user)

        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('auth.login'), code=302)

    return render_template('reset_request.html', title='Reset Password', form=form), 200


@auth.route("/reset-password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    '''
        The function verifies the token and finds out the user and then asks the user to reset his password
        ...

        Parameters:
            token: str
        ...

        In case the database is not able to find the user through the token or the token is expired,
                the user is again redirected to the reset_request page
        
        If the user is successfully identified in the database, he is asked to enter the new password
                and if the user is able to successfully change his password, he is directed to the login page
    '''
    if current_user.is_authenticated:
        return redirect(url_for('main.home'), code=302)

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

    return render_template('reset_token.html', title='Reset Password', form=form), 200
