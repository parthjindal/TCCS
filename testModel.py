from app.models.consignment import Consignment, ConsignmentStatus
from app.models import Address
from app import create_app, db
from app.models import Office,BranchOffice,Address


app = create_app()
app.app_context().push()
# db.session.rollback()
db.create_all()
addr1 = Address(city="Delhi", zipCode="110009")
addr2 = Address(city="Mumbai", zipCode="110008")
a = BranchOffice()
b = BranchOffice(address=addr2)
con1 = Consignment(volume=100, senderAddress=addr1,
                   receiverAddress=addr2)
con2 = Consignment(volume=200, senderAddress=addr1,
                   receiverAddress=addr2, charge=0)
con3 = Consignment(volume=100, senderAddress=addr2,
                   receiverAddress=addr1, charge=0)
con4 = Consignment(volume=200, senderAddress=addr2,
                   receiverAddress=addr1,charge=0)
db.session.add(a)
db.session.add(b)
db.session.add(con1)
db.session.add(con2)
db.session.add(con3)
db.session.add(con4)
# a.addConsignment(con1)
# a.addConsignment(con2)
# b.addConsignment(con3)
# b.addConsignment(con4)
db.session.add(con1)
db.session.add(addr1)
db.session.commit()
print(con1.senderID)
print(con1.senderAddress)
