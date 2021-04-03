from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Required, Email, EqualTo, ValidationError, Length, NumberRange, Optional
from app.models import Address, Office


class ConsignmentForm(FlaskForm):
    volume = IntegerField("Volume")
    destinationBranch = SelectField("Branch", coerce=int)

    senderCity = StringField("City", validators=[DataRequired()])
    senderAddrLine = StringField("Address Line", validators=[
                                 DataRequired(), Length(max=60)])
    senderZipCode = StringField("Zip Code", validators=[
                                DataRequired(), Length(min=6, max=6)])
    receiverCity = StringField("City", validators=[DataRequired()])
    receiverAddrLine = StringField("Address Line", validators=[
                                   DataRequired(), Length(max=60)])
    receiverZipCode = StringField("Zip Code", validators=[
                                  DataRequired(), Length(min=6, max=6)])
    submit = SubmitField("Create")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # print("somewhers")
        self.destinationBranch.choices = [
            (x.id, x.name) for x in Office.query.order_by("name")]
        print([x.id, x.name] for x in Office.query.order_by("name"))


class TruckForm(FlaskForm):
    plateNo = StringField("Plate No.",validators=[DataRequired()])
    