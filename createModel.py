from app.models.consignment import Consignment, ConsignmentStatus
from app.models import Address
from app import create_app, db
from app.models import Office, BranchOffice, Address,HeadOffice, Truck


app = create_app()
app.app_context().push()
# db.session.rollback()
db.create_all()

addr1 = Address(city="Mumbai", addrLine="Egret Mumbai Office", zipCode="100120")
addr2 = Address(city="Delhi", addrLine="Egret Delhi Office", zipCode="110009")
addr3 = Address(city="Kolkata", addrLine="Egret Kolkata Office", zipCode="410009")
bOffice = BranchOffice(address=addr1)
hOffice = HeadOffice(address=addr2)
bOffice2 = BranchOffice(address=addr3)
truck1 = Truck(plateNo="12ABCD")
truck2 = Truck(plateNo="12EFGH")
truck3 = Truck(plateNo="12IJKL")

db.session.add(bOffice)
db.session.add(hOffice)
db.session.add(bOffice2)
db.session.commit()

bOffice.addTruck(truck1)
hOffice.addTruck(truck2)
bOffice2.addTruck(truck3)
db.session.commit()