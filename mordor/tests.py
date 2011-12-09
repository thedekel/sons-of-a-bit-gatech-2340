from django.utils import unittest
from mordor.models import *
from mordor.functions import *

class CharacterTestCase(unittest.TestCase):
    def setUp(self):
        self.party = Party(name="testParty")
        self.defaultChar = Character(party=self.party)
        self.aliveChar = Character(name="test", profession="Benjamin", status=1,health=1, isLeader=False, party=self.party)
        self.deadChar = Character(name="test2", profession="hammers", status=0, health=0, isLeader=False, party=self.party)

    def testCheckIfDead(self):
        """
        Dekel
        """
        self.assertEqual(self.defaultChar.checkIfDead(), False)
        self.assertEqual(self.aliveChar.checkIfDead(), False)
        self.assertEqual(self.deadChar.checkIfDead(), True)

class WagonTestCase(unittest.TestCase):
    def setUp(self):
        self.party = Party(name="testPartyWagon")
        self.wagon = Wagon(party=self.party) #capacity initially 500
        self.anorexic = Item(name = "Feather",description = "Can fit in the wagon easily",weight = 1)
        self.obese = Item("Lard", "Bigger than the wagon capacity",weight = 501)
        self.nonexistent = Item("Nothing", weight = -1)
        self.alottaNothing = Item("NOTHINGNESS", weight= -501)

    def testCheckWagCap(self):
        """
        Roca
        """
        self.assertTrue(self.wagon.checkWagCap(self.anorexic,50))
        self.assertFalse(self.wagon.checkWagCap(self.obese,1))
        self.assertFalse(self.wagon.checkWagCap(self.nonexistent,50))
        self.assertFalse(self.wagon.checkWagCap(self.alottaNothing,1))

class FunctionsTestCase(unittest.TestCase):
    def setUp(self):
        self.party = Party(name="testPartyEvent")
        self.party.save()
        self.event = Event(name="testEvent", location=25)
        self.event.save()
        self.store = Store(name="testStore", location=26)
        self.store.save()

    def tearDown(self):
        #Party.objects.all().delete()
        Store.objects.all().delete()

    def testSearchEvent(self):
        """
        Taormina
        """
        self.assertFalse(searchEvent(self.party.id))
        self.party.location = 25
        self.party.save()
        self.assertTrue(searchEvent(self.party.id))

    def testSearchStore(self):
        """
        Williams
        """
        self.assertFalse(searchStore(self.party.id))
        self.party.location = self.store.location = 26
        self.party.save()
        self.store.save()
        self.assertTrue(searchStore(self.party.id))

class RemoveItemTestCase(unittest.TestCase):
    def setUp(self):
        self.party = Party(name="testPartyWagon")
        self.party.save()
        self.wagon = Wagon(party=self.party) #capacity initially 500
        self.wagon.save()
        self.anorexic = Item(name = "Feather",description = "Can fit in the wagon easily",weight = 1)
        self.anorexic.save()
        self.obese = Item(name = "Lard", description = "Bigger than the wagon capacity",weight = 501)
        self.obese.save()
        self.nonexistent = Item(name = "Nothing",description='oeu', weight = -1)
        self.nonexistent.save()
        self.inventory = Inventory(wagon = self.wagon)
        self.inventory.save()
        self.iteminstance = Iteminstance(base = self.anorexic, inventory = self.inventory)
        self.iteminstance2 = Iteminstance(base = self.obese, inventory = self.inventory)
        self.iteminstance3 = Iteminstance(base = self.nonexistent, inventory = self.inventory)
        self.iteminstance.save()
        self.iteminstance2.save()
        self.iteminstance3.save()
    
    def testRemoveItem(self):
        """
        Whatley
        """
        self.assertTrue(self.inventory.removeItem("Feather", 1))
        self.assertTrue(self.inventory.removeItem("Lard", 1))
        self.assertFalse(self.inventory.removeItem("Lard", 1))
        self.assertTrue(self.inventory.removeItem("Nothing", 1))
        
