from app.models import Address, Bill
from app.models import Employee, Manager
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




