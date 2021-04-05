from .employee import Employee
from app import db
from abc import ABC, abstractmethod
from .truck import Truck, TruckStatus
from .consignment import ConsignmentStatus, Consignment
from app.interface import Interface
from .bill import Bill
from datetime import datetime
from .truck import Logger
import pickle


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

    waitingtime = db.relationship(
        "Logger", foreign_keys="Logger.branchID3", uselist=True, lazy=False
    )

    __mapper_args__ = {
        'polymorphic_identity': 'office',
        'polymorphic_on': type
    }

  ############################################################################

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

    def getRevenue(self):
        amount = 0
        for bill in self.transactions:
            amount += bill.amount
        return amount

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
        value = 0
        for consign in truck.consignments:
            value += (consign.dispatchtime-consign.placetime).total_seconds() / 3600.0
        value /= len(truck.consignments)

        self.waitingtime.append(Logger(value=value, time=datetime.now()))
        if len(self.waitingtime) > 10:
            self.waitingtime.pop(0)

    def addConsignment(self, consign) -> None:
        """
        """
        if consign.srcBranchID is not None:
            raise AttributeError("Consignment already added to some Branch")

        if consign in self.consignments:
            raise Exception("Consignment already added")

        consign.charge = Interface.computeBill(consign, rate=Office.getRate())

        invoice = Office.prettyInvoice(consign.getInvoice())
        bill = Bill(amount=consign.charge, invoice=invoice)
        consign.bill = bill
        self.consignments.append(consign)
        billcopy = Bill(amount=consign.charge, invoice=invoice, branchID=self.id)
        self.transactions.append(billcopy)

    @staticmethod
    def getRate():
        with open("rate.pkl", 'rb') as inp:

            print()
            rate = pickle.load(inp)
        return rate["rate"]

    @staticmethod
    def setRate(rate):
        with open("rate.pkl", 'wb') as outp:
            pickle.dump({"rate": rate}, outp)

    @ staticmethod
    def prettyInvoice(invoice):

        res = f"""
Sender's Details
Name: {invoice["sender"]["name"]}
Address: {invoice["sender"]["address"]}, {invoice["sender"]["city"]}

Receiver's Details
Name: {invoice["receiver"]["name"]}
Receiver's Address: {invoice["receiver"]["address"]}, {invoice["receiver"]["city"]}

Volume: {invoice["volume"]}

Order Placement Time: {invoice["placetime"].strftime('%d-%b-%Y, %H:%M')}

Amount: \u20B9 {invoice["charge"]}
"""
        return res

    @ staticmethod
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

        consigns = [x for x in branch.consignments if x.status == ConsignmentStatus.PENDING]
        consigns.sort(key=compare)

        trucks_ = [x for x in branch.trucks if (
            x.status == TruckStatus.AVAILABLE or x.status == TruckStatus.ASSIGNED)]
        trucks_.sort(reverse=True, key=compare)

        for consign in consigns:
            for truck in trucks_:
                try:
                    truck.addConsignment(consign)
                except:
                    pass
                if consign.status == ConsignmentStatus.ALLOTED:
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
            consignment.arrivaltime = datetime.now()

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
        return f'<Branch Office, {self.id}, Address: {self.address}>'


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
        return f'<Head Office, {self.id}, Address: {self.address}>'
