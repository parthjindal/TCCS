from app.models.consignment import Consignment
from app.models import employee
from app import db
from abc import ABC, abstractmethod


class Office(db.Model):
    '''

    '''
    __tablename__ = "office"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    adress_id = db.Column(db.Integer, db.ForeignKey('address.id'),
                          nullable=False)
    address = db.relationship('Address', uselist=False, lazy=False)
    type = db.Column(db.String(50))
    employees = db.relationship("Employee", uselist=True, lazy=False)

    consignments = db.relationship("Consignment",
                                   foreign_keys=Consignment.srcBranchId,
                                   uselist=True, lazy=False)
    trucks = db.relationship("Truck", uselist=True, lazy=False)

    __mapper_args__ = {
        'polymorphic_identity': 'office',
        'polymorphic_on': type
    }
    
    @abstractmethod
    def isBranch(self) -> bool:
        pass

    def __repr__(self) -> str:
        return f'<Office: {self.name}, Address: {self.address} ,Employees:{[x for x in self.employees]}>'


class BranchOffice(Office):
    __tablename__ = 'branch'
    id = db.Column(db.Integer, db.ForeignKey('office.id'), primary_key=True)

    ## TODO ##

    __mapper_args__ = {
        'polymorphic_identity': 'branch',
    }

    def isBranch(self) -> bool:
        return True


class HeadOffice(Office):
    __tablename__ = 'head'
    id = db.Column(db.Integer, db.ForeignKey('office.id'), primary_key=True)
    manager = db.relation("Manager", uselist=False, lazy=False)

    __mapper_args__ = {
        'polymorphic_identity': 'head',
    }

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def isBranch(self) -> bool:
        return False

    def __repr__(self) -> str:
        return super().__repr__()
