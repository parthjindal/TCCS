from flask import Blueprint
auth = Blueprint("auth", __name__,
                 template_folder="../templates/auth", url_prefix="/auth")
from .forms import LoginForm, ManagerRegistrationForm, RegistrationForm, ResetPasswordForm, RequestResetForm
from app.auth import routes
