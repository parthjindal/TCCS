from app.models import Address, Bill
from app.models import Consignment

def test_consignment(test_client, database):
    """

    """
    addr1 = Address(city = "Delhi", addrLine = "C-28,Model Town-3", zipCode = "110009")
    addr2 = Address(city = "Mumbai", addrLine = "H-Block", zipCode = "100120")
    consign = Consignment(volume = 200, senderAddress = addr1, receiverAddress = addr2)
    database.session.add(consign)
    database.session.commit()
    consign1 = Consignment.query.filter_by(senderAddress = addr1)[-1]


    assert addr1 == consign1.senderAddress
    assert addr2 == consign1.receiverAddress
    assert 200 == consign1.volume

    # assert "1" == consign.srcBranchId
    # assert "2" == consign.dstBranchId
