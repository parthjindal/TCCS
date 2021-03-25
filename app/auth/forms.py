from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email


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
