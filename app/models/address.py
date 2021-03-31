from app import db

class Address(db.Model):
    """
        A class to represent an address
        ....

        Attributes
        ----------
        addressLine: str
            house/block of address
        city: str
            city name
        zipCode: str
            zip-code of address
    """
    __tablename__ = "address"

    id = db.Column(db.Integer, primary_key=True)
    addrLine = db.Column(db.String(128), index=True)
    city = db.Column(db.String(64), index=True)
    zipCode = db.Column(db.String(6), index=True)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
    
    def __repr__(self) -> str:
        return f'< Address: {self.addrLine}' \
           f'City: {self.city} PIN: {self.zipCode}>'


class Bill(db.Model):
    """
        A class representing Bill entity
        ....

        Attributes
        ----------
        amount:  int

        paymentID:  str
            transaction code/IFSC code
    """
    __tablename__ = "bill"

    id = db.Column(db.Integer,primary_key = True)
    amount = db.Column(db.Integer,index = True , nullable = False)
    paymentID = db.Column(db.String(64),index = True,nullable = False)


    def __init__(self,**kwargs) -> None:
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return f'<Bill: {self.amount}, Transaction Code: {self.paymentID}>'