from app.models import address, consignment
from app.models import Address, Bill
from app.models import Employee, Manager
from app.models import Consignment, ConsignmentStatus
from app.models import Office, BranchOffice, HeadOffice
from app.models import Truck, TruckStatus
import unittest
from app.interface import Interface
import time


def test_allotment(test_client, database):
    a1 = Address(city="Delhi")
    a2 = Address(city="Mumbai")
    a3 = Address(city="Chennai")

    o1 = BranchOffice(address=a1)
    o2 = BranchOffice(address=a2)
    o3 = HeadOffice(address=a3)

    t1 = Truck(plateNo="AAAA", volume=200)
    t2 = Truck(plateNo="BBBB", volume=300)
    t3 = Truck(plateNo="CCCC", volume=800)

    database.session.add(o1)
    database.session.add(o2)
    database.session.add(o3)

    database.session.add(t1)
    database.session.add(t2)
    database.session.add(t3)

    database.session.commit()

    c1 = Consignment(volume=400, senderAddress=a1, receiverAddress=a2, dstBranchID=o2.id)
    c2 = Consignment(volume=300, senderAddress=a1, receiverAddress=a2, dstBranchID=o2.id)
    c3 = Consignment(volume=300, senderAddress=a1, receiverAddress=a2, dstBranchID=o2.id)

    o1.addTruck(t1)
    o1.addTruck(t2)
    o1.addTruck(t3)

    database.session.add(c1)
    database.session.add(c2)
    database.session.add(c3)

    database.session.commit()

    o1.addConsignment(c1)
    o1.addConsignment(c2)
    o1.addConsignment(c3)

    # for x in o1.transactions:
    #     database.session.add(x)

    # database.session.commit()
    Office.allotTruck(o1)

    database.session.commit()

    assert c1 in t3.consignments

    o1.dispatchTruck(t3)
    o1.dispatchTruck(t2)

    o2.receiveTruck(t3)

    for i in o1.consignments:
        print(i)
    database.session.commit()

    for i in o1.transactions:
        print(i.invoice)

    database.session.commit()

