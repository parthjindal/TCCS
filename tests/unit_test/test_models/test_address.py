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
    addr1 = Address.query.filter_by(city = "Delhi").first()
    addr2 = Address.query.filter_by(addrLine = "C-28,Model Town-3").first()
    addr3 = Address.query.filter_by(zipCode = "110009").first()
    addr4 = Address.query.filter_by(id = 1).first()
    
    '''
    assert addr1 == addr ensures that the object is created properly and returned correctly when filtered by city
    assert addr2 == addr ensures that the object is created properly and returned correctly when filtered by addrLine
    assert addr3 == addr ensures that the object is created properly and returned correctly when filtered by zipCode
    assert addr4 == addr ensures that the object is created properly and returned correctly when filtered by id
    '''
    assert addr1 == addr   
    assert addr2 == addr   
    assert addr3 == addr   
    assert addr4 == addr   
    