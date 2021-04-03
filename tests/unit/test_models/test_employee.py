from app.models import Address, Bill
from app.models import Employee, Manager
from app.models import Consignment



def test_new_employee(test_client, database):
    """
        
    """
    
    employee = Employee(name = "Parth", branchID = 1, email = "pmjindal@gmail.com")
    employee.set_password("DoShallItMay")
    database.session.add(employee)
    database.session.commit()
    e1 = Employee.query.filter_by(email = "pmjindal@gmail.com").first()


    assert e1.email == "pmjindal@gmail.com"
    assert e1.name == "Parth"
    assert e1.check_password("DoShallItMay") == True
    assert e1.role == "employee"


def test_manager(test_client, database):
    """
        
    """
    manager = Manager(name = "Mayank",email = "mayankkumar1205@gmail.com")
    manager.set_password("WhySoSerious")
    #manager.changeRate(10)
    database.session.add(manager)
    database.session.commit()
    m1 = Manager.query.filter_by(email = "mayankkumar1205@gmail.com").first()

    assert m1.email == "mayankkumar1205@gmail.com"
    assert m1.name == "Mayank"
    assert m1.check_password("WhySoSerious") == True
    assert m1.role == "manager"
    #assert rate == 10

