"""
test the item spawner
"""

from unittest.mock import PropertyMock
from unittest.mock import patch

from evennia.utils.test_resources import BaseEvenniaTest

import world
from world.item_spawner import ItemSpawner, PrototypeManager

DROPPABLE_1 = {
    "prototype_key": "droppable_1",
    "typeclass": "typeclasses.DroppableOne",
    "prototype_tags": ["1", "droppable_1"],
    "attrs": [],
}
DROPPABLE_2 = {
    "prototype_key": "droppable_2",
    "typeclass": "typeclasses.DroppableTwo",
    "prototype_tags": ["2"],
    "attrs": [("materials", "junk")],
}
DROPPABLE_3 = {
    "prototype_key": "droppable_3",
    "typeclass": "typeclasses.DroppableThree",
    "prototype_tags": ["3"],
    "attrs": [
        ("required_level", 10),
        ("materials", "stuff"),
        ("tier", 1),
    ],
}
TEST_DROPPABLES = [
    DROPPABLE_1,
    DROPPABLE_2,
    DROPPABLE_3,
]

ROLLABLE_1 = {
    "prototype_key": "rollable_1",
    "prototype_tags": ["1", "affix", "typeclasses.DroppableOne", "rollable_2"],
    "attrs": [],
}
ROLLABLE_2 = {
    "prototype_key": "rollable_2",
    "prototype_tags": ["2", "affix", "typeclasses.DroppableOne", "rollable_1"],
    "attrs": [],
}
ROLLABLE_3 = {
    "prototype_key": "rollable_3",
    "prototype_tags": ["3", "stuff", "affix", "typeclasses.DroppableTwo"],
    "attrs": [
        ("required_level", 10),
    ],
}
ROLLABLE_4 = {
    "prototype_key": "rollable_4",
    "prototype_tags": ["4", "affix", "typeclasses.DroppableOne"],
    "attrs": [],
}
TEST_ROLLABLES = [
    ROLLABLE_1,
    ROLLABLE_2,
    ROLLABLE_3,
    ROLLABLE_4,
]
TEST_DROP_TABLES = {
    "generic": [
        ("cclass", 1),
    ],
    "cclass": [
        ("stuff", 1),
        ("junk",  1),
    ],
    "stuff": [
        ("droppable_1", 1),
        ("droppable_2", 1),
        ("droppable_3", 1),
    ],
    "tiers": [
        ("tier_1", 1),
        ("tier_2", 1),
    ],
    "affixes": [
        ("rollable_1", 1),
        ("rollable_2", 1),
        ("rollable_3", 1),
        ("rollable_4", 1),
    ],
}

class BaseItemSpawnerTest(BaseEvenniaTest):
    """ shared setUp and tearDown for item spawner classes """
    def setUp(self):
        super().setUp()
        self.all_droppables_patcher = patch(
            "world.item_spawner.PrototypeManager._all_droppables",
            new_callable=PropertyMock
        )
        self.mock_all_droppables = self.all_droppables_patcher.start()
        self.mock_all_droppables.return_value = TEST_DROPPABLES
        self.all_rollables_patcher = patch(
            "world.item_spawner.PrototypeManager._all_rollables",
            new_callable=PropertyMock
        )
        self.mock_all_rollables = self.all_rollables_patcher.start()
        self.mock_all_rollables.return_value = TEST_ROLLABLES

    def tearDown(self):
        self.all_droppables_patcher.stop()
        self.all_rollables_patcher.stop()
        super().tearDown()

