from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import Employee, Manager, Office
from flask_login import login_user


class LoginForm(FlaskForm):
    '''

    '''
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    '''

    '''
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[
                              DataRequired(), EqualTo('password')])
    branch = SelectField("Branch", coerce=int)
    submit = SubmitField('Register')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.branch.choices = [(x.id, f'{x.address.city} Office')
                               for x in Office.query.order_by("id")]
    
    def validate_email(self, email):
        user = Employee.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email already in use')


class ManagerRegistrationForm(FlaskForm):
    '''

    '''
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = Employee.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class RequestResetForm(FlaskForm):
    '''

    '''
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = Employee.query.filter_by(email=self.email.data).first()
        if user is None:
            raise ValidationError(
                'Invalid Email,Employee not registered')


class ResetPasswordForm(FlaskForm):
    '''

    '''
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
