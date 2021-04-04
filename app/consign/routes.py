from app.consign import consign
from flask import redirect, url_for, flash, current_app, request, render_template
from flask_login import current_user, login_required
from app import db, mail
from app.models import Office, Consignment, Address, Truck, Manager
from .forms import ConsignmentForm
from flask_mail import Message


@consign.route("/", methods=["GET"])
@login_required
def index():
    '''

    '''
    if current_user.role == "employee":

        office = Office.query.get(current_user.branchID)
        office_addr = f'{office.address.city}-office'
        return redirect(url_for("consign.place", office=office_addr, id=office.id), code=302)

    else:

        # flash("Access Denied", 'warning')
        # return redirect(url_for("main.home"), code=302)
        return render_template('errors/403.html', code=200)


@consign.route("/place", methods=["GET", "POST"])
@login_required
def place():
    '''

    '''
    office = request.args.get("office")
    id = request.args.get("id")

    if Office.query.get(id) is None:
        flash("Bad request", "warning")
        return redirect(url_for("main.home"), code=302)

    form = ConsignmentForm()
    if form.validate_on_submit():

        senderAddress = Address(addrLine=form.sAddrLine.data,
                                city=form.sCity.data, zipCode=form.sZipCode.data)
        receiverAddress = Address(addrLine=form.rAddrLine.data,
                                  city=form.rCity.data, zipCode=form.rZipCode.data)
        consign = Consignment(
            volume=form.volume.data, senderAddress=senderAddress, receiverAddress=receiverAddress,
            dstBranchID=form.branch.data, srcBranchID=id)

        db.session.add(consign)
        db.session.commit()

        flash("Consignment Placed for Delivery", 'info')
        return redirect(url_for("main.home"), code=302)

    return render_template("consign/place.html", title="Place Consignment", form=form, code=200)


@consign.route("/view/all", methods=["GET"])
@login_required
def view_all():
    if current_user.role == "employee":
        consigns = Consignment.query.filter_by(
            srcBranchID=current_user.branchID).all()
    elif current_user.role == "manager":
        consigns = Consignment.query.all()
    return render_template('consign/view_all.html', data=consigns, code=200)


@consign.route("/view/<id>")
@login_required
def view(id):
    consign = Consignment.query.get(id)
    if consign is None:
        flash("Bad request, consignment not found", "warning")
        return redirect(url_for("main.home", role=current_user.role), code=302)
    return f'{consign}'
