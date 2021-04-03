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

    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
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
    __tablename__ = 'branchOffice'
    id = db.Column(db.Integer, db.ForeignKey('office.id'), primary_key=True)

    ## TODO ##

    __mapper_args__ = {
        'polymorphic_identity': 'branch',
    }

    def isBranch(self) -> bool:
        return True
    
    

class HeadOffice(Office):
    __tablename__ = 'headOffice'
    id = db.Column(db.Integer, db.ForeignKey('office.id'), primary_key=True)
    manager = db.relation("Manager", uselist=False, lazy=False)

    __mapper_args__ = {
        'polymorphic_identity': 'head',
    }

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def isBranch(self) -> bool:
        return False
