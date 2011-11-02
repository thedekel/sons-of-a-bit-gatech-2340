from models import *


#wagon = Wagon(partyz)
#wagon.save()



            

#def storeLoader(storeid):
#    """
#    The initializer for the initial store in the game.
#    @param storeid the id of the store. if attached to location
#    @return an object of the store just loaded. can be modified and .save()'d
#    """
#    astore = Store.objects.get(id=storeid)
#    return astore;
def takeATurn(partyid):
    party = Party.object.get(id = partyid)
    

def moveLocation(partyid): #int
    """
    Moves along the map array to "change" location.
    Any locations that would force a halt will be checked for here (representing with a boolean field in Location, will change later to something else)
    Most of these parameters probably won't be needed
    -Anthony Taormina
    """
	
    party = Party.objects.get(id=partyid)
    numSpaces = 2 * party.pace # (each index is .5 km)
    for x in range(1, numSpaces+1):
        party.location += 1
        place = locmap[party.location] # a Location
        if place.halt:
            break
    party.save()
    place.do()
    
    
def getFood(wagonid):
    """
    @param wagon: takes in a wagon to access the player's inventory
    This is used to find out how much food we have at any given point.
    @return: the amount of rations the player currently has left 
    """
    wagon = Wagon.objects.get(id=wagonid)
    for thing in wagon.inventory.items_set.all():
        if thing.name == "food":
            return thing.amount


def populateLocations():
    """
    This generates the map, which is represented as a list of Locations
    @return: A list of Locations
    """
    locations=[]
    for x in range(50):
        locations.append(Location())
    locations[25] = Location(name = "Mines of Moria")
    locations[49] = Location(name = "Mordor")
    return locations
 
locmap = populateLocations()
