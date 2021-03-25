from app import create_app, db;
from app.models import *;

app = create_app();
app.app_context().push();
db.session.rollback()
db.create_all()
a = Employee(name = "Parth",email = "something")
b = Manager(name = "Mayank",email = "something2")
c = Employee(name = "Shristi",email = "something3")

addr1 = Address(city = "Delhi")
addr2 = Address(city = "Mumbai")

office1 = BranchOffice(name = "Branch Office",address = addr2)
office2 = HeadOffice(name = "Head Office",address = addr1)

office1.employees.append(a)
office2.employees.append(c)
# office2.employees.append(b)
office2.manager = b

db.session.add(office1)
db.session.add(office2)

db.session.commit()
print(Office.query.get(1).type)
print(Office.query.get(2).manager)



