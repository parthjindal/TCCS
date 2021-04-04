from app.models import ConsignmentStatus, TruckStatus, Bill


class Interface():
    
    @staticmethod
    def computeBill(consign, rate):
        if consign.status == ConsignmentStatus.PENDING or consign.status == ConsignmentStatus.ALLOTED \
           or consign.status == ConsignmentStatus.DELIVERED:
            raise ValueError("Consignment status not correct")
        if consign.volumeLeft != 0:
            return ValueError("Consignment volume still left")
        charge = consign.volume * rate
        return charge
