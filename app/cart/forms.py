from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField,SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, NumberRange, Optional
from app.models import Address,Office


class ConsignmentForm(FlaskForm):
    volume = IntegerField("Volume", validators=[DataRequired(), Length(min=1)])
    sendAddrLine = StringField("Sender Address Line", validators=[
                               DataRequired(), Length(min = 0)])
    sendAddrCity = StringField("sendAddrCity", validators=[DataRequired()])
    sendAddrzipCode = IntegerField("sendZip", validators=[Optional(), NumberRange(
        min=6, max=6, message="zip-code should have only 6 no.s")])
    destAddrLine = StringField("destAddrLine", validators=[
                               DataRequired(), Length(min= 0)])
    destAddrCity = StringField("destAddrCity", validators=[DataRequired()])
    destAddrzipCode = IntegerField("destZip", validators=[Optional(), NumberRange(
        min=6, max=6, message="zip-code should have only 6 no.s")])
    destinationBranch = SelectField("Branch",coerce=int)

