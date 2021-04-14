from enum import Enum
from .consignment import ConsignmentStatus, join_table, Consignment
from app import db
from datetime import datetime
import pytz
timezone = pytz.timezone("Asia/Kolkata")


class TruckStatus(Enum):
    AVAILABLE = 0
    ASSIGNED = 1
    READY = 2
    ENROUTE = 3


class Logger(db.Model):
    __tablename__ = "logger"
    id = db.Column(db.Integer, primary_key=True, index=True)
    value = db.Column(db.Float, index=True)
    time = db.Column(db.DateTime)
    branchID1 = db.Column(db.Integer, db.ForeignKey('truck.id'))
    branchID2 = db.Column(db.Integer, db.ForeignKey('truck.id'))
    branchID3 = db.Column(db.Integer, db.ForeignKey('office.id'))

    def __repr__(self):
        return f'<Value:{self.value}, Timestamp:{self.time.strftime("%d-%b-%Y, %H:%M") }>'


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
    # plateNo
    plateNo = db.Column(db.String(16), unique=True)

    branchID = db.Column(                                   # branchID
        db.Integer, db.ForeignKey("office.id"), index=True)
    dstBranchID = db.Column(                                # dstBranchID
        db.Integer, db.ForeignKey("office.id"), index=True)

    status = db.Column(db.Enum(TruckStatus), index=True)    # truck-status

    volume = db.Column(db.Integer)        # volume-init
    volumeLeft = db.Column(db.Integer)    # volume-left

    assignmentTime = db.Column(db.DateTime)  # departure time
    emptyTime = db.Column(db.DateTime)  # empty-time

    usage = db.relationship(
        'Logger', foreign_keys="Logger.branchID1", uselist=True)
    idle = db.relationship(
        'Logger', foreign_keys="Logger.branchID2", uselist=True)

    #####################
    # truck.usage -> list ->(value,)->x:float,y:time
    # truck.usage[0].value ->y
    # truck.usage[0].time->time

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
        self.emptyTime = timezone.localize(datetime.now())
        self.assignmentTime = timezone.localize(datetime.now())
        self.usage.append(
            Logger(value=0, time=timezone.localize(datetime.now())))
        self.idle.append(
            Logger(value=0, time=timezone.localize(datetime.now())))

    def empty(self) -> list:
        """
            The function to empty the truck and return the list of consignments assigned to it
            ....

            Returns:
                consignments: list of Consignment class objects

        """
        self.emptyTime = timezone.localize(datetime.now())
        self.updateUsageTime(self.assignmentTime, self.emptyTime)
        consignments = self.consignments

        self.volumeLeft = self.volume
        self.status = TruckStatus.AVAILABLE
        self.branchID = None
        self.dstBranchID = None
        self.consignments = []

        for consignment in consignments:
            if self in consignment.trucks:
                consignment.trucks.remove(self)

        return consignments

    def updateUsageTime(self, time1, time2):
        log = Logger(value=(time2.replace(
            tzinfo=None)-time1.replace(tzinfo=None)).total_seconds() / 3600, time=time2.astimezone(timezone))
        time2 = time2.astimezone(timezone)
        time1 = time1.astimezone(timezone)

        self.usage.append(log)
        if len(self.usage) > 10:
            self.usage.remove(0)

    def updateIdleTime(self, time1, time2):
        log = Logger(value=(time2.replace(
            tzinfo=None)-time1.replace(tzinfo=None)).total_seconds() / 3600, time=time2.astimezone(timezone))
        time2 = time2.astimezone(timezone)
        time1 = time1.astimezone(timezone)

        self.idle.append(log)
        if len(self.idle) > 10:
            self.idle.remove(0)

    def dispatch(self) -> None:
        """
            The function to dispatch the truck and make neccessary changes to the truck and its consignments

        """
        self.status = TruckStatus.ENROUTE
        for consignment in self.consignments:
            consignment.status = ConsignmentStatus.ENROUTE
            consignment.dispatchtime = timezone.localize(datetime.now())

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
        if self.volumeLeft < consignment.volume:
            raise ValueError("Too big of Consignment")

        if consignment.status != ConsignmentStatus.PENDING:
            return

        if self.branchID != consignment.srcBranchID:
            raise AttributeError("Source Branch not same")

        if self.status == TruckStatus.READY or self.status == TruckStatus.ENROUTE:
            raise ValueError("Truck full/enroute ")

        if self.status == TruckStatus.AVAILABLE:

            self.assignmentTime = timezone.localize(datetime.now())
            self.updateIdleTime(self.emptyTime, self.assignmentTime)

            self.status = TruckStatus.ASSIGNED
            self.dstBranchID = consignment.dstBranchID
            self.consignments.append(consignment)

            consignment.trucks.append(self)

            self.volumeLeft -= consignment.volume
            consignment.status = ConsignmentStatus.ALLOTED

            if self.volumeLeft == 0:
                self.status = TruckStatus.READY

        elif self.status == TruckStatus.ASSIGNED:

            if self.dstBranchID != consignment.dstBranchID:
                raise AttributeError("Destination mismatch")

            self.consignments.append(consignment)
            consignment.trucks.append(self)

            self.volumeLeft -= consignment.volume
            consignment.status = ConsignmentStatus.ALLOTED

            if self.volumeLeft == 0:
                self.status = TruckStatus.READY

    def __repr__(self) -> str:
        """
            The function to get the string representation of the truck
            ....

            Returns:
                str
        """
        return f'<Truck: {self.plateNo}, Id: {self.id}, Volume Left: {self.volumeLeft}, Status: {self.status.name}>'