def test_branch_office(test_client, database):
    """

    """
    addr = Address(city="Delhi", addrLine="Egret Branch Town", zipCode="110009")
    addr1 = Address(city="Delhi", addrLine="C-28,Model Town-3", zipCode="110009")
    addr2 = Address(city="Mumbai", addrLine="H-Block", zipCode="100120")
    addr3 = Address(city="Kolkata", addrLine="H-Block", zipCode="101120")
    bOffice = BranchOffice(address=addr)
    bOffice1 = BranchOffice(address=addr3)
    database.session.add(bOffice)
    database.session.add(bOffice1)
    database.session.commit()

    t1 = Truck(plateNo="01TK0421")
    t2 = Truck(plateNo="01TK0422", dstBranchID=bOffice1.id)
    t3 = Truck(plateNo="01TK049", branchID=bOffice1.id)

    consign1 = Consignment(volume=300, senderAddress=addr1,
                           receiverAddress=addr2, dstBranchID=bOffice1.id)
    consign = Consignment(volume=300, senderAddress=addr1,
                          receiverAddress=addr2)
    
    database.session.add(consign)
    database.session.add(consign1)
    database.session.add(t1)
    database.session.add(t2)
    database.session.add(t3)
    database.session.commit()

    bOffice.addConsignment(consign1)
    database.session.commit()

    flag = False
    flag1 = False
    flag2 = False
    for i in bOffice.transactions:
        if(i.invoice == consign1.bill.invoice):
            flag = True
        if(i.amount == consign1.bill.amount):
            flag1 = True
        if(i.branchID == bOffice.id):
            flag2 = True
    assert flag == True and flag1 == True and flag2 == True

    bOffice1.addConsignment(consign)
    bOffice.addTruck(t1)
    bOffice.addTruck(t2)
    database.session.commit()
    
    t2.addConsignment(consign1)
    database.session.commit()
    
    #print (t2.dstBranchID)
    try:
        bOffice.addTruck(t3)
    except AttributeError:
        print("Truck has already been assigned to another office")

    try:
        bOffice1.addTruck(t3)
    except AttributeError:
        print("Truck already present in the Office")

    try:
        t1.addConsignment(consign1)
    except:
        print("Consignment already alloted to a truck")
    
    t3.addConsignment(consign)

    consign2 = Consignment(volume=300, senderAddress=addr2,
                           receiverAddress=addr1, dstBranchID=bOffice.id)
    consign3 = Consignment(volume=200, senderAddress=addr2,
                           receiverAddress=addr1, dstBranchID=bOffice.id)
    t5 = Truck(plateNo="01TK0424", dstBranchID=bOffice.id)

    bOffice1.addConsignment(consign2)
    bOffice1.addConsignment(consign3)
    bOffice1.addTruck(t5)
    
    t5.addConsignment(consign2)
    t5.addConsignment(consign3)
    database.session.add(t5)
    database.session.commit()

    employee = Employee(name="Shristi",  email="shristi21singh@gmail.com", branchID=bOffice.id)
    employee1 = Employee(name="Parth", email="pmjindal2344@gmail.com", branchID=bOffice.id)

    database.session.add(employee)
    database.session.add(employee1)
    database.session.commit()

    bOffice_ = BranchOffice.query.filter_by(address=addr).first()

    t3 = Truck.query.filter_by(plateNo="01TK0421").first()
    t4 = Truck.query.filter_by(plateNo="01TK0422").first()
    e1 = Employee.query.filter_by(email="pmjindal2344@gmail.com").first()
    e2 = Employee.query.filter_by(email="shristi21singh@gmail.com").first()

    assert addr == bOffice_.address
    assert "branch" == bOffice_.type
    assert bOffice_.isBranch() == True

    assert t3.branchID == bOffice_.id
    assert t4.branchID == bOffice_.id
    assert e1.branchID == bOffice_.id
    assert e2.branchID == bOffice_.id

    f = False

    for i in bOffice_.consignments:
        if (i == consign1):
            f = True

    assert f == True

    f1 = False
    f2 = False
    f3 = False
    f4 = False

    for i in bOffice_.trucks:
        if (i == t3):
            f1 = True

        if (i == t4):
            f2 = True

    assert (f1 == True)
    assert (f2 == True)

    for i in bOffice_.employees:
        if (i == e1):
            f3 = True

        if (i == e2):
            f4 = True

    assert (f3 == True)
    assert (f4 == True)

    f = False
    f1 = False
    lst = bOffice_.receiveTruck(t5)
    database.session.commit()

    try:
        for i in lst:
            if (i == consign2):
                f = True

            if (i == consign3):
                f1 = True

        assert f == True
        assert f1 == True
    except:
        print(lst)

    bOffice_.dispatchTruck(t5)
    database.session.commit()


    f = False

    bOffice.dispatchTruck(t2)
    database.session.commit()
    lst1 = bOffice1.receiveTruck(t2)
    database.session.commit()

    for i in lst1:
        if (i == consign1):
            f = True
    
    assert f == True

    consign4 = Consignment(volume=300, senderAddress=addr1,
                          receiverAddress=addr2)
    consign5 = Consignment(volume=300, senderAddress=addr1,
                          receiverAddress=addr2)
    
    database.session.add(consign4)
    database.session.add(consign5)
    database.session.commit()

    bOffice.addConsignment(consign4)
    bOffice.addConsignment(consign5)
    database.session.commit()

    Office.allotTruck(bOffice)
    database.session.commit()

    assert t1.volumeLeft == 200
    assert consign4.status == ConsignmentStatus.ALLOTED
    assert consign5.status == ConsignmentStatus.PENDING


