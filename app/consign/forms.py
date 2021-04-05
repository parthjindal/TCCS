from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, NumberRange, Optional
from app.models import Address, Office


class ConsignmentForm(FlaskForm):
    '''

    '''
    volume = IntegerField("Volume", validators=[DataRequired(), NumberRange(min=1,max =500)])

    sAddrLine = StringField("Address Line", validators=[DataRequired(), Length(max=60)])
    sCity = StringField("City", validators=[DataRequired()])
    sZipCode = StringField("Zip Code", validators=[DataRequired(), Length(min=6, max=6)])

    rAddrLine = StringField("Address Line", validators=[DataRequired(), Length(max=60)])
    rCity = StringField("City", validators=[DataRequired()])
    rZipCode = StringField("Zip Code", validators=[DataRequired(), Length(min=6, max=6)])

    branch = SelectField("Branch", coerce=int)

    submit = SubmitField("Create")

    def __init__(self,branchID,**kwargs):
        '''

        '''
        super().__init__(**kwargs)
        self.branch.choices = [(x.id, f'{x.address.city} Office')
                               for x in Office.query.order_by("id") if x.id != branchID]

    def validate_rZipCode(self, field):
        '''

        '''
        try:
            int(field.data)
        except ValueError:
            raise ValidationError("All field-chars must be between 0-9")

    def validate_sZipCode(self, field):
        '''

        '''
        try:
            int(field.data)
        except ValueError:
            raise ValidationError("All field-chars must be between 0-9")
