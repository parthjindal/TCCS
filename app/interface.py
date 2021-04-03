from app.models import *



def compar(truck:Truck):
    return (truck.volume-truck.volumeConsumed)


def allotTruck(consign,Branch:BranchOffice):
    trucks = Branch.trucks
    trucks.sort(key = compar,reverse = True)
    for truck in trucks:
        try

