from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from app.models import Office,Truck


class TruckForm(FlaskForm):
    '''

    '''
    plateNo = StringField("Plate No.", validators=[DataRequired()])
    branch = SelectField("Branch", coerce=int)
    submit = SubmitField("Create")

    def __init__(self, **kwargs):
        '''
        '''
        super().__init__(**kwargs)
        self.branch.choices = [(x.id, f'{x.address.city} Office')
                               for x in Office.query.order_by("id")]


class ReceiveTruckForm(FlaskForm):
    '''

    '''
    plateNo = StringField("Plate No.", validators=[DataRequired()])
    submit = SubmitField("Create")

    def __init__(self, branchID, **kwargs):
        '''
        '''
        super().__init__(**kwargs)
        self.branchID = branchID
