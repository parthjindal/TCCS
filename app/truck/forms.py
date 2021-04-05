from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError
from app.models import Office,Truck


class TruckForm(FlaskForm):
    '''

    '''
    plateNo = StringField("Plate No.", validators=[DataRequired()])
    branch = SelectField("Branch", coerce=int)
    submit = SubmitField("Create")

    def validate_plateNo(self, field):
        t = Truck.query.filter_by(plateNo=field.data).first()
        if t is not None:
            raise ValidationError('Truck already registered.')

    def __init__(self, **kwargs):
        '''
        '''
        super().__init__(**kwargs)
        self.branch.choices = [(x.id, f'{x.address.city} Office')
                               for x in Office.query.order_by("id")]


class ReceiveTruckForm(FlaskForm):
    '''

    '''
    plateNo = SelectField("Plate No.", coerce=int)
    submit = SubmitField("Receive")

    def __init__(self, branchID, **kwargs):
        '''
        '''
        super().__init__(**kwargs)
        self.branchID = branchID
        self.plateNo.choices = [(x.id, f'{x.plateNo}')
                               for x in Truck.query.filter_by(dstBranchID=self.branchID) if x.status.name=="ENROUTE"]
