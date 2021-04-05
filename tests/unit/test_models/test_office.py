from app.models import address, consignment
from app.models import Address, Bill
from app.models import Employee, Manager
from app.models import Consignment
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

    Office.allotTruck(o1)

    database.session.commit()

    assert c1 in t3.consignments

    o1.dispatchTruck(t3)
    o1.dispatchTruck(t2)

    time.sleep(10)

    o2.receiveTruck(t3)

    for i in o1.consignments:
        print(i)

    database.session.commit()

    for i in o1.transactions:
        print(i.invoice)

# def test_branch_office(test_client, database):
#     """

#     """
#     addr = Address(city="Delhi", addrLine="TCCS Branch Town", zipCode="110009")
#     addr1 = Address(city="Delhi", addrLine="C-28,Model Town-3", zipCode="110009")
#     addr2 = Address(city="Mumbai", addrLine="H-Block", zipCode="100120")
#     addr3 = Address(city="Kolkata", addrLine="H-Block", zipCode="101120")
#     bOffice = BranchOffice(address=addr)
#     bOffice1 = BranchOffice(address=addr3)
#     database.session.add(bOffice)
#     database.session.add(bOffice1)
#     database.session.commit()

#     t1 = Truck(plateNo="01TK0421")
#     t2 = Truck(plateNo="01TK0422")
#     t3 = Truck(plateNo="01TK049", branchID=bOffice1.id)

#     consign1 = Consignment(volume=300, senderAddress=addr1,
#                            receiverAddress=addr2, srcBranchID=bOffice.id)
#     t2.addConsignment(consign1)
#     consign = Consignment(volume=300, senderAddress=addr1,
#                           receiverAddress=addr2, srcBranchID=bOffice1.id)
#     # t1.addConsignment(consign)
#     bOffice.addTruck(t1)
#     bOffice.addTruck(t2)
#     try:
#         bOffice.addTruck(t3)
#     except AttributeError:
#         print("Truck has already been assigned to another office")

#     try:
#         bOffice1.addTruck(t3)
#     except AttributeError:
#         print("Truck already present in the Office")

#     consign2 = Consignment(volume=300, senderAddress=addr2,
#                            receiverAddress=addr1, dstBranchID=bOffice.id)
#     consign3 = Consignment(volume=200, senderAddress=addr2,
#                            receiverAddress=addr1, dstBranchID=bOffice.id)
#     t5 = Truck(plateNo="01TK0424", dstBranchID=bOffice.id)
#     t5.addConsignment(consign2)
#     t5.addConsignment(consign3)
#     bOffice1.addTruck(t5)
#     # database.session.add(t5)

#     employee = Employee(name="Shristi",  email="shristi21singh@gmail.com", branchID=bOffice.id)
#     employee1 = Employee(name="Parth", email="pmjindal2344@gmail.com", branchID=bOffice.id)
#     database.session.add(employee)
#     database.session.add(employee1)

#     database.session.commit()
#     bOffice_ = BranchOffice.query.filter_by(address=addr).first()

#     t3 = Truck.query.filter_by(plateNo="01TK0421").first()
#     t4 = Truck.query.filter_by(plateNo="01TK0422").first()
#     e1 = Employee.query.filter_by(email="pmjindal2344@gmail.com").first()
#     e2 = Employee.query.filter_by(email="shristi21singh@gmail.com").first()

#     assert addr == bOffice_.address
#     assert "branch" == bOffice_.type
#     assert bOffice_.isBranch() == True

#     assert t3.branchID == bOffice_.id
#     assert t4.branchID == bOffice_.id
#     assert e1.branchID == bOffice_.id
#     assert e2.branchID == bOffice_.id

#     f = False

#     for i in bOffice_.consignments:
#         if (i == consign1):
#             f = True

#     assert f == True

#     f1 = False
#     f2 = False
#     f3 = False
#     f4 = False

#     for i in bOffice_.trucks:
#         if (i == t3):
#             f1 = True

#         if (i == t4):
#             f2 = True

#     assert (f1 == True)
#     assert (f2 == True)

#     for i in bOffice_.employees:
#         if (i == e1):
#             f3 = True

#         if (i == e2):
#             f4 = True

#     assert (f3 == True)
#     assert (f4 == True)

#     f = False
#     f1 = False
#     lst = bOffice_.receiveTruck(t5)

#     try:
#         for i in lst:
#             if (i == consign2):
#                 f = True

#             if (i == consign3):
#                 f1 = True

#         assert f == True
#         assert f1 == True
#     except:
#         print(lst)

#     # t5.status = TruckStatus.ENROUTE
#     # database.session.commit()
#     # lst = bOffice_.receiveTruck(t5)
#     # for i in lst:
# #         if (i == consign2):
# #             f = True

# #         if (i == consign3):
# #             f1 = True

#     # assert f == True
#     # assert f1 == True

#     # assert t5.branchID == bOffice_.id

