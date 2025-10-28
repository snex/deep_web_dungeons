""" test generating insults """

from evennia.utils.test_resources import EvenniaTest

from world.common.dialog.ads import Advertisement
from world.common.dialog.insults import Insult

class Testadvertisement(EvenniaTest):
    """ test generating advertisements """

    def test_generate_advertisement(self):
        """ test that we get a string """
        self.assertTrue(Advertisement(self.char1).generate_advertisement())

class TestInsult(EvenniaTest):
    """ test generating insults """

    def test_generate_insult(self):
        """ test that we get a string """
        self.assertTrue(Insult(self.char1).generate_insult())
