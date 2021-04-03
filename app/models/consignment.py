from app.models.address import Address
from enum import Enum
from app import db
import json
from json import JSONEncoder
from flask import jsonify


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
    # volume-left-to-be-assigned
    volumeLeft = db.Column(db.Integer, index=True)
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
        self.status = ConsignmentStatus.PENDING
        self.volumeLeft = self.volume
        

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
        dict_ = {
            "id": self.id,
            "volume": self.volume,
            "status": ConsignmentStatus(self.status).name,
            "senderAddress": str(self.senderAddress),
            "receiverAddress": str(self.receiverAddress),
            "sourceBranch": self.srcBranchId,
            "destinationBranch": self.dstBranchId
        }
        return json.dumps(dict_)
