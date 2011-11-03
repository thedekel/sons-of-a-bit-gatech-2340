from models import *
from coords import *

#wagon = Wagon(partyz)Wo
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
    """
    This takes a turn.  Shocking, no?
    """
    party = Party.objects.get(id = partyid)
    party.consumeFood()
    moveLocation(partyid)
    
def buyItem(partyid, itemName, num, mult): # string, string, int, float
    """
    @param item: the item to buy 
    @param amount: amount the user wants
    Buys an items
    Checks for sufficient money and capacity
    @return: String: string based on the success of the transaction
    """
    msg = "Your transaction was successful."
    # creating an item here
    abase = Item.objects.get(name=itemName)
    party = Party.objects.get(id = partyid)
    wag = party.wagon_set.all()[0]
    if wag.checkWagCap(abase, num):
        if (wag.party.money - (mult * abase.baseCost * num)) >= 0:
            wag.party.money -= mult * abase.baseCost * num
            wag.party.save()
            wag.weight += abase.weight * num
            wag.save()
            if not wag.inventory.hasItem(itemName):
                newItem = Iteminstance(base=Item.objects.get(name=itemName),amount=num,inventory=wag.inventory)
                newItem.save()
            else:
                thing = wag.inventory.iteminstance_set.get(base = abase)
                thing.amount += num
                thing.save()
        else:
            msg = "You do not have enough money for this purchase."
    else:
        msg = "Your wagon cannot carry this much weight"
        if wag.party.money - item.calculatePrice() >= 0:
            msg += "and you do not have enough money for this purchase."
        else:
            msg += "."
    return msg


def moveLocation(partyid): #int
    """
    Moves along the map array to "change" location.
    Any locations that would force a halt will be checked for here (representing with a boolean field in Location, will change later to something else)
    Most of these parameters probably won't be needed
    -Anthony Taormina
    """
    party = Party.objects.get(id=partyid)
    for x in range(int(party.pace/.5)):
        party.location += 1
#        loc = Location.objects.get(index=party.location)
 #       if loc.halt:
  #          break
    party.save()
   # loc.event_set.all()[0].do()
    

def populateLocations():
    """
    This generates the map, which sits in the database, referenced by an index element
    Used once for instantiation
    @return: A list of Locations
    """
    locations=[]
    events = []
    for num in range(131):
        coord = get_player_coords(num)
        loc = Location(x=coord[0],y=coord[1],index=num)
        loc.save()
        locations.append(loc)
        eee=Event(location = loc)
        eee.save()
        events.append(eee)
        
    for z in [6, 39, 75, 125]:
        locations[z] = Location(halt=True, index=z, x=locations[z].x, y=locations[z].y)
        rce= RiverCrossingEvent(location = locations[z])
        rce.save()
        events[z]=rce
    for a in [[0,"Hobbiton"],[16,"Bree"],[38,"Thrabad"],[74,"Gap of Rohan"],[89,"Edoras"],[106,"Minas Tirith"]]:
        locations[a[0]] = Location(name=a[1],halt=True, index=a[0], x=locations[a[0]].x, y=locations[a[0]].y)
        ste= StoreEvent(location = locations[a[0]],name = a[1])    
        events[a[0]]=ste 
    ll = Location(name = "Mordor",halt=True, index=130, x=locations[130].x, y=locations[130].y)
    ll.save()
    locations[130] = ll
    events[130] = EndGame(location=locations[130])

def takeFerry(partyid): #string
    """
    Takes the Ferry. Takes a designated amount of money away from the player
    to use the ferry
    """
    party = Party.objects.get(id=partyid)
    party.money -= 250
    party.save()
    return "you paid 250 currency to cross the bridge"
    
def ford():
    """
    Attempts to ford the river. Fails if water depth is greater than 3 feet.
    @return: String: The success or failure of fording the river
    """ 
    chance = random.randint(0,100)
    percentChance = 5 * 2
    if (chance > (100 - percentChance)):
        msg = "DUDE FLIP THE WAGON!"
        return msg
    return 0
    
def caulk():
    """
    Attempts to float over the river on the wagon. Greater chance of wagon flip.
    @return: String: The success or failure of caulking the river
    """
    chance = random.randint(0,100)
    if (chance > 70):
        msg = "DUDE FLIP THE WAGON"
        return msg
    return 0

