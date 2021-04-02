from app import create_app, db
from app.models import *


def main():
    app = create_app()
    with app.app_context():

        addr1 = Address(addrLine="C-28", city="Delhi", zipCode="110009")
        addr2 = Address(addrLine="H-1/2", city="Chennai", zipCode="110004")
        a = HeadOffice(name="Delhi Office", address=addr1)
        b = BranchOffice(name="Chennai Office", address=addr2)
        
        db.create_all()
        db.session.add(a)
        db.session.add(b)
        db.session.commit()



main()