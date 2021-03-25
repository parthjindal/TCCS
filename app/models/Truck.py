from TruckStatus import TruckStatus
from Consignment import Consignment
from app import db

class Truck(db.Model):
    truckID = db.Column(db.Integer, primary_key=True)
    currentBranch = db.Column(db.String(64), index=True)
    status = db.Column(db.Integer, index=True)
    volumeConsumed = db.Column(db.Integer, index=True)
    usageTime = db.Column(db.Integer, index=True)
    idleTime = db.Column(db.Integer, index=True)
    consignments = db.relationship("Consignment", secondary=Consignment.join_table, back_populates="trucks")

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
    
    def __repr__(self) -> str:
        return f'< ID: {self.truckID} Current Branch: {self.currentBranch} Status: {TruckStatus(self.status)} \
            Volume Consumed: {self.volumeConsumed} Usage Time: {self.usageTime} Idle Time: {self.idleTime}>'

    def getTruckID(self):
        return self.truckID
    def getCurrentBranch(self):
        return self.currentBranch
    def getStatus(self):
        return self.status
    def getVolumeConsumed(self):
        return self.volumeConsumed
    def getUsageTime(self):
        return self.usageTime
    def getIdleTime(self):
        return self.idleTime
    
    def viewConsignments(self):
        return self.consignments
    
    def setCurrentBranch(self, e):
        self.currentBranch = e
    def setStatus(self, e):
        self.status = e
    
    def updateVolumeConsumed(self, a):
        self.volumeConsumed += a
    def updateUsageTime(self, t):
        self.usageTime += t
    def getIdleTime(self, t):
        self.idleTime += t
    
    def addConsignments(self, e):
        self.consignments.append(e)
    
    def emptyTruck(self):
        consignments =  self.consignments
        self.truckID = None
        self.currentBranch = None
        self.status = None
        self.volumeConsumed = None
        self.usageTime = None
        self.idleTime = None
        self.consignments = []
        return consignments