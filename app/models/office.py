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

    def addConsignment(self, consign):
        consign.volumeLeft = consign.volume
        consign.srcBranchId = self.id
        self.consignments.append(consign)
        consign.status = 0
        #db.session.commit()
        # for x in Office.trucks:
        #     if x.status==TruckStatus.AVAILABLE or x.dstBranchId==consign.dstBranchId:
        #         x.addConsignment(consign)
    
    def addTruck(self, truck):
        # print("I was called")
        truck.branchId = self.id
        truck.dstBranchId = None
        truck.status = 0
        truck.volumeConsumed = 0
        truck.consignments = []
        self.trucks.append(truck)
        #db.session.commit()
    
    def addEmployee(self, emp):
        emp.branchID = self.id
        self.employees.append(emp)

    def receiveTruck(self, truck):
        if truck.status==TruckStatus.ENROUTE and truck.dstBranchId==self.id:
            receivedConsignments = truck.emptyTruck()
            self.addTruck(truck)
            for i in receivedConsignments:
                i.status = 2
        for x in Office.consignments:
            if x.status==ConsignmentStatus.PENDING:
                truck.addConsignments(x)

    def __repr__(self) -> str:
        return f'<Office: {self.name}, Address: {self.address}, Employees:{[x for x in self.employees]}>'


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
