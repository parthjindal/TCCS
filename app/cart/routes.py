from app.models.office import BranchOffice
from app.cart import cart
from .forms import ConsignmentForm, TruckForm
from flask import redirect, url_for
from flask_login import current_user, login_required
from flask import request, render_template
from app.models import Office, Consignment, Address, Truck, Manager
from app import db, mail
from flask import flash
from flask_mail import Message
from flask import current_app


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

@cart.route("/request_truck", methods=['GET', 'POST'])
@login_required
def request_truck():
    if current_user.is_authenticated and current_user.role == "manager":
        flash('You are not authorized to access this page', 'success')
        return redirect(url_for('main.home', role=current_user.role))
    user = Manager.query.filter_by(role="manager").first()
    brnch = Office.query.filter_by(id=current_user.branchID).first()
    msg = Message('Buy New Truck Request',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[user.email])
    msg.body = f'''Hi {user.name}
    
An employee at Egret {current_user.name} requested for adding truck to the branch {brnch.name}.

To buy a new truck for the branch, please go to the following web address:
{url_for('cart.addTruck', _external=True)}

To check the statistics of the branches, please visit:
{url_for('main.branches', _external=True)}

Team Egret
'''
    mail.send(msg)
    flash('The request has been sent to the manager', 'success')
    return redirect(url_for('main.home', role=current_user.role))

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


@cart.route("/view/branch",methods = ["GET"])
@login_required
def view():
    orderID = request.args.get("order")
    consign = Consignment.query.get(orderID)
    