def test_head_office(test_client, database):
    """

    """
    addr = Address(city="Mumbai", addrLine="H-Block", zipCode="100120")
    addr1 = Address(city="Mumbai", addrLine="H-Block", zipCode="100120")
    addr2 = Address(city="Delhi", addrLine="C-28,Model Town-3", zipCode="110009")
    addr3 = Address(city="Kolkata", addrLine="H-Block", zipCode="101120")
    hOffice = HeadOffice(address=addr)
    bOffice1 = BranchOffice(address=addr3)
    database.session.add(hOffice)
    database.session.add(bOffice1)
    database.session.commit()
    
    manager = Manager(name="Mayank", email="mayankkumar1205@gmail.com", branchID=hOffice.id) 
    t1 = Truck(plateNo="01TK0421")
    t2 = Truck(plateNo="01TK0422", dstBranchID=bOffice1.id)
    t3 = Truck(plateNo="01TK049", branchID=bOffice1.id)

    consign1 = Consignment(volume=300, senderAddress=addr1,
                           receiverAddress=addr2, dstBranchID=bOffice1.id)
    consign = Consignment(volume=300, senderAddress=addr1,
                          receiverAddress=addr2)
    
    database.session.add(manager)
    database.session.add(consign)
    database.session.add(consign1)
    database.session.add(t1)
    database.session.add(t2)
    database.session.add(t3)
    database.session.commit()

    hOffice.addConsignment(consign1)
    database.session.commit()

    flag = False
    flag1 = False
    flag2 = False
    for i in hOffice.transactions:
        if(i.invoice == consign1.bill.invoice):
            flag = True
        if(i.amount == consign1.bill.amount):
            flag1 = True
        if(i.branchID == hOffice.id):
            flag2 = True
    assert flag == True and flag1 == True and flag2 == True

    bOffice1.addConsignment(consign)
    hOffice.addTruck(t1)
    hOffice.addTruck(t2)
    database.session.commit()

    t2.addConsignment(consign1)
    database.session.commit()
    
    #print (t2.dstBranchID)
    try:
        hOffice.addTruck(t3)
    except AttributeError:
        print("Truck has already been assigned to another office")

    try:
        bOffice1.addTruck(t3)
    except AttributeError:
        print("Truck already present in the Office")

    try:
        t1.addConsignment(consign1)
    except:
        print (t1.branchID)
        print (consign1.srcBranchID)
    
    t3.addConsignment(consign)
    database.session.commit()

    consign2 = Consignment(volume=300, senderAddress=addr2,
                           receiverAddress=addr1, dstBranchID=hOffice.id)
    consign3 = Consignment(volume=200, senderAddress=addr2,
                           receiverAddress=addr1, dstBranchID=hOffice.id)
    t5 = Truck(plateNo="01TK0424", dstBranchID=hOffice.id)

    bOffice1.addConsignment(consign2)
    bOffice1.addConsignment(consign3)
    database.session.add(t5)
    database.session.commit()

    bOffice1.addTruck(t5)    
    database.session.commit()

    t5.addConsignment(consign2)
    t5.addConsignment(consign3)
    database.session.commit()

    employee = Employee(name="Shristi",  email="shristi21singh@gmail.com", branchID=hOffice.id)
    employee1 = Employee(name="Parth", email="pmjindal2344@gmail.com", branchID=hOffice.id)
    database.session.add(employee)
    database.session.add(employee1)
    database.session.commit()
    
    hOffice_ = HeadOffice.query.filter_by(address=addr).first()

    t3 = Truck.query.filter_by(plateNo="01TK0421").first()
    t4 = Truck.query.filter_by(plateNo="01TK0422").first()
    e1 = Employee.query.filter_by(email="pmjindal2344@gmail.com").first()
    e2 = Employee.query.filter_by(email="shristi21singh@gmail.com").first()

    assert addr == hOffice_.address
    assert "head" == hOffice_.type
    assert hOffice_.isBranch() == False
    assert manager.branchID == hOffice_.id

    assert t3.branchID == hOffice_.id
    assert t4.branchID == hOffice_.id
    assert e1.branchID == hOffice_.id
    assert e2.branchID == hOffice_.id

    f = False

    for i in hOffice_.consignments:
        if (i == consign1):
            f = True

    assert f == True

    f1 = False
    f2 = False
    f3 = False
    f4 = False

    for i in hOffice_.trucks:
        if (i == t3):
            f1 = True

        if (i == t4):
            f2 = True

    assert (f1 == True)
    assert (f2 == True)

    for i in hOffice_.employees:
        if (i == e1):
            f3 = True

        if (i == e2):
            f4 = True

    assert (f3 == True)
    assert (f4 == True)

    f = False
    f1 = False

    lst = hOffice_.receiveTruck(t5)
    database.session.add(t5)

    try:
        for i in lst:
            if (i == consign2):
                f = True

            if (i == consign3):
                f1 = True

        assert f == True
        assert f1 == True
    except:
        print(lst)

    hOffice_.dispatchTruck(t5)
    database.session.commit()

    consign4 = Consignment(volume=300, senderAddress=addr1,
                          receiverAddress=addr2)
    consign5 = Consignment(volume=300, senderAddress=addr1,
                          receiverAddress=addr2)
    
    database.session.add(consign4)
    database.session.add(consign5)
    database.session.commit()

    hOffice.addConsignment(consign4)
    hOffice.addConsignment(consign5)
    database.session.commit()

    Office.allotTruck(hOffice)
    database.session.add(t5)
    database.session.commit()

    assert t1.volumeLeft == 200
    assert consign4.status == ConsignmentStatus.ALLOTED
    assert consign5.status == ConsignmentStatus.PENDING





