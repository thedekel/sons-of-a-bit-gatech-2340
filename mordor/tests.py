from django.utils import unittest
from mordor.models import *
from mordor.functions import *

class CharaterTestCase(unittest.TestCase):
    def setUp(self):
        self.party = Party(name="testParty")
        self.defaultChar = Character(party=self.party)
        self.aliveChar = Character(name="test", profession="Benjamin", status=1,health=1, isLeader=False, party=self.party)
        self.deadChar = Character(name="test2", profession="hammers", status=0, health=0, isLeader=False, party=self.party)

    def testCheckIfDead(self):
        self.assertEqual(self.defaultChar.checkIfDead(), False)
        self.assertEqual(self.aliveChar.checkIfDead(), False)
        self.assertEqual(self.deadChar.checkIfDead(), True)


