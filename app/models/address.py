from app import db


class Address(db.Model):
    """
        A class to represent an address
        ....

        Attributes
        ----------
        addressLine: string
            house/block of address
        city: string
            city name
        zipCode: string
            zip-code of address
    """
    __tablename__ = "address"

    id = db.Column(db.Integer, primary_key=True)
    addrLine = db.Column(db.String(128), index=True)
    city = db.Column(db.String(64), index=True)
    zipCode = db.Column(db.String(6), index=True)

    def __init__(self, addrLine=None, city=None, zipCode=None, **kwargs) -> None:
        """
            The constructor for Address class
            ....

            Pararmeters:
                addrLine: string
                    house/block of address
                city: string
                    city name
                zipCode: string
                    zip-code of address

        """
        super().__init__(**kwargs)
        self.addrLine = addrLine
        self.city = city
        self.zipCode = zipCode

    def __repr__(self) -> str:
        """
            The function to get the string representation of the address
            ....

            Returns:
                str: A string which stores the representation of the address
        """
        return f'< Address: {self.addrLine}' \
            f'City: {self.city} PIN: {self.zipCode}>'


class Bill(db.Model):
    """
        A class to represent a bill
        ....

        Attributes
        ----------
        amount: int
            amount to be paid
        paymentID: string
            paymentID of the payment made by the customer
    """
    ################################# ORM #################################
    __tablename__ = "bill"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, index=True, nullable=False)
    paymentID = db.Column(db.String(64), index=True, nullable=False)

    def __init__(self, **kwargs) -> None:
        """
            The constructor of the Bill class
            ....

            Parameters:
                amount: int
                    amount to be paid
                paymentID: string
                    paymentID of the payment made by the customer

        """
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        """
            The function to get the string representation of the bill
            ....

            Returns:
                str: A string which stores the representation of the bill
        """
        return f'<Bill: {self.amount}, Transaction Code: {self.paymentID}>'
