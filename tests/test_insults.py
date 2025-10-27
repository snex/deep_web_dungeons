""" test generating insults """

from evennia.utils.test_resources import BaseEvenniaTest

from world.common.dialog.insults import Insult

class TestInsult(BaseEvenniaTest):
    """ test generating insults """

    def test_generate_insult(self):
        """ test that we get a string """
        self.assertTrue(Insult("snex", "male").generate_insult())
