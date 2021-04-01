from app.models.consignment import Consignment, ConsignmentStatus
from app import create_app, db
from app.models import *

app = create_app()
app.app_context().push()
db.session.rollback()
db.create_all()

