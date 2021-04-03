from operator import add
from app.models import Address


def test_address():
    """
    GIVEN a Address model
    WHEN a new Address is created
    THEN check the city, addressLine, zipcode
    """
    addr = Address(city = "Delhi",addrLine = "C-28,Model Town-3",zipCode = "110009")
    assert "Delhi" == addr.city
    assert "C-28,Model Town-3" == addr.addrLine
    assert "110009" == addr.zipCode    
    