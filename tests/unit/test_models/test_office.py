from app.models import address, consignment
from app.models import Address, Bill
from app.models import Employee, Manager
from app.models import Consignment
from app.models import Office, BranchOffice, HeadOffice
from app.models import Truck, TruckStatus
import unittest

def test_branch_office(test_client, database):
    """
        
    """
    addr = Address(city = "Delhi", addrLine = "TCCS Branch Town", zipCode = "110009")
    addr1 = Address(city = "Delhi", addrLine = "C-28,Model Town-3", zipCode = "110009")
    addr2 = Address(city = "Mumbai", addrLine = "H-Block", zipCode = "100120")
    t1 = Truck(plateNo = "01TK0421")
    t2 = Truck(plateNo = "01TK0422")
    bOffice = BranchOffice(address = addr)
    consign1 = Consignment(volume = 300, senderAddress = addr1, receiverAddress = addr2, srcBranchID = bOffice.id)
    t2.addConsignment(consign1)
    bOffice.addTruck(t1)
    bOffice.addTruck(t2)
    employee = Employee(name = "Shristi",  email = "shristi21singh@gmail.com")
    employee1 = Employee(name = "Parth", email = "pmjindal2344@gmail.com")
    bOffice.addEmployee(employee)
    bOffice.addEmployee(employee1)
    database.session.add(bOffice)
    database.session.commit()
    bOffice1 = BranchOffice.query.filter_by(address = addr).first()

    t3 = Truck.query.filter_by(plateNo = "01TK0421").first()
    t4 = Truck.query.filter_by(plateNo = "01TK0422").first()
    e1 = Employee.query.filter_by(email = "pmjindal2344@gmail.com").first()
    e2 = Employee.query.filter_by(email = "shristi21singh@gmail.com").first()

    assert addr == bOffice1.address
    assert "branch" == bOffice1.type
    assert bOffice1.isBranch() == True

    assert t3.branchID == bOffice1.id
    assert t4.branchID == bOffice1.id
    assert e1.branchID == bOffice1.id
    assert e2.branchID == bOffice1.id

    # for i in bOffice1.consignments:
    #     print (i)

    f = False

    for i in bOffice1.consignments:
        if (i == consign1):
            f = True

    assert f == True

    f1 = False
    f2 = False
    f3 = False
    f4 = False


    for i in bOffice1.trucks:
        if (i == t3):
            f1 = True
        
        if (i == t4):
            f2 = True

    assert (f1 == True)
    assert (f2 == True)

    for i in bOffice1.employees:
        if (i == e1):
            f3 = True
        
        if (i == e2):
            f4 = True

    assert (f3 == True)
    assert (f4 == True)

def test_head_office(test_client, database):
    """
        
    """
    
    addr = Address(city = "Mumbai", addrLine = "H-Block", zipCode = "100120")
    addr1 = Address(city = "Mumbai", addrLine = "H-Block", zipCode = "100120")
    addr2 = Address(city = "Delhi", addrLine = "C-28,Model Town-3", zipCode = "110009")
    t1 = Truck(plateNo = "01TK0421")
    t2 = Truck(plateNo = "01TK0422")
    hOffice = HeadOffice(address = addr)
    manager = Manager(name = "Mayank", email = "mayankkumar1205@gmail.com", headOffice = hOffice.id)
    hOffice.manager = manager
    hOffice.addTruck(t1)
    hOffice.addTruck(t2)

    employee = Employee(name = "Shristi",  email = "shristi21singh@gmail.com")
    employee1 = Employee(name = "Parth", email = "pmjindal2344@gmail.com")
    hOffice.addEmployee(employee)
    hOffice.addEmployee(employee1)
    database.session.add(hOffice)
    database.session.commit()
    hOffice1 = HeadOffice.query.filter_by(address = addr).first()

    t3 = Truck.query.filter_by(plateNo = "01TK0421").first()
    t4 = Truck.query.filter_by(plateNo = "01TK0422").first()
    e1 = Employee.query.filter_by(email = "pmjindal2344@gmail.com").first()
    e2 = Employee.query.filter_by(email = "shristi21singh@gmail.com").first()

    assert addr == hOffice1.address
    assert manager == hOffice1.manager
    assert "head" == hOffice1.type
    assert hOffice1.isBranch() == False

    assert t3.branchID == hOffice1.id
    assert t4.branchID == hOffice1.id
    assert e1.branchID == hOffice1.id
    assert e2.branchID == hOffice1.id
    assert manager.headOffice == hOffice1.id

    f1 = False
    f2 = False
    f3 = False
    f4 = False


    for i in hOffice1.trucks:
        if (i == t3):
            f1 = True
        
        if (i == t4):
            f2 = True

    assert (f1 == True)
    assert (f2 == True)

    for i in hOffice1.employees:
        if (i == e1):
            f3 = True
        
        if (i == e2):
            f4 = True

    assert (f3 == True)
    assert (f4 == True)