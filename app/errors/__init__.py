from flask import Blueprint
errors = Blueprint("error", __name__,
                 template_folder="../templates/error", url_prefix="")
# from .forms import LoginForm, ManagerRegistrationForm, RegistrationForm, ResetPasswordForm, RequestResetForm
from app.errors import routes
