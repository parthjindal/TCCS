from app import db


class Office(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    adress_id = db.Column(db.Integer, db.ForeignKey('address.id'),
                          nullable=False)
    address = db.relationship('Address', uselist=False, lazy=False)
    ## TODO ###
    ## ADD TRUCK ##
    
    def __repr__(self) -> str:
        return f'<Office: {self.name}, Address: {self.address}>'
