from app import create_app, db
from app.models import *


def main():
    app = create_app()
    with app.app_context():

        addr1 = Address(addrLine="C-28", city="Delhi", zipCode="110009")
        addr2 = Address(addrLine="H-1/2", city="Chennai", zipCode="110004")
        headOffice = HeadOffice(name="Delhi Office", address=addr1)
        branchOffice = BranchOffice(name="Chennai Office", address=addr2)
        
        manager = Manager(name = "Parth",email = "pmjindal@gmail.com",headOffice = headOffice.id)
        manager.set_password("ParthJindal")
        db.create_all()
        db.session.add(headOffice)
        db.session.add(branchOffice)
        db.session.add(manager)
        db.session.commit()

main()