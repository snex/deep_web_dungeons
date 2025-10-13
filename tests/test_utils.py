"""
Tests of the utils module.

"""

from evennia.utils import create
from evennia.utils.test_resources import EvenniaTest

from world import utils
from typeclasses.objects import Object


class TestUtils(EvenniaTest):
    """ test utils """
    def test_get_obj_stats(self):
        """ test get_obj_stats """

        obj = create.create_object(
            Object, key="testobj", attributes=(("desc", "A test object"),)
        )
        result = utils.get_obj_stats(obj)

        self.assertEqual(
            result,
            """
testobj

A test object

Slots: |w1|n, Used from: |wbackpack|n
Quality: |wN/A|n, Uses: |wN/A|n
Attacks using |wNo attack|n against |wNo defense|n
""",
        )