#     f = False
#     lst1 = bOffice_.receiveTruck(t2)
#     try:
#         for i in lst:
#             if (i == consign1):
#                 f = True

#         assert f == True
#     except:
#         print(lst)


# def test_head_office(test_client, database):
#     """

#     """

#     addr = Address(city="Mumbai", addrLine="H-Block", zipCode="100120")
#     addr1 = Address(city="Mumbai", addrLine="H-Block", zipCode="100120")
#     addr2 = Address(city="Delhi", addrLine="C-28,Model Town-3", zipCode="110009")
#     addr3 = Address(city="Kolkata", addrLine="H-Block", zipCode="101120")
#     bOffice1 = BranchOffice(address=addr3)
#     hOffice = HeadOffice(address=addr)
#     database.session.add(bOffice1)
#     database.session.add(hOffice)
#     database.session.commit()

#     t1 = Truck(plateNo="01TK0421")
#     t2 = Truck(plateNo="01TK0422")
#     t3 = Truck(plateNo="01TK049", branchID=bOffice1.id)

#     consign1 = Consignment(volume=300, senderAddress=addr1,
#                            receiverAddress=addr2, srcBranchID=hOffice.id)
#     t2.addConsignment(consign1)
#     manager = Manager(name="Mayank", email="mayankkumar1205@gmail.com", branchID=hOffice.id)
#     #hOffice.manager = manager
#     hOffice.addTruck(t1)
#     hOffice.addTruck(t2)
#     try:
#         hOffice.addTruck(t3)
#     except AttributeError:
#         print("Truck has already been assigned to another office")

#     try:
#         bOffice1.addTruck(t3)
#     except AttributeError:
#         print("Truck already present in the Office")

#     consign2 = Consignment(volume=300, senderAddress=addr2,
#                            receiverAddress=addr1, dstBranchID=hOffice.id)
#     consign3 = Consignment(volume=200, senderAddress=addr2,
#                            receiverAddress=addr1, dstBranchID=hOffice.id)
#     t5 = Truck(plateNo="01TK0424", dstBranchID=hOffice.id)
#     t5.addConsignment(consign2)
#     t5.addConsignment(consign3)

#     t6 = Truck(plateNo="01TK0433")
#     bOffice1.addTruck(t6)
#     database.session.add(bOffice1)
#     database.session.commit()

#     t6.addConsignment(consign1)

#     try:
#         assert t6.branchID == consign1.srcBranchID
#     except AssertionError:
#         print("The source branches of the consignment and the truck are different\n")

#     try:
#         assert t6.branchID == hOffice.id
#     except AssertionError:
#         print("The source branches of the truck is not the Head Office\n")

#     employee = Employee(name="Shristi",  email="shristi21singh1@gmail.com", branchID=hOffice.id)
#     employee1 = Employee(name="Parth", email="pmjindal23441@gmail.com", branchID=hOffice.id)
#     database.session.add(employee)
#     database.session.add(employee1)

#     database.session.commit()
#     hOffice1 = HeadOffice.query.filter_by(address=addr).first()

#     t3 = Truck.query.filter_by(plateNo="01TK0421").first()
#     t4 = Truck.query.filter_by(plateNo="01TK0422").first()
#     e1 = Employee.query.filter_by(email="pmjindal23441@gmail.com").first()
#     e2 = Employee.query.filter_by(email="shristi21singh1@gmail.com").first()

#     assert addr == hOffice1.address
#     #assert manager == hOffice1.manager
#     assert "head" == hOffice1.type
#     assert hOffice1.isBranch() == False

#     assert t3.branchID == hOffice1.id
#     assert t4.branchID == hOffice1.id
#     assert e1.branchID == hOffice1.id
#     assert e2.branchID == hOffice1.id
#     assert manager.branchID == hOffice1.id
#     assert t5.dstBranchID == hOffice1.id

#     f = False

#     for i in hOffice1.consignments:
#         if (i == consign1):
#             f = True

#     assert f == True

#     f1 = False
#     f2 = False
#     f3 = False
#     f4 = False

#     for i in hOffice1.trucks:
#         if (i == t3):
#             f1 = True

#         if (i == t4):
#             f2 = True

#     assert (f1 == True)
#     assert (f2 == True)

#     for i in hOffice1.employees:
#         if (i == e1):
#             f3 = True

#         if (i == e2):
#             f4 = True

#     assert (f3 == True)
#     assert (f4 == True)

#     f = False
#     f1 = False
#     lst = hOffice1.receiveTruck(t5)

#     try:
#         for i in lst:
#             if (i == consign2):
#                 f = True

#             if (i == consign3):
#                 f1 = True

#         assert f == True
#         assert f1 == True
#     except:
#         print(lst)

#     f = False
#     lst1 = hOffice1.receiveTruck(t2)
#     try:
#         for i in lst:
#             if (i == consign1):
#                 f = True

#         assert f == True
#     except:
#         print(lst)
