from models import *



wagon = Wagon(partyz)
wagon.save()
itemDict = [ # this is where you add items to the game (name, des, basecost, weight)
            ("Food", "", 1, 1),
            ("Wagon Wheel", "", 100, 10)
            ]
for article in itemDict:
    newItem  = Item(article[0], article[1], article[2], store, maxAmounts, article[3])
    newItem.save()
    wagon.inventory.addItem(newItem) # puts item holder in inventory at 0 amount

def populateLocations():
    """
    This generates the map, which is represented as a list of Locations
    @return: A list of Locations
    """
    locations=[]
    for x in range(50):
        locations[x] = Location()
    location[25] = Location(name = "Mines of Moria")
    location[49] = Location(name = "Mordor")
    return locations
    
def storeMaker(storeName, maxAmounts, bannedItems):
    """
    The initializer for the initial store in the game.
    @param storeName: The name of the store. string
    @param maxAmounts: How much of each item does this store carry? int
    @param bannedItems: What items is this store missing?  list
    """
    store = Store(name = storeName)
    store.save()
    for article in itemDict:
        if article not in bannedItems:
            newItem  = Item(article[0], article[1], article[2], store, maxAmounts, article[3])
            newItem.save()
            store.addItem(newItem)
	return store;
        

def moveLocation(map, currentLocation, numSpaces): #array of Locations, int, int
    """
    Moves along the map array to "change" location.
    Any locations that would force a halt will be checked for here (representing with a boolean field in Location, will change later to something else).
    Most of these parameters probably won't be needed
    -Anthony Taormina
    """
    numSpaces *= 2 # (each index is .5 km)
    for x in range(1, numSpaces+1):
        place = map[currentLocation + x] # a Location
        if place.halt:
            break
    place.do()
    
    
    
