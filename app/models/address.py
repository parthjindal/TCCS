from app import db

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(64), index=True)
    zipCode = db.Column(db.String(6), index=True)
    addressLine = db.Column(db.String(128), index=True)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
    
    def __repr__(self) -> str:
        return f'< Address: {self.addressLine} \
           City: {self.city} PIN: {self.zipCode}>'