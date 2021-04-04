from .employee import Employee
from app import db
from abc import ABC, abstractmethod
from .truck import Truck, TruckStatus
from .consignment import ConsignmentStatus


class Office(db.Model):
    """

    """
    ####################################### ORM ################################

    __tablename__ = "office"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(16))

    addressID = db.Column(db.Integer, db.ForeignKey('address.id'))
    address = db.relationship('Address', uselist=False)

    employees = db.relationship("Employee", uselist=True, lazy=False)

    consignments = db.relationship(
        "Consignment", foreign_keys='Consignment.srcBranchID', uselist=True, lazy=False)

    trucks = db.relationship(
        "Truck", foreign_keys='Truck.branchID', uselist=True, lazy=False)

    __mapper_args__ = {
        'polymorphic_identity': 'office',
        'polymorphic_on': type
    }

    ############################################################################

    def __init__(self, **kwargs):
        """

        """
        super().__init__(**kwargs)

    def isBranch(self) -> bool:
        """

        """
        pass

    def addTruck(self, truck) -> None:
        """

        """
        if truck.branchID != None:
            raise AttributeError("Truck Already assigned")

        if truck in self.trucks:
            raise ValueError("Office already contains truck")

        if truck.status != TruckStatus.AVAILABLE:
            raise AttributeError("Truck not available")

        self.trucks.append(truck)

    def receiveTruck(self, truck) -> list:
        """

        """
        if truck.dstBranchID != self.id:
            return ValueError("Truck id mismatch")

        if truck.status != TruckStatus.ENROUTE:
            return AttributeError("Truck not enroute")

        consignments = truck.empty()
        self.addTruck(truck)

        for consignment in consignments:
            if self in consignment.trucks:
                consignment.trucks.remove(self)
            consignment.status = ConsignmentStatus.DELIVERED

        return consignments

    def __repr__(self) -> str:
        return f'<Office, Address: {self.address}>'


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

    def __repr__(self):
        return f'<Branch Office, {self.name}, Address: {self.address}>'


class HeadOffice(Office):
    __tablename__ = 'head'
    id = db.Column(db.Integer, db.ForeignKey('office.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'head',
    }

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def isBranch(self) -> bool:
        return False

    def __repr__(self):
        return f'<Head Office, {self.name}, Address: {self.address}>'
