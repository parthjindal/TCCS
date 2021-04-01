from app.models.address import Address
from enum import Enum
from app import db


class ConsignmentStatus(Enum):
    PENDING = 0
    ENROUTE = 1
    DELIVERED = 2
    ALLOTED = 3


join_table = db.Table(
    'join_table', db.Model.metadata, db.Column(
        'consignmentID', db.Integer, db.ForeignKey('consignment.id')),
    db.Column('truckID', db.Integer, db.ForeignKey('truck.id')))


class Consignment(db.Model):
    """
        A class representing a generic consignment
        ....

        Attributes
        ---------
        volume:  int
            consignment volume
        
    """
    __tablename__ = "consignment"

    id = db.Column(db.Integer, primary_key=True)    # consignment-id
    volume = db.Column(db.Integer, index=True)      # volume
    volumeLeft = db.Column(db.Integer,index = True) # volume-left-to-be-alloted
    status = db.Column(db.Integer, index=True)      # current-status
    charge = db.Column(db.Integer, index=True)
    
    #### SENDER ADDRESS #####
    sId = db.Column(db.Integer, db.ForeignKey('address.id'), 
                    nullable=False)                 
    senderAddress = db.relationship(
        'Address', uselist=False, foreign_keys=sId, lazy=False) 
    
    #### RECEIVER ADDRESS ####
    rId = db.Column(db.Integer, db.ForeignKey('address.id'),
                    nullable=False)
    receiverAddress = db.relationship(
        'Address', uselist=False, foreign_keys=rId, lazy=False)

    #### Source Branch ######
    srcBranchId = db.Column(
        db.String(64),
        db.ForeignKey("office.id"),
        index=True)

    #### Destination Branch #######
    dstBranchId = db.Column(
        db.String(64),
        db.ForeignKey("office.id"),
        index=True)

    #### trucks #####
    trucks = db.relationship(
        "Truck", secondary=join_table, back_populates="consignments")

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    
    def getStatus(self) -> ConsignmentStatus:
        return ConsignmentStatus(self.status)

    def getSourceBranch(self) -> int:
        return self.srcBranchId

    def getDestinationBranch(self) -> int:
        return self.dstBranchId 

    def getTruckIDs(self) -> list:
        return [x.id for x in self.trucks]

    def setStatus(self, status: ConsignmentStatus = ConsignmentStatus.PENDING):
        self.status = status.value()

    def setDestinationBranch(self, e):
        self.destinationBranch = e

    def __repr__(self) -> str:
        return f'< ID: {self.id} Volume: {self.volume} Status: {self.status} Sender Address: {self.senderAddress}' \
            f'Receiver Address: {self.receiverAddress} Status: {ConsignmentStatus(self.status)} Source Branch: {self.srcBranchId}' \
            f'Destination Branch: {self.dstBranchId} Charge: {self.charge}>'
