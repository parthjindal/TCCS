from enum import Enum
from .consignment import ConsignmentStatus,join_table, Consignment
from app import db
from datetime import datetime


class TruckStatus(Enum):
    AVAILABLE = 0
    ASSIGNED = 1
    ENROUTE = 2

class Truck(db.Model):
    """

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

        """
        super().__init__(**kwargs)
        self.volume = volume
        self.volumeLeft = self.volume
        self.status = TruckStatus.AVAILABLE
        self.usageTime = 0
        self.idleTime = 0

    def empty(self) -> list:
        """

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
            consignment.trucks.remove(self)

        return consignments

    
    def dispatch(self)->None:
        """

        """
        self.status = TruckStatus.ENROUTE
        self.departureTime = datetime.now()
        for consignment in self.consignments:
            consignment.status = "ENROUTE"


    def addConsignment(self, consignment: Consignment) -> None:
        """

        """
        if self.volumeLeft - consignment.volume < 0:
            raise ValueError("Consignment too large")

        if self.status == TruckStatus.ENROUTE:
            raise TypeError("Status mismatch,Truck Enroute")

        if self.status == TruckStatus.AVAILABLE:

            self.status == TruckStatus.ASSIGNED
            self.dstBranchID = consignment.dstBranchId
            self.consignments.append(consignment)
            self.volumeLeft -= consignment.volume
            
        elif self.status == TruckStatus.ASSIGNED:
            
            self.consignments.append(consignment)
            self.volumeLeft -= consignment.volume

    def __repr__(self) -> str:
        """

        """
        return f'Truck:{self.plateNo}'
