"""
Tests of the utils module.

"""

from evennia.utils import create
from evennia.utils.ansi import strip_ansi
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
        expected_output = strip_ansi("""
+------------------------------------------------------------------------------+
|                                                                              |
|                                                                              |
|                                   testobj                                    |
|                                A test object                                 |
|                                                                              |
+------------------------------------------------------------------------------+
|                                                                              |
|  Weight:           1                                    --                   |
|  Quality:          Perfect                                                   |
|                                                                              |
|                                                                              |
|                                                                              |
|                                                                              |
|                                                                              |
|                                                                              |
|                                                                              |
|                                                                              |
|                                                                              |
|                                                                              |
|                                                                              |
|                                                                              |
|                                                                              |
+------------------------------------------------------------------------------+
""").strip()
        result = strip_ansi(utils.get_obj_stats(obj)).strip()

        self.assertEqual(result, expected_output)

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
