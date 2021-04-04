from flask import Blueprint

truck = Blueprint("truck", __name__,
                 template_folder="../templates/truck", url_prefix="/truck")
from app.truck import routes