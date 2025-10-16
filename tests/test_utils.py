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

    def test_each_cons(self):
        """ test each_cons """

        l = [1, 2, 3, 4]
        self.assertEqual(
            utils.each_cons(l, 2),
            [[1, 2], [2, 3], [3, 4]]
        )
        self.assertEqual(
            utils.each_cons(l, 3),
            [[1, 2, 3], [2, 3, 4]]
        )

    def test_each_slice(self):
        """ test each_slice """

        l = [1, 2, 3, 4, 5, 6]
        self.assertEqual(
            list(utils.each_slice(l, 2)),
            [[1, 2], [3, 4], [5, 6]]
        )
        self.assertEqual(
            list(utils.each_slice(l, 3)),
            [[1, 2, 3], [4, 5, 6]]
        )

    def test_list_flatten(self):
        """ test list_flatten """

        l = [[1, 2], [3, 4], [5, 6]]
        self.assertEqual(
            utils.list_flatten(l),
            [1, 2, 3, 4, 5, 6]
        )

    def test_rainbow(self):
        """ test rainbow effect on text """

        self.assertEqual(
            utils.rainbow("rainbow!"),
            "|rr|530a|yi|gn|bb|co|mw|r!|n"
        )
