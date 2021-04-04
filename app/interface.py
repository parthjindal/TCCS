from app.models import Office, ConsignmentStatus, TruckStatus, Bill


class Interface():

    @staticmethod
    def compareDate(consign):
        return consign.placetime

    @staticmethod
    def compareVol(truck):
        return truck.volumeLeft

    @staticmethod
    def allotTruck(branch):
        consigns = []
        for consign in branch.consignments:
            if consign.status == ConsignmentStatus.PENDING:
                consigns.append(consign)

        consigns.sort(reverse=True, key=Interface.compareDate)

        trucks = []
        for truck in branch.trucks:
            if truck.status != TruckStatus.ENROUTE:
                trucks.append(truck)
        trucks.sort(reverse=True, key=Interface.compareVol)

        for consign in consigns:
            for truck in trucks:
                try:
                    truck.addConsignment(consign)
                    break
                except:
                    continue

    @staticmethod
    def computeBill(consign,rate):
        if consign.status == ConsignmentStatus.PENDING or consign.status == ConsignmentStatus.ALLOTED \
           or consign.status == ConsignmentStatus.DELIVERED:
            raise ValueError("Consignment status not correct")
        if consign.volumeLeft != 0:
            return ValueError("Consignment volume still left")
        charge = consign.volume * rate
        return charge
