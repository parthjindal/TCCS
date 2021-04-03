from app.models import Address
from app.models import Consignment

def test_consignment():
    """

    """
    addr1 = Address(city = "Delhi", addrLine = "C-28,Model Town-3", zipCode = "110009")
    addr2 = Address(city = "Mumbai", addrLine = "H-Block", zipCode = "100120")
    consign = Consignment(volume = 500, senderAddress = addr1, receiverAddress = addr2)

    assert addr1 == consign.senderAddress
    assert addr2 == consign.receiverAddress
    assert 500 == consign.volume

