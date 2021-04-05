from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, NumberRange


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Sign In")


class ChangeRate(FlaskForm):
    rate = FloatField("New Rate", validators=[DataRequired(), NumberRange(min=0.1)])
    submit = SubmitField("Submit")
