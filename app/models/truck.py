from enum import Enum
from .consignment import join_table
from app import db


class TruckStatus(Enum):
    AVAILABLE = 0
    Assigned = 1
    Enroute = 2


class Truck(db.Model):
    __tablename__ = "truck"
    id = db.Column(db.Integer, primary_key=True)
    plateNo = db.Column(db.String(16))
    branchId = db.Column(db.String(64), db.ForeignKey("office.id"), index=True)
    status = db.Column(db.Integer, index=True)
    volumeConsumed = db.Column(db.Integer, index=True)
    usageTime = db.Column(db.Integer, index=True)
    idleTime = db.Column(db.Integer, index=True)

    consignments = db.relationship(
        "Consignment", secondary=join_table, back_populates="trucks")

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return f'< ID: {self.id} Current Branch: {self.branchId} Status: {TruckStatus(self.status)}' \
            f'Volume Consumed: {self.volumeConsumed} Usage Time: {self.usageTime} Idle Time: {self.idleTime}>'

############################### TODO ########################################
    # def getTruckID(self):
    #     return self.id
    # def getCurrentBranch(self):
    #     return self.currentBranch
    # def getStatus(self):
    #     return self.status
    # def getVolumeConsumed(self):
    #     return self.volumeConsumed
    # def getUsageTime(self):
    #     return self.usageTime
    # def getIdleTime(self):
    #     return self.idleTime

    # def viewConsignments(self):
    #     return self.consignments

    # def setCurrentBranch(self, e):
    #     self.currentBranch = e
    # def setStatus(self, e):
    #     self.status = e

    # def updateVolumeConsumed(self, a):
    #     self.volumeConsumed += a
    # def updateUsageTime(self, t):
    #     self.usageTime += t
    # def getIdleTime(self, t):
    #     self.idleTime += t

    # def addConsignments(self, e):
    #     self.consignments.append(e)

    # def emptyTruck(self):
    #     consignments =  self.consignments
    #     # self.id = None
    #     self.currentBranch = None
    #     self.status = None
    #     self.volumeConsumed = None
    #     self.usageTime = None
    #     self.idleTime = None
    #     self.consignments = []
    #     return consignments
