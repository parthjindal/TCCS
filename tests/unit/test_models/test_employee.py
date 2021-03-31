from app.models.address import Address,Bill
from app.models import Employee,Manager, employee
from app.models import Consignment


def test_new_employee():
    """
        
    """
    employee = Employee(name = "Parth",email = "pmjindal@gmail.com")
    employee.set_password("DoShallItMay")

    assert employee.email == "pmjindal@gmail.com"
    assert employee.name == "Parth"
    assert employee.check_password("DoShallItMay") == True
    assert employee.role == "employee"

def test_consignment():
    """

    """
    addr1 = Address(city = "Delhi",addrLine = "C-28,Model Town-3",zipCode = "110009")
    addr2 = Address(city = "Mumbai",addrLine = "H-Block",zipCode = "100120")
    consign = Consignment(volume = 500,senderAddress = addr1,receiverAddress = addr2)

    ########TODO#############


def test_Bill():
    b1 = Bill(amount = 10,paymentID = "1000")
    assert b1.amount == 10
    assert b1.paymentID == "1000"