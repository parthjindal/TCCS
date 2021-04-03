from app.models import Truck, TruckStatus
from app import db

def test_truck():
    """
    """
    truck = Truck(volume=500,plateNo = "DL-09-0768",branchID = 1)
    assert truck.volume == 500
    assert truck.plateNo == "DL-09-0768"
    assert truck.branchID == 1
    assert truck.volumeLeft == 500
    assert truck.usageTime == 0
    assert truck.idleTime == 0


