from models import *
from coords import *
from views  import *
import random

def takeATurn(partyid):
    """
    This takes a turn.  Shocking, no?
    """
    party = Party.objects.get(id = partyid)
    if not party.consumeFood():
        stuck(partyid, "Your party is out of food and cannot proceed")
        return 'stuck'
    return moveLocation(partyid)

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
    if (wag.weight + abase.weight * num > wag.capacity):
        aparty.stopmsg = "You can't buy these items; they're too heavy!"
        aparty.save()
        return
    inv = Inventory.objects.get(wagon = wag)
    if itemName in map(lambda q: q.base.name, inv.iteminstance_set.all()):
        ii = inv.iteminstance_set.get(base = abase)
        ii.amount += num
        aparty.money-=num*mult*abase.baseCost
        ii.save()
        aparty.stopmsg += "\nSuccessfully added %d items of type %s" %(num, itemName)
        aparty.save()
    else:
        ii = Iteminstance(base = abase, amount = num, inventory = inv)
        ii.save()
        aparty.money-=num*mult*abase.baseCost
        wag.weight += abase.weight * num
        wag.save()
        aparty.stopmsg += "\nSuccessfully purchased %d items of type %s" %(num, itemName)
        aparty.save()
    return

def searchStore(pid):
    aparty = Party.objects.get(id=pid)
    try:
        Store.objects.get(location=int(aparty.location))
        return True
    except:
        return False
    return False

def searchEvent(pid):
    aparty = Party.objects.get(id=pid)
    try:
        Event.objects.get(location=aparty.location)
        return True
    except:
        return False
    return False

def determineEv(e, p):
    w = Wagon.objects.get(party = p)
    i = Inventory.objects.get(wagon = w) 
    a=5
    #River
    if e.etype==0:
        p.stopmsg = "River"
        p.save()
    #Battle
    elif e.etype==1:
        if i.itemCount("Swords") >= p.numAlive():
            # if number of swords is >= number of party members, lose 1 sword
            p.stopmsg = "You encountered some Orcs. After a fierce battle, all party members survived, but one Sword broke."
            i.removeItem("Swords", 1)
        elif i.itemCount("Swords") < p.numAlive() and p.numAlive > 1:
            # if not enough swords, a person dies...
            qq = p.kill()
            p.money = p.money*2/3.
            p.stopmsg = "You encountered some Orcs. After a fierce battle, party member '" + qq + "' died. You lost a third of your money to looters."
        else:
            # if anything else, you died
            p.stopmsg = 'death'
            p.killall()
        p.save()
        return
    #Wagon Breaks
    elif e.etype==2:
        if i.itemCount("Supplies") >= 1:
            p.stopmsg = "The Wagon broke, but you had the supplies to fix it. Lost 1 Supply package"
        else:
            p.stopmsg = "broken"
            p.killall()
        p.save()
        return
    #Balrog
    elif e.etype==3 and __import__("random").random()>.75:
        if i.itemCount("Gandalf") >= 1:
            p.stopmsg = "You encountered a Balrog, but a Gandalf in your inventory took care of it."
            i.removeItem("Gandalf", 1)
        else:
            p.stopmsg = "balrog"
            p.killall()
        p.save()
    #dysentery
    elif e.etype==4:
        if __import__('random').random()>.95:
            qq = p.kill()
            if qq:
                p.stopmsg = "Party Member '" + qq + "' died of dysentery."
            else:
                p.killall()
                p.stopmsg = "death"
            p.save()
        return
    #Mordor
    elif e.etype==99 or p.location>=130:
        p.stopmsg = "You reach the border of Mordor. You are preparing to enter your final destination and... you die of dysentery. One does not simply walk into Mordor.<br />"
        p.name+="--DONE--"
        p.save()
    return 'stuck'
       
       
       


def moveLocation(partyid): #int
    """
    Moves along the map array to "change" location.
    Any locations that would force a halt will be checked for here (representing with a boolean field in Location, will change later to something else)
    Most of these parameters probably won't be need1gT
    -Anthony Taormina
    """
    aparty = Party.objects.get(id = partyid)
    dl = int(aparty.pace/.5)
    for q in range(dl):
        aparty.location+=1;
        aparty.save()
        if aparty.location>=130:
            aparty.location=130;
            aparty.save()
        if searchStore(partyid):
            astore = Store.objects.get(location = aparty.location)
            aparty.stopmsg = "You have arrived at %s, click on \"Shop\" to browse the shop!" % astore.name
            aparty.save()
            return 'stuck'
        if searchEvent(partyid):
            print "Found Event"
            ev = Event.objects.get(location = aparty.location)
            evname = ev.name
            evtype = ev.etype
            return determineEv(ev, aparty)
        if random.random()>.5:
            ev = Event(location = aparty.location, etype = random.choice(range(1,5)), name="gazeeng")
            return determineEv(ev,aparty)

    return

def takeFerry(partyid): #string
    """
    Takes the Ferry. Takes a designated amount of money away from the player
    to use the ferry
    """
    aparty = Party.objects.get(id=partyid)
    party.money -= 250
    party.stopmsg = "You paid 250 gold to cross the bridge"
    party.save()
    return
    
def ford():
    """
    Attempts to ford the river. Fails if water depth is greater than 3 feet.
    @return: String: The success or failure of fording the river
    """ 
    aparty = Party.objects.get(id=partyid)
    chance = random.randint(0,100)
    percentChance = 5 * 2
    if (chance > (100 - percentChance)):
        aparty.stopmsg = "You failed to ford the river!"
        aparty.save()
        return
    aparty.stopmsg = "You successfully forded the river!"
    aparty.save()
    return 

def caulk():
    """
    Attempts to float over the river on the wagon. Greater chance of wagon flip.
    @return: String: The success or failure of caulking the river
    """
    aparty = Party.objects.get(id=partyid)
    chance = random.randint(0,100)
    if (chance > 70):
        aparty.stopmsg = "You couldn't float over the river"
        aparty.stop()
        return 
    aparty.stopmsg = "You managed to float over the river"
    aparty.stop()
    return 

