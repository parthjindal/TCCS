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
    DELIVERED = 2
    ALLOTED = 3


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
        status: Enum(ConsignmentStatus)
            represents the current status of the consignment i.e. whether pending, enroute, delivered or alloted
        placetime: datetime
            the time at which the consignment was placed
        arrivaltime: datetime
            the time at which the consignment arrived
        charge: int
            the charge of transporting the consignment
        senderAddress: Address
            address of the sender of the consignment
        receiverAddress: Address
            address of the receiver of the consignment
        senderID: int
            unique id of the sender address
        receiverID: int
            unique id of the receiver address
        srcBranchID: int
            id of the office where the consignment was placed
        dstBranchID: int
            id of the destination office of the consignment
        trucks: Truck
            list of the trucks on which the consignment was loaded
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
        pass

    def __repr__(self) -> str:
        """
            The function to get the string representation of the consignment
            ....

            Returns:
                str: A string which stores the representation of the consignment
        """
        return f'<Consignment: {self.id}, Volume:{self.volume}, status: {self.status}>'
