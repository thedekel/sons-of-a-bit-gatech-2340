from models import *
from coords import *

def takeATurn(partyid):
    """
    This takes a turn.  Shocking, no?
    """
    party = Party.objects.get(id = partyid)
    if not party.consumeFood():
        stuck(partyid, "Your party is out of food and cannot proceed")
        return
    moveLocation(partyid)
    party.save()

def stuck(partyid,msg):
    party = Party.objects.get(id = partyid)
    party.stopmsg = msg
    party.pace = 0
    party.rations = 0
    party.save()
    
def buyItem(partyid, itemName, num, mult): # string, string, int, float
    """
    @param item: the item to buy 
    @param amount: amount the user wants
    Buys an items
    Checks for sufficient money and capacity
    @return: String: string based on the success of the transaction
    """
    abase = Item.objects.get(name = itemName)
    aparty = Party.objects.get(id = partyid)
    if (num <=0):
        aparty.stopmsg = "You can't buy a negative amount, that would be weird..."
        aparty.save()
        return
    if (num*mult*abase.baseCost>aparty.money):
        aparty.stopmsg = "You can't afford this purchase"
        aparty.save()
        return
    wag = Wagon.objects.get(party=aparty)
    if (wag.weight + abase.wight * num > wag.capacity):
        aparty.stopmsg = "You can't buy these items; they're too heavy!"
        aparty.save()
        return
    inv = Inventory.objects.get(wagon = wag)
    if itemName in map(lambda q: q.base.name, inv.iteminstance_set.all()):
        ii = inv.iteminstance_set.get(base = abase)
        ii.amount += num
        ii.save()
        aparty.stopmsg = "Successfully added %d items of type %s" %(num, itemName)
        aparty.save()
    else:
        ii = Iteminstance(base = abase, amount = num, inventory = inv)
        ii.save()
        aparty.stopmsg = "Successfully purchased %d items of type %s" %(num, itemName)
        aparty.save()
    return




def moveLocation(partyid): #int
    """
    Moves along the map array to "change" location.
    Any locations that would force a halt will be checked for here (representing with a boolean field in Location, will change later to something else)
    Most of these parameters probably won't be needed
    -Anthony Taormina
    """
    aparty = Party.objects.get(id = partyid)
    dl = int(aparty.pace/.5)
    while q in range(dl):
        aparty.location+=1
        aparty.save()
        if searchStore(partyid):
            astore = Store.objects.get(location = aparty.location)
            aparty.stopmsg = "You have arrived at %s, click on \"Store\" to browse the shop!" % astore.name
            aparty.save()
            return
        if searchEvent(partyid):
            ev = Event.objects.get(location = aparty.location)
            evname = ev.name
            evtype = ev.etype
            aparty.stopmsg = ev.text()
            aparty.save()



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

