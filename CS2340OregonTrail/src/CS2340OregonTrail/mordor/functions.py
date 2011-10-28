from django.db import models

def main():
    return

def populateLocations():
    locations=[]
    for x in range(50):
        locations[x] = Location()
    location[0] = Location(name = "The Shire", description = "")
    location[25] = Location(name = "Mines of Moria")
    location[49] = Location(name = "Mordor")
    
def initialStore():
    store = Store(name = "Initial store")
    store.addItem(Item(name = "Food", amount = 10))
    store.addItem(Item(name = "Wagon Wheel", amount = 10))