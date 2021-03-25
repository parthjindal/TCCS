from app import create_app, db
from app.models import Address
from app.models.office import Office

app = create_app()
app.app_context().push()

