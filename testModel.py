from app.models.consignment import Consignment, ConsignmentStatus
from app.models import Address
from app import create_app, db
from app.models import Office,BranchOffice,Address


app = create_app()
app.app_context().push()
db.create_all()