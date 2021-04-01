from app.cart import cart
from .forms import ConsignmentForm
from flask import redirect, url_for
from flask_login import current_user, login_required
from flask import request,render_template
from app.models import Office,Consignment


@cart.route("/")
@login_required
def index():
    if current_user.is_authenticated:
        branch = Office.query.get(current_user.branchID).name
    return redirect(url_for("cart.place", branch=branch, Id=current_user.id))


@cart.route("/place/", methods=["GET", "POST"])
@login_required
def place():
    if request.method == "GET":
        branch = request.args.get("branch")
        Id = request.args.get("id")

        form = ConsignmentForm()
        form.destinationBranch.choices = [(x.id,x.name) for x in Office.query.order_by("name")]
        if form.validate_on_submit():
            print({f"{x.data}":x.data for x in form})
            # consign = Consignment()
        return "{}".format(x for x in form.destinationBranch.choices)