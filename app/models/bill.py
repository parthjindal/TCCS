from app import db

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
    branchID = db.Column(db.Integer, db.ForeignKey('office.id'))
    invoice = db.Column(db.String(128))

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
