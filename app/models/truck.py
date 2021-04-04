from enum import Enum
from .consignment import ConsignmentStatus, join_table, Consignment
from app import db
from datetime import datetime


class TruckStatus(Enum):
    AVAILABLE = 0
    ASSIGNED = 1
    ENROUTE = 2


class Truck(db.Model):
    """
        A class to represent a truck
        ....

        Attributes
        ----------
        plateNo: string
            plate number of the truck

        branchID: int
            id of the office to which the truck has been assigned

        dstBranchID: int
            id of the destination office of the truck

        volumeLeft: float
            volume left in the truck
        
        consignments: list of Consignment class objects
            list of the consignments that have been assigned to the truck
        
        Member Functions
        ----------------
        empty(): list
            the function to empty the truck and return the list of consignments that were assigned to it

        dispatchTruck():
            the function to dispatch the truck

        addConsignment(consignment: Consignment):
            the function to add a new consignment to the truck

        __repr__(): str
            returns the string representation of an object of the class

        

    """
    ############################## ORM ########################################
    __tablename__ = "truck"
    id = db.Column(db.Integer, primary_key=True)            # id
    plateNo = db.Column(db.String(16))                      # plateNo

    branchID = db.Column(                                   # branchID
        db.Integer, db.ForeignKey("office.id"), index=True)
    dstBranchID = db.Column(                                # dstBranchID
        db.Integer, db.ForeignKey("office.id"), index=True)

    status = db.Column(db.Enum(TruckStatus), index=True)    # truck-status

    volume = db.Column(db.Float)        # volume-init
    volumeLeft = db.Column(db.Float)    # volume-left

    departureTime = db.Column(db.DateTime)  # departure time

    usageTime = db.Column(db.Float)
    idleTime = db.Column(db.Float)

    consignments = db.relationship(
        "Consignment", secondary=join_table, back_populates="trucks")

    ##########################################################################

    def __init__(self, volume=500, **kwargs) -> None:
        """
            The constructor for the Truck class
            ....

            Parameters:
                volume: float
                    volume of the truck, default value is 500
                plateNo: string
                    plate number of the truck
                branchID: int
                    id of the office to which the truck has been assigned
                dstBranchID: int
                    id of the destination office of the truck

        """
        super().__init__(**kwargs)
        self.volume = volume
        self.volumeLeft = self.volume
        self.status = TruckStatus.AVAILABLE
        self.usageTime = 0
        self.idleTime = 0

    def empty(self) -> list:
        """
            The function to empty the truck and return the list of consignments assigned to it
            ....

            Returns:
                consignments: list of Consignment class objects

        """
        consignments = self.consignments

        self.volumeLeft = self.volume
        self.status = TruckStatus.AVAILABLE
        self.branchID = None
        ######################################### TODO ##############################
        # update usage time/idletime
        #############################################################################

        self.dstBranchID = None
        self.consignments = []

        for consignment in consignments:
            if self in consignment.trucks:
                consignment.trucks.remove(self)

        return consignments

    def dispatch(self) -> None:
        """
            The function to dispatch the truck and make neccessary changes to the truck and its consignments

        """
        self.status = TruckStatus.ENROUTE
        self.departureTime = datetime.now()
        for consignment in self.consignments:
            consignment.status = "ENROUTE"

    def addConsignment(self, consignment: Consignment) -> None:
        """
            The function to assign a consignment to the truck if all the following conditions are satisfied
                a. The source branches and the destination branches(in case of a truck with ASSIGNED status) 
                            of the consignment and the truck are equal
                b. There is enough volume left in the truck
                c. Truck status is not ENROUTE
            Else raise a suitable error
            ....

            Parameters:
                consignment: Consignment
                    consignment to be added to the truck

        """
        if self.branchID != consignment.srcBranchID:
            raise AttributeError("Source Branch not same")

        if self.volumeLeft - consignment.volume < 0:
            raise ValueError("Consignment too large")

        if self.status == TruckStatus.ENROUTE:
            raise AttributeError("Status mismatch,Truck Enroute")

        if self.status == TruckStatus.AVAILABLE:

            self.status == TruckStatus.ASSIGNED
            self.dstBranchID = consignment.dstBranchID
            self.consignments.append(consignment)
            consignment.trucks.append(self)
            self.volumeLeft -= consignment.volume
            consignment.volume = 0

        elif self.status == TruckStatus.ASSIGNED:

            if self.dstBranchID != consignment.dstBranchID:
                raise AttributeError("Destination mismatch")

            self.consignments.append(consignment)
            consignment.trucks.append(self)
            self.volumeLeft -= consignment.volume
            consignment.volume = 0

    def __repr__(self) -> str:
        """
            The function to get the string representation of the truck
            ....

            Returns:
                str
        """
        return f'<Truck:{self.plateNo},id {self.id},Volume:{self.volume}, Status:{self.status.name}>'
