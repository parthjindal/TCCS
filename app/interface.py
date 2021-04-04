from app.models import ConsignmentStatus, TruckStatus, Bill


class Interface():
    
    @staticmethod
    def computeBill(consign, rate):
        charge = consign.volume * rate
        return charge
