from app.cart import cart
from flask import redirect, url_for, flash, current_app, request, render_template
from flask_login import current_user, login_required
from app import db, mail
from app.models import Office, Consignment, Address, Truck, Manager
from .forms import ConsignmentForm, TruckForm
from flask_mail import Message


@cart.route("/place", methods=["GET"])
@login_required
def index():
    '''

    '''
    if current_user.role == "employee":

        office = Office.query.get(current_user.branchID)
        office_addr = f'{office.address.city}-office'
        return redirect(url_for("cart.place", office=office_addr, id=office.id))

    else:

        flash("Access Denied", 'warning')
        return redirect(url_for("main.home"))


@cart.route("/place/<office>/<id>/", methods=["GET", "POST"])
@login_required
def place(office, id):
    '''

    '''
    form = ConsignmentForm()
    if form.validate_on_submit():

        senderAddress = Address(addrLine=form.senderAddrLine.data,
                                city=form.sCity.data, zipCode=form.sZipCode.data)
        receiverAddress = Address(addrLine=form.rAddrLine.data,
                                  city=form.rCity.data, zipCode=form.rZipCode.data)
        consign = Consignment(
            volume=form.volume.data, senderAddress=senderAddress, receiverAddress=receiverAddress,
            dstBranchID=form.branch.data, srcBranchID=office.id)

        db.session.add(consign)
        db.session.commit()

        flash("Consignment Placed for Delivery", 'info')
        return redirect(url_for("main.home"))

    return render_template("cart/place.html", title="Place Consignment", form=form)


@cart.route("/request-truck/", methods=['GET', 'POST'])
@login_required
def request_truck():
    '''

    '''
    if current_user.role == "manager":
        flash('Access Denied', 'warning')
        return redirect(url_for('main.home', role=current_user.role))

    manager = Manager.query.filter_by(role="manager").first()
    office = Office.query.filter_by(id=current_user.branchID).first()

    msg = Message('Buy New Truck Request',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[manager.email],
                  body=render_template("request", user=manager, branch=office))
    mail.send(msg)

    flash('Request mail sent!', 'success')
    return redirect(url_for('main.home', role=current_user.role))


@cart.route("/add-truck/", methods=["GET", "POST"])
@login_required
def addTruck():
    '''

    '''
    if current_user.role == "employee":

        flash("Access Denied", "warning")
        return redirect(url_for("main.home"), role=current_user.role)

    if current_user.role == "manager":

        form = TruckForm()
        if form.validate_on_submit():

            truck = Truck(plateNo=form.plateNo.data, branchID=form.branch.data)
            db.session.add(truck)
            db.session.commit()

            flash("Truck Added", 'success')
            return redirect(url_for("main.home"))

        return render_template("cart/addTruck.html", title="Buy new truck", form=form)


@cart.route("/receive/truck", methods=["GET", "POST"])
@login_required
def receive():
    branchID = current_user.branchID
