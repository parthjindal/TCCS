from .address import Address
from enum import Enum
from app import db
from datetime import datetime

join_table = db.Table(
    'join_table', db.Model.metadata, db.Column(
        'consignmentID', db.Integer, db.ForeignKey('consignment.id')),
    db.Column('truckID', db.Integer, db.ForeignKey('truck.id')))


class ConsignmentStatus(Enum):
    PENDING = 0
    ENROUTE = 1
    ALLOTED = 2
    DELIVERED = 3


class Consignment(db.Model):
    """
        A class for representing a consignment
        ....

        Attributes
        ----------
        volume: int
            volume of the consignment

        volumeLeft: int
            volume of the consignment that has yet not been assigned to a truck

        senderAddress: Address
            address of the sender of the consignment

        receiverAddress: Address
            address of the receiver of the consignment

        srcBranchID: int
            id of the office where the consignment was placed

        dstBranchID: int
            id of the destination office of the consignment

        trucks: Truck
            list of the trucks on which the consignment was loaded

        Member Functions
        ----------------
        getInvoice(): dict

        __repr__(): str
            returns the string representation of an object of the class

    """
    ####################################### ORM ##############################################
    __tablename__ = "consignment"

    id = db.Column(db.Integer, primary_key=True)

    volume = db.Column(db.Integer, index=True)
    volumeLeft = db.Column(db.Integer, index=True)
    status = db.Column(db.Enum(ConsignmentStatus), index=True)

    placetime = db.Column(db.DateTime)
    arrivaltime = db.Column(db.DateTime)

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

    billID = db.Column(db.Integer, db.ForeignKey('bill.id'))
    bill = db.relationship(
        'Bill', uselist=False, foreign_keys=billID)

    trucks = db.relationship(
        "Truck", secondary=join_table, back_populates="consignments")

    ############################################################################################
    def __init__(self, **kwargs) -> None:
        '''
            The constructor of the consignment class
            ....

            Parameters:
                volume: int 
                    volume of the consignment
                senderAddress: Address
                    address of the sender of the consignment
                receiverAddress: Address
                    address of the receiver of the consignment
                srcBranchID: int
                    id of the office where the consignment was placed
                dstBranchID: int
                    id of the destination office of the consignment

        '''

        super().__init__(**kwargs)
        self.status = ConsignmentStatus.PENDING
        self.volumeLeft = self.volume
        self.charge = 0  # FIXME
        self.placetime = datetime.now()

    def getInvoice(self) -> dict:
        res = {
            "volume": self.volume,
            "placetime": self.placetime,
            "charge": self.charge,
            "sender": {
                "city": self.senderAddress.city,
                "address": self.senderAddress.addrLine,
                "zipCode": self.senderAddress.zipCode
            },
            "receiver": {
                "city": self.receiverAddress.city,
                "address": self.receiverAddress.addrLine,
                "zipCode": self.receiverAddress.zipCode
            }
        }

        return res

    def __repr__(self) -> str:
        """
            The function to get the string representation of the consignment
            ....

            Returns:
                str
        """
        return f'<Consignment: {self.id}, Volume:{self.volume}, status: {self.status}>'
