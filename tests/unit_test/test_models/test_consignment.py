from app.models import Address, Bill
from app.models import Consignment

def test_consignment(test_client, database):
    """

    """
    addr1 = Address(city = "Delhi", addrLine = "C-28,Model Town-3", zipCode = "110009")
    addr2 = Address(city = "Mumbai", addrLine = "H-Block", zipCode = "100120")
    consign = Consignment(volume = 200, senderAddress = addr1, receiverAddress = addr2, dstBranchID=1)
    database.session.add(consign)
    database.session.commit()
    consign1 = Consignment.query.filter_by(senderAddress = addr1)[-1]


    assert addr1 == consign1.senderAddress
    assert addr2 == consign1.receiverAddress
    assert 200 == consign1.volume

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
    