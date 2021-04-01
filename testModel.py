from app.models.consignment import Consignment, ConsignmentStatus
from app import create_app, db
from app.models import *

app = create_app()
app.app_context().push()
db.session.rollback()
db.create_all()
addr1 = Address(city = "Delhi",zipCode = "110009")
addr2 = Address(city = "Mumbai",zipCode = "110008")
a = BranchOffice(name = "Delhi Office",address = addr1)
b = BranchOffice(name = "Mumbai Office",address = addr2)
db.session.add(a)
db.session.add(b)
db.session.commit()