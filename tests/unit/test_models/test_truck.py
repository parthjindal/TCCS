from app.models import Address
from app.models import Consignment
from app.models import Truck


def test_truck(test_client, database):
    """
        
    """
    t1 = Truck(plateNo = "01TK0423")
    addr1 = Address(city = "Delhi", addrLine = "C-28,Model Town-3", zipCode = "110009")
    addr2 = Address(city = "Mumbai", addrLine = "H-Block", zipCode = "100120")
    addr3 = Address(city = "Delhi", addrLine = "D-Block", zipCode = "110009")
    addr4 = Address(city = "Mumbai", addrLine = "A-Block", zipCode = "100120")
    consign1 = Consignment(volume = 300, senderAddress = addr1, receiverAddress = addr2)
    consign2 = Consignment(volume = 200, senderAddress = addr3, receiverAddress = addr4)


    t1.addConsignment(consign1)
    t1.addConsignment(consign2)
    
    database.session.add(t1)
    database.session.commit()

    consign = Consignment(volume = 200, senderAddress = addr3, receiverAddress = addr4)
    try:
        t1.addConsignment(consign)
    except:
        print ("No space available\n")
    t2 = Truck.query.filter_by(plateNo = "01TK0423").first()

    consign3 = Consignment.query.filter_by(senderAddress = addr1)[-1]
    consign4 = Consignment.query.filter_by(senderAddress = addr3)[-1]
    f1 = False
    f2 = False
    f3 = False
    f4 = False

    assert "01TK0423" == t2.plateNo
    assert 0 == t2.volumeLeft

    for i in t2.consignments:
        if (i == consign3):
            f1 = True
        
        if (i == consign4):
            f2 = True

    assert (f1 == True)
    assert (f2 == True)

    for i in consign1.trucks:
        if (i == t2):
            f3 = True
        
    for i in consign2.trucks:
        if (i == t2):
            f4 = True

    assert (f3 == True)
    assert (f4 == True)

    lst = t1.empty()
    database.session.commit()
    t3 = Truck.query.filter_by(plateNo = "01TK0423").first()
    
    f1 = False
    f2 = False
    f3 = False
    f4 = False
    
    for i in lst:
        if (i.senderAddress == consign1.senderAddress):
            f1 = True
        
        if (i.senderAddress == consign2.senderAddress):
            f2 = True

    for i in consign1.trucks:
        if (i == t3):
            f3 = True
        
    for i in consign2.trucks:
        if (i == t3):
            f4 = True
    
    assert (f1 == True)
    assert (f2 == True)
    assert (f3 == False)
    assert (f4 == False)

    consign = Consignment(volume = 501, senderAddress = addr3, receiverAddress = addr4)
    try:
        t1.addConsignment(consign)
    except:
        print ("Volume of Consignment is too large\n")

    

        


    

    

