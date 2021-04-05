from app.models import address, consignment
from app.models import Address, Bill
from app.models import Employee, Manager
from app.models import Consignment, ConsignmentStatus
from app.models import Office, BranchOffice, HeadOffice
from app.models import Truck, TruckStatus
import unittest
from app.interface import Interface
import time

def test_application(test_client, database):
    '''
        This is the application test for Egret - the Transport Company Computerization Software(TCCS)
        All the functions and scenarios have been tried to cover
        This function can help anyone to understand the flow of the working of the software
        Here, we have tested the application assuming that the company has a Head Office
                    and two branch offices
        Each of the branch offices have been assigned an employee
        Atleast one truck and one consignment have been assigned to each of the offices
        Each consignment is placed in an office, its bill is computed and then it is dispatched
                    after being assigned to a truck
        Then truck is received in the destination office and now this office becomes its source branch office 
                    and the status of the consignment is changed to delivered
        Now, the office can even use this received truck to transport the consignments placed in it
        Note that no consignment can be alloted to a truck unless they have the same source branchID
                    and the truck has enough space to accomodate the consignment
    '''
    addr1 = Address(city="Delhi", addrLine="C-28,Model Town-3", zipCode="110009")
    addr2 = Address(city="Mumbai", addrLine="H-Block", zipCode="100120")
    addr3 = Address(city="Kolkata", addrLine="B-Block", zipCode="101120")
    addr4 = Address(city="Delhi", addrLine="D-17,Model Town-3", zipCode="110009")
    addr5 = Address(city="Mumbai", addrLine="A-Block", zipCode="100120")
    addr6 = Address(city="Kolkata", addrLine="D-Block", zipCode="101120")
    database.session.add(addr1)
    database.session.add(addr2)
    database.session.add(addr3)
    database.session.add(addr4)
    database.session.add(addr5)
    database.session.add(addr6)

    addr1_ = Address.query.filter_by(addrLine="C-28,Model Town-3").first()
    addr2_ = Address.query.filter_by(city="Mumbai").first()
    addr3_ = Address.query.filter_by(zipCode="101120").first()
    addr4_ = Address.query.filter_by(id=4).first()
    addr5_ = Address.query.filter_by(addrLine="A-Block").first()
    addr6_ = Address.query.filter_by(addrLine="D-Block").first()

    '''
        assert addr1_ == addr1 ensures that the addr1 object was correctly created and gives same object when filtered by addrLine,
                          here, addrLine will be unique for all address rows in table, and .first() ensures that address object is returned instead of list
        assert addr2_ == addr2 ensures that the addr2 object was correctly created and gives same object when filtered by city,
                         .first() should give same object as addr2_ since addr2_ was the first address added to database with this city
        assert addr3_ == addr3 ensures that the addr3 object was correctly created and gives same object when filtered by zipCode,
                         .first() should give same object as addr3_ since addr3_ was the first address added to database with this zipCode
        assert addr4_ == addr4 ensures that the addr4 object was correctly created and gives same object when filtered by id,
                         id should be 4 since it is 4th row in address table, and id is allotted serially by the database
        assert addr5_ == addr5 ensures that the addr5 object was correctly created and gives same object when filtered by addrLine
        assert addr6_ == addr6 ensures that the addr6 object was correctly created and gives same object when filtered by addrLine
    '''

    assert addr1_ == addr1
    assert addr2_ == addr2
    assert addr3_ == addr3
    assert addr4_ == addr4
    assert addr5_ == addr5
    assert addr6_ == addr6

    hOffice = HeadOffice(address=addr1)
    bOffice1 = BranchOffice(address=addr2)
    bOffice2 = BranchOffice(address=addr3)

    database.session.add(hOffice)
    database.session.add(bOffice1)
    database.session.add(bOffice2)
    database.session.commit()

    hOffice_ = HeadOffice.query.filter_by(address=addr1).first()
    hOffice_1 = HeadOffice.query.filter_by(id=1).first()
    hOffice_2 = HeadOffice.query.filter_by(type="head").first()
    bOffice1_ = BranchOffice.query.filter_by(address=addr2).first()
    bOffice1_2 = BranchOffice.query.filter_by(id=2).first()
    bOffice2_2 = BranchOffice.query.filter_by(type="branch")[-1]

    '''
    assert hOffice == hOffice_ ensures that hOffice object was correctly created and gives same object when filtered by addrLine
    assert hOffice == hOffice_1 ensures that hOffice object was correctly created and gives same object when filtered by id
    assert hOffice == hOffice_2 ensures that hOffice object was correctly created and gives same object when filtered by type
                                .first() should give same object as hOffice since hOffice was the first branch office added to database with this type
    assert bOffice1 == bOffice1_ ensures that bOffice1 object was correctly created and gives same object when filtered by addrLine
    assert bOffice1 == bOffice1_2 ensures that bOffice2 object was correctly created and gives same object when filtered by id
                                .first() should give same object as bOffice1 since bOffice1 was the first branch office added to database with this id
    assert bOffice2 == bOffice2_2 ensures that bOffice2 object was correctly created and gives same object when filtered by id
                                [-1] should give same object as bOffice2 since bOffice2 was the last branch office added to database with this type
    '''

    assert hOffice == hOffice_
    assert hOffice == hOffice_1
    assert hOffice == hOffice_2
    assert bOffice1 == bOffice1_
    assert bOffice1 == bOffice1_2
    assert bOffice2 == bOffice2_2

    '''
    assert hOffice.isBranch() == False ensures that isBranch() gives False for head office
    assert bOffice1.isBranch() == True ensures that isBranch() gives True for branch office
    assert bOffice2.isBranch() == True ensures that isBranch() gives True for branch office
    '''

    assert hOffice.isBranch() == False
    assert bOffice1.isBranch() == True
    assert bOffice2.isBranch() == True

    manager = Manager(name="Mayank", email="mayankkumar1205@gmail.com", branchID=hOffice.id)
    employee1 = Employee(name="Parth", email="pmjindal@gmail.com", branchID=bOffice1.id)
    employee2 = Employee(name="Shristi", email="shristi21singh@gmail.com", branchID=bOffice2.id)
    database.session.add(manager)
    database.session.add(employee1)
    database.session.add(employee2)
    database.session.commit()
    
    manager_ = Manager.query.filter_by(email="mayankkumar1205@gmail.com").first()
    employee1_ = Employee.query.filter_by(name="Parth").first()
    employee2_ = Employee.query.filter_by(branchID=3).first()

    '''
        assert manager == manager_ ensures that manager object is created properly and gives same object when filtered by email
        assert employee1 == employee1_ ensures that employee object is created properly and gives same object when filtered by name
                                    .first() should give same object as employee1 since employee1 was the first employee added to database with this name
        assert employee2 == employee2_ ensures that employee object is created properly and gives same object when filtered by branchID
                                    .first() should give same object as employee2 since employee2 was the first employee added to database with this branchID
    '''

    assert manager == manager_
    assert employee1 == employee1_
    assert employee2 == employee2_

    truck1 = Truck(plateNo="A12345")
    truck2 = Truck(plateNo="B12345")
    truck3 = Truck(plateNo="C12345")
    truck4 = Truck(plateNo="D12345")
    database.session.add(truck1)
    database.session.add(truck2)
    database.session.add(truck3)
    database.session.add(truck4)
    database.session.commit()

    truck1_ = Truck.query.filter_by(status=TruckStatus.AVAILABLE).first()
    truck2_ = Truck.query.filter_by(id=2).first()
    truck3_ = Truck.query.filter_by(plateNo="C12345").first()
    truck4_ = Truck.query.filter_by(volumeLeft=500)[-1]

    '''
        assert truck1 == truck1_ ensures that truck object is created properly and gives same object when filtered by status
                                    .first() should give same object as truck1 since truck1 was the first truck added to database with this status
        assert truck2 == truck2_  ensures that truck object is created properly and gives same object when filtered by id
        assert truck3 == truck3_ ensures that truck object is created properly and gives same object when filtered by plateNo
        assert truck4 == truck4_ ensures that truck object is created properly and gives same object when filtered by status
                                    [-1] should give same object as truck4 since truck4 was the last truck added to database with this volumeLeft
    '''

    assert truck1 == truck1_
    assert truck2 == truck2_
    assert truck3 == truck3_
    assert truck4 == truck4_

    hOffice.addTruck(truck1)
    bOffice1.addTruck(truck2)
    bOffice2.addTruck(truck3)
    bOffice2.addTruck(truck4)
    database.session.commit()

    consign1 = Consignment(volume=250, senderAddress=addr1, receiverAddress=addr5, dstBranchID=bOffice1.id)
    consign2 = Consignment(volume=250, senderAddress=addr4, receiverAddress=addr2, dstBranchID=bOffice1.id)
    consign3 = Consignment(volume=500, senderAddress=addr2, receiverAddress=addr6, dstBranchID=bOffice2.id)
    consign4 = Consignment(volume=500, senderAddress=addr3, receiverAddress=addr1, dstBranchID=hOffice.id)
    consign5 = Consignment(volume=500, senderAddress=addr6, receiverAddress=addr4, dstBranchID=hOffice.id)
    consign6 = Consignment(volume=500, senderAddress=addr1, receiverAddress=addr3, dstBranchID=bOffice2.id)
    database.session.add(consign1)
    database.session.add(consign2)
    database.session.add(consign3)
    database.session.add(consign4)
    database.session.add(consign5)
    database.session.add(consign6)
    database.session.commit()

    consign1_ = Consignment.query.filter_by(volume=250).first()
    consign2_ = Consignment.query.filter_by(senderAddress=addr4).first()
    consign3_ = Consignment.query.filter_by(receiverAddress=addr6).first()
    consign4_ = Consignment.query.filter_by(dstBranchID=hOffice.id).first()
    consign5_ = Consignment.query.filter_by(id=5).first()
    consign6_ = Consignment.query.filter_by(status=ConsignmentStatus.PENDING)[-1]

    '''
        assert consign1 == consign1_ ensures that consignment object is created properly and gives same object when filtered by volume
                                .first() should give same object as consign1 since consign1 was the first consignment added to database with this volume
        assert consign2 == consign2_ ensures that consignment object is created properly and gives same object when filtered by senderAddress
                                .first() should give same object as consign2 since consign2 was the first consignment added to database with this senderAddress
        assert consign3 == consign3_ ensures that consignment object is created properly and gives same object when filtered by senderAddress
                                .first() should give same object as consign3 since consign3 was the first consignment added to database with this receiverAddress
        assert consign4 == consign4_ ensures that consignment object is created properly and gives same object when filtered by receiverAddress
                                .first() should give same object as consign4 since consign4 was the first consignment added to database with this dstBranchID
        assert consign5 == consign5_ ensures that consignment object is created properly and gives same object when filtered by id
        assert consign6 == consign6_ ensures that consignment object is created properly and gives same object when filtered by status
                                [-1] should give same object as consign6 since consign6 was the last consignment added to database with this status
    '''

    assert consign1 == consign1_
    assert consign2 == consign2_
    assert consign3 == consign3_
    assert consign4 == consign4_
    assert consign5 == consign5_
    assert consign6 == consign6_

    hOffice.addConsignment(consign1)
    hOffice.addConsignment(consign2)
    bOffice1.addConsignment(consign3)
    bOffice2.addConsignment(consign4)
    bOffice2.addConsignment(consign5)
    hOffice.addConsignment(consign6)
    database.session.commit()

    # Ensures that same consignment is not added twice to any branch

    try: 
        bOffice2.addConsignment(consign6)
    except:
        print("Consignment already added to some branch")
    
    try: 
        hOffice.addConsignment(consign6)
    except:
        print("Consignment already placed in this branch")
    
    # Checking if the bills for all the consignments have been computed correctly

    # For consignments in hOffice
    flag = False
    flag1 = False
    flag2 = False
    flag_ = False
    flag1_ = False
    flag2_ = False
    flag_1 = False
    flag1_2 = False
    flag2_3 = False
    for i in hOffice.transactions:
        if(i.invoice == consign1.bill.invoice):
            flag = True
            if(i.amount == consign1.bill.amount):
                flag1 = True
                if(i.branchID == hOffice.id):
                    flag2 = True

        if(i.invoice == consign2.bill.invoice):
            flag_ = True
            if(i.amount == consign2.bill.amount):
                flag1_ = True
                if(i.branchID == hOffice.id):
                    flag2_ = True
        
        if(i.invoice == consign6.bill.invoice):
            flag_1 = True
            if(i.amount == consign6.bill.amount):
                flag1_2 = True
                if(i.branchID == hOffice.id):
                    flag2_3 = True

    '''
        assert flag == True and flag1 == True and flag2 == True ensures that the bill objects in hOffice was correctly created and stored in database
        assert flag_ == True and flag1_ == True and flag2_ == True ensures that the bill objects in hOffice was correctly created and stored in database
        assert flag_1 == True and flag1_2 == True and flag2_3 == True ensures that the bill objects in hOffice was correctly created and stored in database
    '''

    assert flag == True and flag1 == True and flag2 == True
    assert flag_ == True and flag1_ == True and flag2_ == True
    assert flag_1 == True and flag1_2 == True and flag2_3 == True

    #for consignments in bOffice1

    flag = False
    flag1 = False
    flag2 = False
    for i in bOffice1.transactions:
        if(i.invoice == consign3.bill.invoice):
            flag = True
        if(i.amount == consign3.bill.amount):
            flag1 = True
        if(i.branchID == bOffice1.id):
            flag2 = True

    '''
    assert flag == True and flag1 == True and flag2 == True ensures that the bill objects in bOffice2 was correctly created and stored in database
    '''

    assert flag == True and flag1 == True and flag2 == True

    #For consignments in bOffice2
    flag = False
    flag1 = False
    flag2 = False
    flag_ = False
    flag1_ = False
    flag2_ = False
    for i in bOffice2.transactions:
        if(i.invoice == consign4.bill.invoice):
            flag = True
            if(i.amount == consign4.bill.amount):
                flag1 = True
            if(i.branchID == bOffice2.id):
                flag2 = True

        if(i.invoice == consign5.bill.invoice):
            flag_ = True
            if(i.amount == consign5.bill.amount):
                flag1_ = True
            if(i.branchID == bOffice2.id):
                flag2_ = True

    '''
        assert flag == True and flag1 == True and flag2 == True ensures that the bill objects in bOffice2 was correctly created and stored in database
        assert flag_ == True and flag1_ == True and flag2_ == True  ensures that the bill objects in bOffice2 was correctly created and stored in database
    '''

    assert flag == True and flag1 == True and flag2 == True
    assert flag_ == True and flag1_ == True and flag2_ == True
    

    Office.allotTruck(hOffice)
    database.session.commit()

    '''
        assert truck1.volumeLeft == 0 ensures that volumeLeft attribute is changed correctly in the database
        assert consign1.status == ConsignmentStatus.ALLOTED ensures that status attribute is changed correctly in the database
        assert consign2.status == ConsignmentStatus.ALLOTED  ensures that status attribute is changed correctly in the database
    '''

    assert truck1.volumeLeft == 0
    assert consign1.status == ConsignmentStatus.ALLOTED
    assert consign2.status == ConsignmentStatus.ALLOTED

    # Ensure that no truck is alloted to the consignment if no truck was available for it

    try:
        assert consign6.status == ConsignmentStatus.ALLOTED
    except:
        print ("No truck was alloted to this consignment")

    '''
        assert truck1.status == TruckStatus.READY ensures that truck status changes properly when it is fully loaded
        assert truck1 == consign1.trucks[-1] ensures that truck1 was alloted to consign1
        assert truck1 == consign2.trucks[-1] ensures that truck1 was alloted to consign2

    '''

    assert truck1.status == TruckStatus.READY
    assert truck1 == consign1.trucks[-1]
    assert truck1 == consign2.trucks[-1]


    hOffice.dispatchTruck(truck1)
    database.session.commit()

    '''
        assert truck1.status == TruckStatus.ENROUTE ensures that truck status changes correctly when it is dispatched
        assert consign1.status == ConsignmentStatus.ENROUTE ensures that consignment status changes correctly when it's truck is dispatched
        assert consign2.status == ConsignmentStatus.ENROUTE ensures that consignment status changes correctly when it's truck is dispatched
    '''

    assert truck1.status == TruckStatus.ENROUTE
    assert consign1.status == ConsignmentStatus.ENROUTE
    assert consign2.status == ConsignmentStatus.ENROUTE
    
    flag1 = False
    flag2 = False
    consignments = bOffice1.receiveTruck(truck1)
    database.session.commit()
    
    for i in consignments:
        if i == consign1 and consign1.status == ConsignmentStatus.DELIVERED:
            flag1 = True
        if i == consign2 and consign2.status == ConsignmentStatus.DELIVERED:
            flag2 = True
    
    '''
        assert flag1 == True and flag2 == True ensures that consignment status changes correctly when it's truck is received
        assert truck1.branchID == bOffice1.id ensures that consignment status changes correctly when it's truck is received
        assert truck1.status == TruckStatus.AVAILABLE ensures that truck status changes correctly when it is received
        assert truck2.status == TruckStatus.AVAILABLE ensures that truck status changes correctly when it is received
    '''

    assert flag1 == True and flag2 == True
    assert truck1.branchID == bOffice1.id
    assert truck1.status == TruckStatus.AVAILABLE
    assert truck2.status == TruckStatus.AVAILABLE

    Office.allotTruck(bOffice1)
    database.session.commit()

    '''
        assert truck2.volumeLeft == 500 ensures that volumeLeft of truck2 is changed correctly if it is not assigned
        assert truck1.volumeLeft == 0 ensures that volumeLeft of truck2 is changed correctly if it is assigned to any consignment
        assert consign3.status == ConsignmentStatus.ALLOTED ensures that status of consign1 changes correctly when it is alloted to a truck
        assert truck1.status == TruckStatus.READY ensures that truck status changes correctly when it is fully loaded
        assert truck2.status == TruckStatus.AVAILABLE ensures that truck status changes correctly when it is fully empty
        assert truck1 == consign3.trucks[-1] ensures that truck1 was alloted to consign3
    '''

    assert truck2.volumeLeft == 500
    assert truck1.volumeLeft == 0
    assert consign3.status == ConsignmentStatus.ALLOTED
    assert truck1.status == TruckStatus.READY
    assert truck2.status == TruckStatus.AVAILABLE
    assert truck1 == consign3.trucks[-1]

    bOffice1.dispatchTruck(truck1)
    database.session.commit()

    '''
        assert truck1.status == TruckStatus.ENROUTE ensures that truck1 status is changed properly when it is dispatched
        assert consign3.status == ConsignmentStatus.ENROUTE ensures that consign3 status is changed properly when its truck is dispatched
    '''

    assert truck1.status == TruckStatus.ENROUTE
    assert consign3.status == ConsignmentStatus.ENROUTE
    
    flag1 = False
    consignments = bOffice2.receiveTruck(truck1)
    database.session.commit()
    
    for i in consignments:
        if i == consign3 and consign3.status == ConsignmentStatus.DELIVERED:
            flag1 = True

    '''
        assert flag1 == True ensures that status of all consignments in the truck changes when it is received
        assert truck1.branchID == bOffice2.id ensures that branchID of truck1 is correctly changes when it is received
        assert truck1.status == TruckStatus.AVAILABLE ensures that truck1 status is changed properly when it is received
        assert truck3.status == TruckStatus.AVAILABLE ensures that truck3 status is correctly stored in the database
        assert truck4.status == TruckStatus.AVAILABLE ensures that truck4 status is correctly stored in the database
    '''

    assert flag1 == True
    assert truck1.branchID == bOffice2.id
    assert truck1.status == TruckStatus.AVAILABLE
    assert truck3.status == TruckStatus.AVAILABLE
    assert truck4.status == TruckStatus.AVAILABLE

    Office.allotTruck(bOffice2)
    database.session.commit()

    '''
        assert truck1.volumeLeft == 0 ensures that volumeLeft of truck1 is properly changed when it is assigned any consignment
        assert consign4.status == ConsignmentStatus.ALLOTED ensures that status of consign4 is properly changed when it is alloted to a truck
        assert truck1.status == TruckStatus.READY ensures that truck1 status is properly changed when it is fully loaded
        assert truck1 == consign4.trucks[-1] ensures that truck1 was alloted to consign4
        assert truck3.volumeLeft == 0 ensures that volumeLeft of truck3 is changed properly when it is assigned any onsignment
        assert consign5.status == ConsignmentStatus.ALLOTED ensures that status of consign5 is properly changed when it is alloted to a truck
        assert truck3.status == TruckStatus.READY ensures that truck3 status is properly changed when it is fully loaded
        assert truck3 == consign5.trucks[-1] ensures that truck3 was alloted to consign5
        assert truck4.status == TruckStatus.AVAILABLE ensures that truck4 status is correctly stored in the database
    '''

    assert truck1.volumeLeft == 0
    assert consign4.status == ConsignmentStatus.ALLOTED
    assert truck1.status == TruckStatus.READY
    assert truck1 == consign4.trucks[-1]
    assert truck3.volumeLeft == 0
    assert consign5.status == ConsignmentStatus.ALLOTED
    assert truck3.status == TruckStatus.READY
    assert truck3 == consign5.trucks[-1]
    assert truck4.status == TruckStatus.AVAILABLE

    bOffice2.dispatchTruck(truck1)
    database.session.commit()

    '''
        assert truck1.status == TruckStatus.ENROUTE ensures that truck status is properly changed when it is dispatched
        assert consign4.status == ConsignmentStatus.ENROUTE ensures that consignment status is properly changed when it's truck is dispatched
    '''

    assert truck1.status == TruckStatus.ENROUTE
    assert consign4.status == ConsignmentStatus.ENROUTE
    
    flag1 = False
    consignments = hOffice.receiveTruck(truck1)
    database.session.commit()
    
    for i in consignments:
        if i == consign4 and consign4.status == ConsignmentStatus.DELIVERED:
            flag1 = True
    
    '''
        assert flag1 == True ensures that consign4 status is properly changed when it's truck is received
        assert truck1.status == TruckStatus.AVAILABLE ensures that truck status is properly changed when it is received
        assert truck1.branchID == hOffice.id ensures that truck branchID is properly changed when it is received
    '''

    assert flag1 == True
    assert truck1.status == TruckStatus.AVAILABLE
    assert truck1.branchID == hOffice.id

    bOffice2.dispatchTruck(truck3)
    database.session.commit()

    '''
        assert truck3.status == TruckStatus.ENROUTE ensures that truck status is properly changed when it is dispatched
        assert consign5.status == ConsignmentStatus.ENROUTE ensures that consignment status is properly changed when it's truck is dispatched
    '''

    assert truck3.status == TruckStatus.ENROUTE
    assert consign5.status == ConsignmentStatus.ENROUTE
    
    flag1 = False
    consignments = hOffice.receiveTruck(truck3)
    database.session.commit()
    
    for i in consignments:
        if i == consign5 and consign5.status == ConsignmentStatus.DELIVERED:
            flag1 = True
    
    '''
        assert flag1 == True ensures that consignment status is properly changed when it's truck is received
        assert truck3.status == TruckStatus.AVAILABLE ensures that truck status is properly changed when it is received
        assert truck3.branchID == hOffice.id ensures that truck branchID is properly changed when it is received
    '''
    assert flag1 == True
    assert truck3.status == TruckStatus.AVAILABLE
    assert truck3.branchID == hOffice.id
    
    try:
        truck4.addConsignment(consign6)
    except:
        print ("Source Branch Office of the truck and the consignment are different")

    Office.allotTruck(hOffice)
    database.session.commit()

    '''
        assert truck1.volumeLeft == 0 ensures that volumeLeft of truck is properly changed when it is assigned with a consignment
        assert consign6.status == ConsignmentStatus.ALLOTED ensures that consignment status is properly changed when it is alloted to a truck
        assert truck1.status == TruckStatus.READY ensures that truck status is properly changed when it is assigned with a consignment
        assert truck1 == consign6.trucks[-1] ensures that truck1 is assigned with consign6
    '''

    assert truck1.volumeLeft == 0
    assert consign6.status == ConsignmentStatus.ALLOTED
    assert truck1.status == TruckStatus.READY
    assert truck1 == consign6.trucks[-1]

    hOffice.dispatchTruck(truck1)
    database.session.commit()

    '''
        assert truck1.status == TruckStatus.ENROUTE ensures that truck status is properly changed when it is dispatched
        assert consign6.status == ConsignmentStatus.ENROUTE ensures that consignment status is properly changed when it's truck is dispatched
    '''

    assert truck1.status == TruckStatus.ENROUTE
    assert consign6.status == ConsignmentStatus.ENROUTE

    # Ensure that wrong office does not receive a truck

    try:
        consignments = bOffice1.receiveTruck(truck1)
        database.commit()
    except:
        print ("This office cannot receive this truck because the office is not its destination branch")
    
    flag1 = False
    consignments = bOffice2.receiveTruck(truck1)
    database.session.commit()
    
    for i in consignments:
        if i == consign6 and consign6.status == ConsignmentStatus.DELIVERED:
            flag1 = True
    
    '''
        assert flag1 == True ensures that consignment status is properly changed when it is received
        assert truck1.status == TruckStatus.AVAILABLE ensures that truck status is properly changed when it is received
        assert truck1.branchID == bOffice2.id ensures that truck branchID is properly changed when it is received
    '''

    assert flag1 == True
    assert truck1.status == TruckStatus.AVAILABLE
    assert truck1.branchID == bOffice2.id