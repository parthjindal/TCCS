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

        Member Functions:
        ----------------
         
        __repr__(): str
            returns the string representation of an object of the class
    """

    __tablename__ = "address"

    id = db.Column(db.Integer, primary_key=True)
    addrLine = db.Column(db.String(128), index=True)
    city = db.Column(db.String(64), index=True)
    zipCode = db.Column(db.String(6), index=True)

    def __init__(self, addrLine=None, city=None, zipCode=None, **kwargs) -> None:
        """
            The constructor for Address class called automatically whenever an object
                    of the Address class is created
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
                str
        """
        return f'< Address: {self.addrLine}' \
            f'City: {self.city} PIN: {self.zipCode}>'
