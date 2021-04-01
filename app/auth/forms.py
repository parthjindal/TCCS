from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import Employee, Manager, Office, BranchOffice


class LoginForm(FlaskForm):
    '''
        Login Form for validation
        @parameters:
            email: string,required
            password: string,required
            remember: bool
            submit: bool
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
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    # branchID = StringField('Branch ID', validators=[DataRequired()])
    branch = SelectField("Branch", coerce=int, validate_choice=True)
    submit = SubmitField('Register')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.branch.choices = [(x.id, x.name)
                               for x in Office.query.order_by("name")]

    def validate_email(self, email):
        user = Employee.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class ManagerRegistrationForm(FlaskForm):
    '''
    '''
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = Employee.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
