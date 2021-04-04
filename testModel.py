from app.models.consignment import Consignment, ConsignmentStatus
from app.models import Address
from app import create_app, db
from app.models import Office, BranchOffice, Address,HeadOffice


app = create_app()
app.app_context().push()
# db.session.rollback()
db.create_all()

addr1 = Address(city="Mumbai", addrLine="H-Block", zipCode="100120")
addr2 = Address(city="Delhi", addrLine="C-28,Model Town-3",
                zipCode="110009")
bOffice = BranchOffice(address=addr1)
hOffice = HeadOffice(address=addr2)

db.session.add(bOffice)
db.session.add(hOffice)
db.session.commit()