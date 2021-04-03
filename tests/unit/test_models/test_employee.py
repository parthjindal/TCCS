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


def test_manager():
    """
        
    """
    manager = Manager(name = "Mayank",email = "mayankkumar1205@gmail.com")
    manager.set_password("WhySoSerious")
    manager.changeRate(10)

    assert manager.email == "mayankkumar1205@gmail.com"
    assert manager.name == "Mayank"
    assert manager.check_password("WhySoSerious") == True
    assert manager.role == "manager"
    assert rate == 10

