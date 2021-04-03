from app.models.office import BranchOffice
from app.cart import cart
from .forms import ConsignmentForm, TruckForm
from flask import redirect, url_for
from flask_login import current_user, login_required
from flask import request, render_template
from app.models import Office, Consignment, Address, Truck
from app import db
from flask import flash,jsonify


@cart.route("/")
@login_required
def index():
    if current_user.role == "employee":
        branch = Office.query.get(current_user.branchID).name
        return redirect(url_for("cart.place", branch=branch, id=current_user.id))
    else:
        flash("Access Denied")
        return redirect(url_for("main.home"))        

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
            dstBranchId=form.destinationBranch.data, srcBranchId=current_user.branchID)
        db.session.add(consign)
        db.session.commit()
        
        flash("Consignment Placed for Delivery")
        return redirect(url_for("main.home"))
    return render_template("cart/place.html", title="Place Consignment", form=form)

@cart.route("/addTruck", methods=["GET", "POST"])
@login_required
def addTruck():
    if current_user.is_authenticated and current_user.role == "manager":
        form = TruckForm()
        if form.validate_on_submit():
            trck = Truck(
                plateNo=form.plateNo.data, usageTime=0, idleTime=0)
            brnch = BranchOffice.query.get(form.branch.data)
            # print(brnch)
            db.session.add(trck)
            db.session.commit()
            brnch.addTruck(trck)
            flash("Truck has been added")
            return redirect(url_for("main.home"))
        return render_template("cart/addTruck.html", title="Buy new truck", form=form)
    flash('You are not authorized to access this page', 'warning')
    return redirect(url_for('main.home', role=current_user.role))


@cart.route("/view/branch", methods=["GET"])
@login_required
def view():
    consignments = Consignment.query.filter_by(srcBranchId = current_user.branchID)



@cart.route("/receive/",methods = ["GET","POST"])
@login_required
def receive():
    branchID = current_user.branchID
