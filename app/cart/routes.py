from app.cart import cart
from .forms import ConsignmentForm
from flask import redirect, url_for
from flask_login import current_user, login_required
from flask import request, render_template
from app.models import Office, Consignment, Address
from app import db
from flask import flash


@cart.route("/")
@login_required
def index():
    if current_user.is_authenticated:
        branch = Office.query.get(current_user.branchID).name
    return redirect(url_for("cart.place", branch=branch, id=current_user.id))


@cart.route("/place/<branch>/<id>", methods=["GET", "POST"])
@login_required
def place(branch, id):
    form = ConsignmentForm()
    if form.validate_on_submit():
        senderAddress = Address(addrLine=form.senderAddrLine.data,
                                city=form.senderCity.data, zipCode=form.senderZipCode.data)
        receiverAddress = Address(addrLine=form.receiverAddrLine.data,
                                  city=form.receiverCity.data, zipCode=form.receiverZipCode.data)
        consign = Consignment(
            volume=form.volume.data, senderAddress=senderAddress, receiverAddress=receiverAddress,
            dstBranchId=form.destinationBranch.data, srcBranchId=current_user.branchID, status=0, volumeLeft=form.volume.data)
        db.session.add(consign)
        db.session.commit()
        flash("Consignment Placed for Delivery")
        return redirect(url_for("main.home"))
    return render_template("cart/place.html", title="Place Consignment", form=form)


@cart.route("/view/branch",methods = ["GET"])
@login_required
def view():
    orderID = request.args.get("order")
    consign = Consignment.query.get(orderID)
    