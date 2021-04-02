from app.models import address, consignment
from app.models import Address, Bill
from app.models import Employee, Manager
from app.models import Consignment
from app.models import Office, BranchOffice, HeadOffice
from app.models import Truck, TruckStatus
import unittest

def test_branch_office():
    """
        
    """
    addr = Address(city = "Delhi", addrLine = "TCCS Branch Town", zipCode = "110009")
    addr1 = Address(city = "Delhi", addrLine = "C-28,Model Town-3", zipCode = "110009")
    addr2 = Address(city = "Mumbai", addrLine = "H-Block", zipCode = "100120")
    t1 = Truck(plateNo = "01TK0421", branchId = "1", status = TruckStatus.AVAILABLE, volumeConsumed = 0)
    t2 = Truck(plateNo = "01TK0422", branchId = "1", status = TruckStatus.AVAILABLE, volumeConsumed = 0)
    consign = Consignment(volume = 500, senderAddress = addr1, receiverAddress = addr2, dstBranchId = "2")
    bOffice = BranchOffice(name = "B1", address = addr, type = "Branch")
    bOffice.addConsignment(consign)
    bOffice.addTruck(t1)
    bOffice.addTruck(t2)
    tl = [t1, t2]
    cl = [consign]
    assert "B1" == bOffice.name
    assert addr == bOffice.address
    assert "Branch" == bOffice.type
    assert all([a == b for a, b in zip(tl, bOffice.trucks)])
    assert all([a == b for a, b in zip(cl, bOffice.consignments)])

# def test_head_office():
#     """

#     """
#     hOffice = HeadOffice()