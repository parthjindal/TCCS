from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, NumberRange, Optional
from app.models import Address, Office


class AddressForm(FlaskForm):
    city = StringField("City", validators=[
                       DataRequired()], filters=[lambda x:x.title()])
    addrLine = StringField("Address Line", validators=[
                           DataRequired(), Length(max=60)])

    def validate_zip(self, field):
        try:
            int(zipCode)
        except:
            raise ValidationError(message="Enter Numerical Digits only")

    zipCode = StringField("Zip Code", validators=[
                          DataRequired(), Length(min=6, max=6), validate_zip])


class ConsignmentForm(FlaskForm):
    volume = IntegerField("Volume", validators=[DataRequired(), Length(min=1)])
    destinationBranch = SelectField("Branch", coerce=int)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.destinationBranch.choices = [
            (x.id, x.name) for x in Office.query.order_by("name")]
        self.senderAddress = AddressForm()
        self.receiverAddress = AddressForm()

    def validate_on_submit(self):
        return (super().validate_on_submit())*(self.senderAddress.validate_on_submit()) *\
            (self.receiverAddress.validate_on_submit())
