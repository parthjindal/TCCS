from app.models import *


def compar(truck: Truck):
    return (truck.volume-truck.volumeConsumed)

# def compar(consignment: Consignment):

def getCharge():
    pass

def allotTruck(Branch: BranchOffice):
    pass
#     for consignment in Branch.consignments:
        





    # trucks = Branch.trucks
    # trucks.sort(key=compar, reverse=True)
    # for truck in trucks:
    #     if truck.status == TruckStatus.ENROUTE:
    #         continue
    #     if truck.status == TruckStatus.ASSIGNED and truck.dstBranchId != consign.dstBranchId:
    #         continue
    #     truck.addConsignment()