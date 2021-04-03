from .address import Address
from enum import Enum
from app import db
from app.interface import getCharge

join_table = db.Table(
    'join_table', db.Model.metadata, db.Column(
        'consignmentID', db.Integer, db.ForeignKey('consignment.id')),
    db.Column('truckID', db.Integer, db.ForeignKey('truck.id')))


class ConsignmentStatus(Enum):
    PENDING = 0
    ENROUTE = 1
    DELIVERED = 2
    ALLOTED = 3


class Consignment(db.Model):
    """
    """

    ####################################### ORM ##############################################
    __tablename__ = "consignment"

    id = db.Column(db.Integer, primary_key=True)

    volume = db.Column(db.Integer, index=True)
    volumeLeft = db.Column(db.Integer, index=True)
    status = db.Column(db.Enum(ConsignmentStatus), index=True)

    charge = db.Column(db.Integer, index=True)

    ######################################## TODO ###########################################
    # invoice = db.relationship('Bill',uselist = False,lazy = False)

    senderID = db.Column(db.Integer, db.ForeignKey('address.id'))
    receiverID = db.Column(db.Integer, db.ForeignKey('address.id'))

    senderAddress = db.relationship(
        'Address', uselist=False, foreign_keys=senderID)
    receiverAddress = db.relationship(
        'Address', uselist=False, foreign_keys=receiverID)

    srcBranchID = db.Column(db.Integer, db.ForeignKey("office.id"), index=True)
    dstBranchID = db.Column(db.Integer, db.ForeignKey("office.id"), index=True)

    trucks = db.relationship(
        "Truck", secondary=join_table, back_populates="consignments")

    ############################################################################################
    def __init__(self, **kwargs) -> None:
        """

        """
        super().__init__(**kwargs)
        self.status = ConsignmentStatus.PENDING
        self.volumeLeft = self.volume
        self.charge = 0  # FIXME

    def getInvoice(self) -> dict:
        pass

    def __repr__(self) -> str:
        return f'<Consignment: {self.id}, Volume:{self.volume}, status: {self.status}>'
