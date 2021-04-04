from .employee import Employee
from app import db
from abc import ABC, abstractmethod
from .truck import Truck, TruckStatus
from .consignment import ConsignmentStatus


class Office(db.Model):
    """
        A class to represent an office
        ....

        Attributes
        ----------
        address: Address
            addresss of the office
        addressID: int
            unique id of the adress
        employees: list of Employee class objects
            list of the employees working in the office
        consignments: list of Consignment class objects
            list of the consignments placed in the office
        trucks: list of Truck class objects
            list of the trucks assigned to the office
        

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
            The constructor of the Office class
            ....
            
            Pararmeters:
                address: Address
                    address of the office

        """
        super().__init__(**kwargs)

    def isBranch(self) -> bool:
        """
            The function to check if an office is a branch office or head office
            ....

            Returns:
                bool:
                    returns true if the office is a branch office and false in case of a head office

        """
        pass

    def addTruck(self, truck) -> None:
        """
            The function to add a truck to the office in case it hasn't been assigned to any other office or is not already present in the office and is available
            ....

            Parameters:
                truck: Truck
                    the truck to be added to the office

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
            The function to receive a truck and its consignments
            ....

            Parameters:
                truck: Truck
                    the truck to be received in case the office is its destination branch
            
            Returns:
                consignments: list of Consignment class objects
                    the consignments which were assigned to the truck
                

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
        """
            The function to get the string representation of the office
            ....

            Returns:
                str: A string which stores the representation of the office
        """
        return f'<Office, Address: {self.address}>'


class BranchOffice(Office):
    '''
        A class inherited from Office class to represent a branch office
        ....
        
        Attributes
        ----------
        Same as that of the Office class

    '''
    __tablename__ = 'branch'
    id = db.Column(db.Integer, db.ForeignKey('office.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'branch',
    }

    def __init__(self, **kwargs) -> None:
        """
            The constructor of the BranchOffice class
            ....
            
            Pararmeters:
                address: Address
                    address of the branch office

        """
        super().__init__(**kwargs)

    def isBranch(self) -> bool:
        '''
            The function to check if the office is a branch office
            ....

            Returns:
                True: bool
                    bool value True is always returned because the object is of the type BranchOffice
        '''
        return True

    def __repr__(self):
        """
            The function to get the string representation of the branch office
            ....

            Returns:
                str: A string which stores the representation of the branch office
        """
        return f'<Branch Office, {self.name}, Address: {self.address}>'


class HeadOffice(Office):
    '''
        A class inherited from Office class to represent the head office
        ....
        
        Attributes
        ----------
        Same as that of the Office class

    '''
    __tablename__ = 'head'
    id = db.Column(db.Integer, db.ForeignKey('office.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'head',
    }

    def __init__(self, **kwargs) -> None:
        """
            The constructor of the HeadOffice class
            ....
            
            Pararmeters:
                address: Address
                    address of the head office

        """
        super().__init__(**kwargs)

    def isBranch(self) -> bool:
        '''
            The function to check if the office is a branch office
            ....

            Returns:
                False: bool
                    bool value False is always returned because the object is of the type HeadOffice and not BranchOffice
        '''
        return False

    def __repr__(self):
        """
            The function to get the string representation of the head office
            ....

            Returns:
                str: A string which stores the representation of the head office
        """
        return f'<Head Office, {self.name}, Address: {self.address}>'
