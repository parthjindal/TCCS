from app.truck import truck
from flask import redirect, url_for, flash, current_app, request, render_template
from flask_login import current_user, login_required
from app import db, mail
from app.models import Office, Consignment, Address, Truck, Manager
from .forms import TruckForm
from flask_mail import Message


@truck.route("/view/all", methods=["GET"])
@login_required
def view_all():
    if current_user.role == "manager":
        trucks = Truck.query.all()
    elif current_user.role == "employee":
        trucks = Truck.query.filter_by(branchID=current_user.branchID)
    return render_template("view_all.html", data=trucks)


@truck.route("/view/<id>", methods=["GET"])
@login_required
def view(id):
    truck_ = Truck.query.get(id)

    if truck_ is not None:
        consigns = truck_.consigns
        render_template("truck.html", truck=truck_, data=consigns)
    flash("Truck not registered", "warning")
    return redirect(url_for("main.home"))


@truck.route("/dispatch", methods=["GET"])
@login_required
def dispatch():
    trucks = Truck.query.filter_by(branchID=current_user.branchID)
    trucks = [x for x in trucks if x.volumeLeft < 5]
    return render_template("dispatch.html", data=trucks)


@truck.route("/request/", methods=['GET', 'POST'])
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
                  body=render_template("request_truck.txt", user=manager, branch=office))
    mail.send(msg)

    flash('Request mail sent!', 'success')
    return redirect(url_for('main.home', role=current_user.role))


@truck.route("/add", methods=["GET", "POST"])
@login_required
def add():
    '''

    '''
    if current_user.role == "employee":

        flash("Access Denied", "warning")
        return redirect(url_for("main.home", role=current_user.role))

    if current_user.role == "manager":

        form = TruckForm()
        if form.validate_on_submit():

            truck_ = Truck(plateNo=form.plateNo.data, branchID=form.branch.data)
            db.session.add(truck_)
            db.session.commit()

            flash("Truck Added", 'success')
            return redirect(url_for("main.home"))

        return render_template("add.html", title="Buy new truck", form=form)


@truck.route("/receive", methods=["GET", "POST"])
@login_required
def receive():
    ############ TODO ####################
    branchID = current_user.branchID
