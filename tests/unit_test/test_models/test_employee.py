from app.models import Address, Bill
from app.models import Employee, Manager
from app.models import Consignment



def test_new_employee(test_client, database):
    """
    Unit test function to test Employee class
    """
    
    employee = Employee(name = "Parth", branchID = 1, email = "pmjindal@gmail.com")
    employee.set_password("DoShallItMay")
    database.session.add(employee)
    database.session.commit()

    e1 = Employee.query.filter_by(email = "pmjindal@gmail.com").first()
    e2 = Employee.query.filter_by(name = "Parth").first()
    e3 = Employee.query.filter_by(branchID = 1).first()

    '''
    assert e1 == employee ensures that object is created properly and returned correcty on being filtered by email
    assert e2 == employee ensures that object is created properly and returned correcty on being filtered by name
    assert e3 == employee ensures that object is created properly and returned correcty on being 
                            filtered by branchID
    '''
    assert e1 == employee
    assert e2 == employee
    assert e3 == employee
    
    '''
    Ensures that no two employees have the same email id
    '''
    try:
        employee1 = Employee(name = "Partha", branchID = 2, email = "pmjindal@gmail.com")
        database.session.add(employee1)
        database.session.commit()
    except:
        print ("The given email-id has already been registered")



def test_manager(test_client, database):
    """
      Unit test function to test the Manager class  
    """
    manager = Manager(name = "Mayank",email = "mayankkumar1205@gmail.com", branchID = 2)
    manager.set_password("WhySoSerious")
    #manager.changeRate(10)
    database.session.add(manager)
    database.session.commit()
    m1 = Manager.query.filter_by(email = "mayankkumar1205@gmail.com").first()
    m2 = Manager.query.filter_by(name = "Mayank").first()
    m3 = Manager.query.filter_by(branchID = 2).first()
    
    '''
    assert m1 == manager ensures that object is created properly and returned correcty on being filtered by email
    assert m2 == manager ensures that object is created properly and returned correcty on being filtered by name
    assert m3 == manager ensures that object is created properly and returned correcty on being 
                            filtered by branchID
    '''
    assert m1 == manager
    assert m2 == manager
    assert m3 == manager
    
    '''
    Ensures that no employee can have the same email id as the manager
    '''
    try:
        employee = Employee(name = "Mayankk",email = "mayankkumar1205@gmail.com")
        database.session.add(employee)
        database.session.commit()
    except:
        print ("The given email-id has already been registered")

