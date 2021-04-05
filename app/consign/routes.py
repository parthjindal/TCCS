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
        The user needs to be logged in to use this function
        If the current user is an employee, he is redirected to the 
                    place consignment page of the office of the employee
        Else an error occurs because access is denied

    '''
    if current_user.role == "employee":

        office = Office.query.get(current_user.branchID)
        office_addr = f'{office.address.city}-office'
        return redirect(url_for("consign.place", office=office_addr, id=office.id), code=302)

    else:

        # flash("Access Denied", 'warning')
        # return redirect(url_for("main.home"), code=302)
        return render_template('errors/403.html'), 403


@consign.route("/place", methods=["GET", "POST"])
@login_required
def place():
    '''
        The function used by the user to place a consignment in his office
        The employee needs to be logged in to use this

        If the office id of the employee is valid, the an object of the Consignment class is created
                with srcBranchID equal to the branchID of the user's office and
                        other credentials as specified and is added to the database 
                                after this the employee is redirected to the home page
        Else a warning is displayed and the user is redirected to the home page
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
            dstBranchID=form.branch.data)

        db.session.add(consign)
        office = Office.query.get(id)
        office.addConsignment(consign)
        db.session.add(office.transactions[-1])
        db.session.commit()
        Office.allotTruck(Office.query.get(id))

        db.session.commit()

        flash("Consignment Placed for Delivery", 'info')
        return redirect(url_for("main.home"), code=302)

    return render_template("consign/place.html", title="Place Consignment", form=form), 200


@consign.route("/view/all", methods=["GET"])
@login_required
def view_all():
    '''
        If the user is an Employee, this function allows him to view all the consignments
                that are placed in his office

        If the user is the Manager, he can view all the consignments 
                irrepective of their source office
    '''
    if current_user.role == "employee":
        consigns = Consignment.query.filter_by(
            srcBranchID=current_user.branchID).all()
    elif current_user.role == "manager":
        consigns = Consignment.query.all()
    return render_template('consign/view_all.html', data=consigns), 200


@consign.route("/view/<id>")
@login_required
def view(id):
    '''
        This function allows the user to view the details of any consignment provided 
                the id of the required consignment given by the user is correct
        ....

        Parameters:
            id: int
                the id of the consignment, the user wants to query about
    '''
    consign = Consignment.query.get(id)
    if consign is None:
        flash("Bad request, consignment not found", "warning")
        return redirect(url_for("main.home", role=current_user.role), code=302)

    ############################ TODO #####################################################
    return render_template('consign/view2.html', data=consign), 200