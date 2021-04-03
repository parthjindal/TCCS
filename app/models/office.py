from .truck import Truck, TruckStatus
from .consignment import Consignment, ConsignmentStatus
from .employee import Employee
from app import db
from abc import ABC, abstractmethod


class Office(db.Model):
    """

    """
    ####################################### ORM ################################

    __tablename__ = "office"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(16))

    addressID = db.Column(db.Integer, db.ForeignKey('address.id'))
    address = db.relationship('Address', foreign_keys=addressID, uselist=False)

    employees = db.relationship("Employee", uselist=True, lazy=False)

    consignments = db.relationship(
        "Consignment", foreign_keys='consignment.id', uselist=True, lazy=False)
    trucks = db.relationship(
        "Truck", foreign_keys='truck.id', uselist=True, lazy=False)

    __mapper_args__ = {
        'polymorphic_identity': 'office',
        'polymorphic_on': type
    }

    ############################################################################

    def __init__(**kwargs):
        """

        """
        super().__init__(**kwargs)

    def isBranch(self) -> bool:
        """

        """
        pass

    def addTruck(self, truck: Truck) -> None:
        """

        """

        if truck.branchID != None:
            raise AttributeError("Truck Already assigned")

        if truck in self.trucks:
            raise ValueError("Office already contains truck")

        self.trucks.append(truck)
        truck.branchID = self.id

    def __repr__(self) -> str:
        return f'<Office: {self.name}, Address: {self.address}, Employees:{[x for x in self.employees]}>'


class BranchOffice(Office):
    __tablename__ = 'branch'
    id = db.Column(db.Integer, db.ForeignKey('office.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'branch',
    }

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

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
