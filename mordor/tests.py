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

    def testSearchEvent(self):
        self.assertFalse(searchEvent(self.party.id))
        self.party.location = 25
        self.party.save()
        self.assertTrue(searchEvent(self.party.id))

    def testSearchStore(self):
        self.party.location = self.store.location = 888

        self.party.save()
        self.assertTrue(searchStore(self.party.id))
        self.party.location = 26
        self.store.location = 9876
        self.party.save()
        self.assertTrue(searchStore(self.party.id))

class RemoveItemTestCase(unittest.TestCase):
    def setUp(self):
        self.party = Party(name="testPartyWagon")
        self.wagon = Wagon(party=self.party) #capacity initially 500
        self.anorexic = Item(name = "Feather",description = "Can fit in the wagon easily",weight = 1)
        self.obese = Item("Lard", "Bigger than the wagon capacity",weight = 501)
        self.nonexistent = Item("Nothing", weight = -1)
    
    def testRemoveItem(self):
        self.assertTrue(self.inventory.removeItem("Feather", 1))
        self.assertTrue(self.inventory.removeItem("Lard", 1))
        self.assertFalse(self.inventory.removeItem("Lard", 1))
        self.assertTrue(self.inventory.removeItem("Nothing", 1))
        
