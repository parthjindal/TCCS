from app.cart import cart
from .forms import ConsignmentForm
from flask import redirect, url_for
from flask_login import current_user, login_required
from flask import request, render_template
from app.models import Office, Consignment, Address
from app import db


@cart.route("/")
@login_required
def index():
    if current_user.is_authenticated:
        branch = Office.query.get(current_user.branchID).name
    return redirect(url_for("cart.place", branch=branch, Id=current_user.id))


@cart.route("/place/<branch>/<id>", methods=["GET", "POST"])
@login_required
def place(branch, id):
    form = ConsignmentForm()
    if form.validate_on_submit():
        senderAddress = Address(addressLine=form.senderAddress.addrLine.data,
                                city=form.senderAddress.city.data, zipCode=form.senderAddress.zipCode.data)
        receiverAddress = Address(addressLine=form.receiverAddress.addrLine.data,
                                  city=form.receiverAddress.city.daata, zipCode=form.receiverAddress.zipCode.data)
        consign = Consignment(
            volume=form.volume.data, senderAddress=senderAddress, receiverAddress=receiverAddress,
            dstBranch=form.destinationBranch.data)
        db.session.add(consign)
        db.session.commit()
        return redirect(url_for("main.home"))
    return render_template("cart/place.html", title="Place Consignment", form=form)
