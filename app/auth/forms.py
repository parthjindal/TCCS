from app.models.office import BranchOffice
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import Employee, Manager

# Login form
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

# Employee Registration form
class RegistrationForm(FlaskForm):
    '''
    '''
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    branchID = StringField('Branch ID', validators=[DataRequired()])
    submit = SubmitField('Register')
    
    def validate_email(self, email):
        user = Employee.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
    
    def validate_branchID(self, branchID):
        branchIDs = BranchOffice.query.filter_by(id=branchID.data).first()
        if branchIDs is None:
            raise ValidationError('Please use correct Branch ID.')

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
