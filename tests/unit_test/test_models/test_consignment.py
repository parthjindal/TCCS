from app.models import Address, Bill
from app.models import Consignment

def test_consignment(test_client, database):
    """
    Unit test for Consignment class
    """
    addr1 = Address(city = "Delhi", addrLine = "C-28,Model Town-3", zipCode = "110009")
    addr2 = Address(city = "Mumbai", addrLine = "H-Block", zipCode = "100120")
    consign = Consignment(volume = 200, senderAddress = addr1, receiverAddress = addr2, dstBranchID=1)
    database.session.add(consign)
    database.session.commit()
    consign1 = Consignment.query.filter_by(senderAddress = addr1).first()
    consign2 = Consignment.query.filter_by(volume = 200).first()
    consign3 = Consignment.query.filter_by(dstBranchID=1).first()
    consign4 = Consignment.query.filter_by(receiverAddress = addr2,).first()

    '''
    assert consign1 == consign  To check that correct object was created and returned 
                        when filtered by senderAddress
    assert consign2 == consign  To check that correct object was created and returned 
                        when filtered by volume
    assert consign3 == consign  To check that correct object was created and returned 
                        when filtered by dstBranchID
    assert consign4 == consign  To check that correct object was created and returned 
                        when filtered by receiverAddress
    '''
    assert consign1 == consign
    assert consign2 == consign
    assert consign3 == consign
    assert consign4 == consign
    
    '''
    To check that all the elements of the dictionary returned on calling getInvoice() are correct
    '''
    consign_dict = consign1.getInvoice()
    assert consign_dict['volume'] == 200
    assert consign_dict['placetime'] == consign.placetime
    assert consign_dict['charge'] == consign.charge
    assert consign_dict['sender']['city'] == addr1.city
    assert consign_dict['sender']['address'] == addr1.addrLine
    assert consign_dict['sender']['zipCode'] == addr1.zipCode
    assert consign_dict['receiver']['city'] == addr2.city
    assert consign_dict['receiver']['address'] == addr2.addrLine
    assert consign_dict['receiver']['zipCode'] == addr2.zipCode
    