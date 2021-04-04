from flask import Blueprint

consign = Blueprint("consign", __name__,
                 template_folder="../templates", url_prefix="/consign")
from app.consign import routes