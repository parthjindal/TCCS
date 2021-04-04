from .employee import Employee
from app import db
from abc import ABC, abstractmethod
from .truck import Truck, TruckStatus
from .consignment import ConsignmentStatus, Consignment
from app.interface import Interface
from .bill import Bill


class Office(db.Model):
    """
        A class to represent an office
        ....

        Attributes
        ----------

        address: Address
            addresss of the office

        employees: list of Employee class objects
            list of the employees working in the office

        consignments: list of Consignment class objects
            list of the consignments placed in the office

        trucks: list of Truck class objects
            list of the trucks assigned to the office

        Member Functions
        ----------------
        isBranch(): bool
            the function to check if the office is a branch office or not

        addTruck(truck: Truck):
            the function to assign a truck to the office

        recieveTruck(truck: Truck): list
            the function to recieve a truck and its consignment if the office is the
                    destination branch of the truck

        __repr__(): str
            returns the string representation of an object of the class

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

    transactions = db.relationship(
        "Bill", foreign_keys='Bill.branchID', uselist=True, lazy=False)

    __mapper_args__ = {
        'polymorphic_identity': 'office',
        'polymorphic_on': type
    }

  ############################################################################

    rate = 5

    def __init__(self, **kwargs):
        """
            The constructor of the Office class called automatically whenever an object of the
                    Office class is created
            ....

            Pararmeters:
                address: Address
                    address of the office

        """
        super().__init__(**kwargs)

    def isBranch(self):
        """
            The function to check if an office is a branch office or head office
            ....

            Returns:
                bool
        """
        pass

    def addTruck(self, truck) -> None:
        """
            The function to add a truck to the office if it satisfies the following conditions:
                a. it hasn't been assigned to any other office
                b. is not already present in the office
                c. its current status is AVAILABLE
            else the function raises a suitable error whenever any of the given conditions are not satisfied
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

    def dispatchTruck(self, truck: Truck) -> None:
        '''
        '''
        truck.dispatch()
        for consign in truck.consignments:

            consign.fare = Interface.computeBill(consign, rate=self.rate)
            bill = Bill(amount=consign.fare, invoice=consign.getInvoice())

            self.transactions.add(bill)

    def addConsignment(self, consign) -> None:
        """
        """
        if consign.srcBranchID is not None:
            raise AttributeError("Consignment already added to some Branch")

        if consign in self.consignments:
            raise Exception("Consignment already added")

        self.consignments.append(consign)

    @staticmethod
    def allotTruck(branch):
        """
        """
        def compare(obj):
            if isinstance(obj, Truck):
                return obj.volumeLeft
            if isinstance(obj, Consignment):
                return obj.placetime
            else:
                raise TypeError("Unknown Type")

        consigns = [x for x in branch.consignments if x.status.name == "PENDING"]
        consigns.sort(reverse=True, key=compare)

        trucks_ = [x for x in branch.trucks if x.status.name == "AVAILABLE"]
        trucks_.sort(reverse=True, key=compare)

        for consign in consigns:
            for truck in trucks_:
                try:
                    truck.addConsignment(consign)
                except:
                    pass
                if consign.status.name == "ALLOTED":
                    break
        return

    def receiveTruck(self, truck) -> list:
        """
            The function to receive a truck and its consignments if all the following conditions are satisfed:
                a. the destination branchID of the truck matches with the id of the office
                b. current status of the truck is ENROUTE
                The function changes empties the truck and changes the status of all the consignments 
                            that were alloted to the truck to DELIVERED
            If the above conditions are not satisfied, the function raises a suitable error
            ....

            Parameters:
                truck: Truck
                    the truck to be received

            Returns:
                consignments: list of Consignment class objects


        """
        if truck.dstBranchID != self.id:
            return ValueError("Truck id mismatch")

        if truck.status != TruckStatus.ENROUTE:
            return AttributeError("Truck not enroute")

        consignments = truck.empty()
        self.addTruck(truck)

        for consignment in consignments:
            consignment.status = ConsignmentStatus.DELIVERED

        return consignments

    def __repr__(self) -> str:
        """
            The function to get the string representation of the Office class object
            ....

            Returns:
                str
        """
        return f'<Office, Address: {self.address}>'


class BranchOffice(Office):
    '''
        A class inherited from Office class to represent a branch office
        ....

        Attributes
        ----------
        All the atrributes of this class are same as Office class

        Member Functions
        ----------------
        All the member functions of this class are same as Office class

    '''
    __tablename__ = 'branch'
    id = db.Column(db.Integer, db.ForeignKey('office.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'branch',
    }

    def __init__(self, **kwargs) -> None:
        """
            The constructor of the BranchOffice class called automatically whenever an object of the 
                        BranchOffice class is created
            ....

            Pararmeters:
                address: Address
                    address of the branch office

        """
        super().__init__(**kwargs)

    def isBranch(self) -> bool:
        '''
            The function to check if the office is a branch office, thus always returns True
            ....

            Returns:
                True
        '''
        return True

    def __repr__(self):
        """
            The function to get the string representation of the branch office
            ....

            Returns:
                str
        """
        return f'<Branch Office, {self.name}, Address: {self.address}>'


class HeadOffice(Office):
    '''
        A class inherited from Office class to represent the head office
        ....

        Attributes
        ----------
        All the atrributes of this class are same as Office class

        Member Functions
        ----------------
        All the member functions of this class are same as Office class

    '''
    __tablename__ = 'head'
    id = db.Column(db.Integer, db.ForeignKey('office.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'head',
    }

    def __init__(self, **kwargs) -> None:
        """
            The constructor of the HeadOffice class called automatically whenever an object of the 
                        HeadOffice class is created
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
                False
        '''
        return False

    def __repr__(self):
        """
            The function to get the string representation of the head office
            ....

            Returns:
                str
        """
        return f'<Head Office, {self.name}, Address: {self.address}>'