class PrototypeManagerTest(BaseItemSpawnerTest):
    """ test the PrototypeManager """

    def setUp(self):
        super().setUp()
        self.pm = PrototypeManager()

    def test_droppables(self):
        """ test get droppables """
        self.assertEqual(self.pm.droppables(), TEST_DROPPABLES)
        self.assertEqual(self.pm.droppables("1"), [DROPPABLE_1])
        self.assertEqual(self.pm.droppables("1", "2"), [DROPPABLE_1, DROPPABLE_2])
        self.assertEqual(self.pm.droppables("1", "2", must_include="2"), [DROPPABLE_2])
        self.assertEqual(self.pm.droppables(exclude="droppable_2"), [DROPPABLE_1, DROPPABLE_3])
        self.assertEqual(
            self.pm.droppables(exclude="typeclasses.DroppableTwo"),
            [DROPPABLE_1, DROPPABLE_3]
        )
        self.assertEqual(self.pm.droppables(exclude="2"), [DROPPABLE_1, DROPPABLE_3])

    def test_rollables(self):
        """ test get rollables """
        self.assertEqual(self.pm.rollables(), TEST_ROLLABLES)
        self.assertEqual(self.pm.rollables("1"), [ROLLABLE_1])
        self.assertEqual(self.pm.rollables("1", "2"), [ROLLABLE_1, ROLLABLE_2])
        self.assertEqual(self.pm.rollables("1", "2", must_include="2"), [ROLLABLE_2])
        self.assertEqual(self.pm.rollables(exclude="rollable_2"), [ROLLABLE_3, ROLLABLE_4])
        self.assertEqual(self.pm.rollables(exclude="2"), [ROLLABLE_1, ROLLABLE_3, ROLLABLE_4])

    def test_droppables_by_level(self):
        """ test droppables by level """
        self.assertEqual(self.pm.droppables_by_level(1), [DROPPABLE_1, DROPPABLE_2])
        self.assertEqual(self.pm.droppables_by_level(10), TEST_DROPPABLES)

    def test_rollables_by_level(self):
        """ test rollables by level """
        self.assertEqual(self.pm.rollables_by_level(1), [ROLLABLE_1, ROLLABLE_2, ROLLABLE_4])
        self.assertEqual(self.pm.rollables_by_level(10), TEST_ROLLABLES)

class ItemSpawnerTest(BaseItemSpawnerTest):
    """ test the ItemSpawner """

    def setUp(self):
        super().setUp()
        self.drop_tables_patcher = patch.object(world.item_spawner, "DROP_TABLES", TEST_DROP_TABLES)
        self.mock_drop_tables = self.drop_tables_patcher.start()
        self.randint_patcher = patch("random.randint")
        self.mock_randint = self.randint_patcher.start()
        self.search_prototype_patcher = patch("evennia.prototypes.spawner.search_prototype")
        self.mock_search_prototype = self.search_prototype_patcher.start()
        self.sp = ItemSpawner()

    def tearDown(self):
        self.drop_tables_patcher.stop()
        self.randint_patcher.stop()
        self.search_prototype_patcher.stop()
        super().tearDown()

    def test_roll_drop_table(self):
        """ test rolling from the drop table """
        self.mock_randint.return_value = 0
        self.assertEqual(self.sp.roll_drop_table(), "droppable_1")
        self.mock_randint.side_effect = [0, 3]
        self.assertEqual(self.sp.roll_drop_table(cclass="junk"), "junk")

    def test_roll_droppable(self):
        """ test rolling a base item """
        self.mock_randint.side_effect = [0, 0, 0]
        self.mock_search_prototype.return_value = [DROPPABLE_1]
        self.assertEqual(
            self.sp.roll_droppable(1),
            DROPPABLE_1 | {
                "prototype_desc": "",
                "prototype_locks": "spawn:all();edit:all()",
                "tags": [],
            }
        )
        self.mock_randint.side_effect = [0, 0, 0]
        self.mock_all_droppables.return_value = []
        self.assertIsNone(self.sp.roll_droppable(1), None)

    def test_roll_material(self):
        """ test rolling item material """
        self.assertEqual(self.sp.roll_material(DROPPABLE_1, 1), {})
        self.assertEqual(self.sp.roll_material(DROPPABLE_2, 1), {})
        self.assertEqual(self.sp.roll_material(DROPPABLE_3, 1), {})
        self.assertEqual(self.sp.roll_material(DROPPABLE_3, 10), ROLLABLE_3)

    def test_roll_tier(self):
        """ test rolling item tier """
        self.assertEqual(self.sp.roll_tier(DROPPABLE_1), 0)
        self.mock_randint.return_value = 2
        self.assertEqual(self.sp.roll_tier(DROPPABLE_3), "tier_2")

    def test_roll_affix(self):
        """ test rolling a single affix """
        self.mock_randint.side_effect = [1]
        self.assertEqual(self.sp.roll_affix(DROPPABLE_1, 1), "rollable_1")
        self.mock_randint.side_effect = [1, 4]
        self.assertEqual(self.sp.roll_affix(DROPPABLE_1, 1, ["rollable_1"]), "rollable_4")

    def test_roll_affixes(self):
        """ test rolling item affixes """
        self.assertEqual(self.sp.roll_affixes(DROPPABLE_1, 1, 1), [])
        self.mock_randint.side_effect = [4, 1, 4]
        self.assertEqual(self.sp.roll_affixes(DROPPABLE_1, 1, 4), ["rollable_1", "rollable_4"])
        self.mock_randint.side_effect = [1, 1, 4]
        self.assertEqual(self.sp.roll_affixes(DROPPABLE_1, 1, 4), ["rollable_1"])
