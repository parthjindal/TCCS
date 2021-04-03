from enum import Enum
from .consignment import ConsignmentStatus, join_table
from app import db


class TruckStatus(Enum):
    AVAILABLE = 0
    ASSIGNED = 1
    ENROUTE = 2


class Truck(db.Model):
    __tablename__ = "truck"
    id = db.Column(db.Integer, primary_key=True)
    plateNo = db.Column(db.String(16))
    branchId = db.Column(db.String(64), db.ForeignKey("office.id"), index=True)
    dstBranchId = db.Column(db.String(64), db.ForeignKey("office.id"), index=True)
    status = db.Column(db.Integer, index=True)
    volume = db.Column(db.Integer,index = True)
    volumeConsumed = db.Column(db.Integer, index=True)
    usageTime = db.Column(db.Integer, index=True)
    idleTime = db.Column(db.Integer, index=True)

    consignments = db.relationship(
        "Consignment", secondary=join_table, back_populates="trucks")

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.volumeConsumed = 0
        self.usageTime = 0
        self.idleTime = 0

    def __repr__(self) -> str:
        return f'< ID: {self.id} Current Branch: {self.branchId} Status: {TruckStatus(self.status)}' \
            f'Volume Consumed: {self.volumeConsumed} Usage Time: {self.usageTime} Idle Time: {self.idleTime}>'

    def updateVolumeConsumed(self, a):
        self.volumeConsumed += a

    def addConsignments(self, consign):
        if 
        if not len(self.consignments):
            self.dstBranchId = consign.dstBranchId
            self.status = TruckStatus.ASSIGNED
        if self.volumeConsumed < 500 and self.dstBranchId == consign.dstBranchId and consign.status == ConsignmentStatus.PENDING and \
           self.status != TruckStatus.ENROUTE:
            consign.trucks.append(self)
            self.consignments.appned(consign)
            if consign.volumeLeft > (500-self.volumeConsumed):
                consign.volumeLeft = consign.volumeLeft - (500-self.volumeConsumed)
                self.updateVolumeConsumed(500-self.volumeConsumed)
                consign.status = ConsignmentStatus.PENDING
            else:
                self.updateVolumeConsumed(consign.volumeLeft)
                consign.volumeLeft = 0
                consign.status = ConsignmentStatus.ALLOTED
        if self.volumeConsumed == 500:
            self.status = TruckStatus.ENROUTE
            if consign.volumeLeft == 0:
                consign.status = ConsignmentStatus.ENROUTE

    def emptyTruck(self):
        consignments =  self.consignments
        self.branchId = None
        self.dstBranchId = None
        self.status = TruckStatus.AVAILABLE
        self.volumeConsumed = 0
        # self.usageTime = None
        # self.idleTime = None
        self.consignments = []
        return consignments
