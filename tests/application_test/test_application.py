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
        This is the application test for the Transport Company Computerization Software(TCCS)
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
    bOffice1_ = BranchOffice.query.filter_by(address=addr2).first()
    bOffice2_ = BranchOffice.query.filter_by(address=addr3).first()

    assert hOffice == hOffice_
    assert bOffice1 == bOffice1_
    assert bOffice2 == bOffice2_

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
    employee1_ = Employee.query.filter_by(email="pmjindal@gmail.com").first()
    employee2_ = Employee.query.filter_by(email="shristi21singh@gmail.com").first()

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

    truck1_ = Truck.query.filter_by(plateNo="A12345").first()
    truck2_ = Truck.query.filter_by(plateNo="B12345").first()
    truck3_ = Truck.query.filter_by(plateNo="C12345").first()
    truck4_ = Truck.query.filter_by(plateNo="D12345").first()

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

    consign1_ = Consignment.query.filter_by(receiverAddress=addr5).first()
    consign2_ = Consignment.query.filter_by(receiverAddress=addr2).first()
    consign3_ = Consignment.query.filter_by(receiverAddress=addr6).first()
    consign4_ = Consignment.query.filter_by(receiverAddress=addr1).first()
    consign5_ = Consignment.query.filter_by(receiverAddress=addr4).first()
    consign6_ = Consignment.query.filter_by(receiverAddress=addr3).first()

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

    try: 
        bOffice2.addConsignment(consign6)
    except:
        print("Consignment already added to some branch")
    
    try: 
        hOffice.addConsignment(consign6)
    except:
        print("Consignment already placed in this branch")
    
    #Checking if the bills for all the consignments have been computed correctly

    #For consignments in hOffice
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

    assert flag == True and flag1 == True and flag2 == True
    assert flag_ == True and flag1_ == True and flag2_ == True
    

    assert truck1.status == TruckStatus.AVAILABLE

    Office.allotTruck(hOffice)
    database.session.commit()

    assert truck1.volumeLeft == 0
    assert consign1.status == ConsignmentStatus.ALLOTED
    assert consign2.status == ConsignmentStatus.ALLOTED
    try:
        assert consign6.status == ConsignmentStatus.ALLOTED
    except:
        print ("Consignment could not be alloted to any truck due to lack of free volume")
    assert truck1.status == TruckStatus.READY
    assert truck1 == consign1.trucks[-1]
    assert truck1 == consign2.trucks[-1]


    hOffice.dispatchTruck(truck1)
    database.session.commit()
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
    assert flag1 == True and flag2 == True
    assert truck1.branchID == bOffice1.id


    assert truck1.status == TruckStatus.AVAILABLE
    assert truck2.status == TruckStatus.AVAILABLE

    Office.allotTruck(bOffice1)
    database.session.commit()

    assert truck2.volumeLeft == 500
    assert truck1.volumeLeft == 0
    assert consign3.status == ConsignmentStatus.ALLOTED
    assert truck1.status == TruckStatus.READY
    assert truck2.status == TruckStatus.AVAILABLE
    assert truck1 == consign3.trucks[-1]

    bOffice1.dispatchTruck(truck1)
    database.session.commit()
    assert truck1.status == TruckStatus.ENROUTE
    assert consign3.status == ConsignmentStatus.ENROUTE
    
    flag1 = False
    consignments = bOffice2.receiveTruck(truck1)
    database.session.commit()
    
    for i in consignments:
        if i == consign3 and consign3.status == ConsignmentStatus.DELIVERED:
            flag1 = True

    assert flag1 == True
    assert truck1.branchID == bOffice2.id


    assert truck1.status == TruckStatus.AVAILABLE
    assert truck3.status == TruckStatus.AVAILABLE
    assert truck4.status == TruckStatus.AVAILABLE

    Office.allotTruck(bOffice2)
    database.session.commit()

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
    assert truck1.status == TruckStatus.ENROUTE
    assert consign4.status == ConsignmentStatus.ENROUTE
    
    flag1 = False
    consignments = hOffice.receiveTruck(truck1)
    database.session.commit()
    
    for i in consignments:
        if i == consign4 and consign4.status == ConsignmentStatus.DELIVERED:
            flag1 = True
    assert flag1 == True
    assert truck1.branchID == hOffice.id

    bOffice2.dispatchTruck(truck3)
    database.session.commit()
    assert truck3.status == TruckStatus.ENROUTE
    assert consign5.status == ConsignmentStatus.ENROUTE
    
    flag1 = False
    consignments = hOffice.receiveTruck(truck3)
    database.session.commit()
    
    for i in consignments:
        if i == consign5 and consign5.status == ConsignmentStatus.DELIVERED:
            flag1 = True
    assert flag1 == True
    assert truck3.branchID == hOffice.id
    
    try:
        truck4.addConsignment(consign6)
    except:
        print ("Source Branch Office of the truck and the consignment are different")

    Office.allotTruck(hOffice)
    database.session.commit()

    assert truck1.volumeLeft == 0
    assert consign6.status == ConsignmentStatus.ALLOTED
    assert truck1.status == TruckStatus.READY
    assert truck1 == consign6.trucks[-1]

    hOffice.dispatchTruck(truck1)
    database.session.commit()
    assert truck1.status == TruckStatus.ENROUTE
    assert consign6.status == ConsignmentStatus.ENROUTE

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
    assert flag1 == True
    assert truck1.branchID == bOffice2.id