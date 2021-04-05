from app.truck import truck
from flask import redirect, url_for, flash, current_app, request, render_template
from flask_login import current_user, login_required
from app import db, mail
from app.models import Office, Consignment, Address, Truck, Manager, TruckStatus
from .forms import TruckForm, ReceiveTruckForm
from flask_mail import Message
from datetime import datetime


@truck.route("/view/all", methods=["GET"])
@login_required
def view_all():
    x = 1
    if current_user.role == "manager":
        trucks = Truck.query.all()
    elif current_user.role == "employee":
        trucks = Truck.query.filter_by(branchID=current_user.branchID)
    if trucks is None:
        x = 0
    return render_template("view_all.html", data=trucks, len=x), 200


@truck.route("/view/<id>", methods=["GET"])
@login_required
def view(id):
    truck_ = Truck.query.get(id)

    if truck_ is not None:
        consigns = truck_.consignments
        x = len(consigns)
        value = []
        ts = []
        for i in truck_.usage:
            value.append(i.value)
            ts.append(datetime.timestamp(i.time))
        value2 = []
        ts2 = []
        for i in truck_.idle:
            value2.append(i.value)
            ts2.append(datetime.timestamp(i.time))
        return render_template("truck.html", role=current_user.role, truck=truck_, data=consigns, len=x, values=value, labels=ts, values2=value2, labels2=ts2), 200
    flash("Truck not registered", "warning")
    return redirect(url_for("main.home"), code=302)


@truck.route("/dispatch/view", methods=["GET"])
@login_required
def dispatch():
    trucks = Truck.query.filter_by(branchID=current_user.branchID)
    readyTrucks = []
    for i in trucks:
        if i.status == TruckStatus.READY:
            readyTrucks.append(i)
            print(i.status)
    x = len(readyTrucks)
    return render_template("dispatch.html", data=readyTrucks, len=x), 200


@truck.route("/dispatch/<id>")
@login_required
def dispatch_truck(id):

    truck_ = Truck.query.get(id)
    branch = Office.query.get(current_user.branchID)

    branch.dispatchTruck(truck_)
    db.session.commit()

    ################### SHOW DETAILS OF ALL CONSIGNMENTS IN SIDE IT BEFORE DISPATCH ###################
    flash("Truck Logged as dispatched", "info")
    return redirect(url_for("main.home"))


@truck.route("/request-for", methods=['GET', 'POST'])
@login_required
def request_truck():
    '''

    '''
    if current_user.role == "manager":
        # flash('Access Denied', 'warning')
        # return redirect(url_for('main.home', role=current_user.role), code=302)
        return render_template('errors/403.html'), 403

    manager = Manager.query.filter_by(role="manager").first()
    office = Office.query.filter_by(id=current_user.branchID).first()

    msg = Message('Buy New Truck Request',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[manager.email],
                  body=render_template("request_truck.txt", user=manager, branch=office))
    mail.send(msg)

    flash('Request mail sent!', 'success')
    return redirect(url_for('main.home', role=current_user.role), code=302)


@truck.route("/add", methods=["GET", "POST"])
@login_required
def add():
    '''

    '''
    if current_user.role == "employee":
        return render_template('errors/403.html'), 403

    if current_user.role == "manager":

        form = TruckForm()
        if form.validate_on_submit():

            truck_ = Truck(plateNo=form.plateNo.data)
            db.session.add(truck_)
            db.session.commit()

            branch = Office.query.get(form.branch.data)
            branch.addTruck(truck_)

            db.session.commit()
            Office.allotTruck(branch)

            db.session.commit()

            flash("Truck Added", 'success')
            return redirect(url_for("main.home"), code=302)

        return render_template("add.html", title="Buy new truck", form=form), 200


@truck.route("/receive", methods=["GET", "POST"])
@login_required
def receive():
    if current_user.role == "manager":
        return render_template('errors/403.html'), 403
    form = ReceiveTruckForm()
    if form.validate_on_submit():
        truck_ = Truck.query.filter_by(plateNo=form.plateNo.data).first()
        if truck_ is None:
            return redirect(url_for("main.home"), code=302)
        branch = Office.query.filter_by(id=current_user.branchID).first()

        branch.receiveTruck(truck_)
        db.session.commit()

        Office.allotTruck(branch)
        db.session.commit()

        flash("Truck logged as received", 'info')
        return redirect(url_for("main.home"), code=302)
        ################################### TODO #################################################
    return render_template('receive.html', form=form, title="Receive Truck"), 200
