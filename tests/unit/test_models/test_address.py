from operator import add
from app.models import Address


def test_address(test_client, database):
    """
    GIVEN a Address model
    WHEN a new Address is created
    THEN check the city, addressLine, zipcode
    """
    addr = Address(city = "Delhi",addrLine = "C-28,Model Town-3",zipCode = "110009")
    database.session.add(addr)
    database.session.commit()
    addr1 = Address.query.filter_by(city = "Delhi").last()
    
    assert "Delhi" == addr1.city
    assert "C-28,Model Town-3" == addr1.addrLine
    assert "110009" == addr1.zipCode    
    