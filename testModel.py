from app.models.consignment import Consignment, ConsignmentStatus
from app import create_app, db
from app.models import *

app = create_app()
app.app_context().push()
db.session.rollback()
db.create_all()

# print(db.get_tables_for_bind())
empl1 = Employee(name="Parth", email="pmjindal@gmail.com")
manager = Manager(name="Mayank", email="something2")
empl2 = Employee(name="Shristi", email="something3")

empl1.set_password("parth")
empl2.set_password("s")

addr1 = Address(city="Delhi")
addr2 = Address(city="Mumbai")

office1 = HeadOffice(name="Delhi Office", address=addr1)
office2 = BranchOffice(name="Mumbai Office", address=addr2)

cons = Consignment(
    volume=100, senderAddress=addr1, receiverAddress=addr2,
    status=0)

t1 = Truck(volumeConsumed = 0,usageTime = 0,idleTime = 0,status = 0)
t1.consignments.append(cons)
db.session.add(t1)
db.session.commit()

print(t1)
print(cons.trucks[0])
print(cons)


office1.employees.append(empl1)
office2.employees.append(empl2)
office2.manager = manager

db.session.add(office1)
db.session.add(office2)
# db.session.add(Truck)
db.session.commit()



print(Office.query.get(1).type)
print(Office.query.get(2).manager)
