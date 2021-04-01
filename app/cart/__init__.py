from flask import Blueprint

cart = Blueprint("cart", __name__,
                 template_folder="../templates", url_prefix="/cart")
from app.cart import routes