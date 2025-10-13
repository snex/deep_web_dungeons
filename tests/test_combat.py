"""
Test combat handler..

"""

from evennia.utils.create import create_object
from evennia.utils.test_resources import EvenniaTest, EvenniaCommandTest
from typeclasses.mobs.mob import BaseMob
from world.combat import CombatHandler
from world.enums import CombatRange

from commands import combat
from .mixins import AinneveTestMixin


class TestCombatHandler(AinneveTestMixin, EvenniaTest):
    """ Test CombatHandler. """
    def setUp(self):
        super().setUp()
        self.combat = CombatHandler(self.char1, self.char2)
        self.combat.positions[self.char1] = 1
        self.combat.positions[self.char2] = 2

    def test_add_remove(self):
        """ Test add to and remove from combat. """
        target = create_object(BaseMob, key="rat", location=self.room1)
        self.combat.add(target)
        self.assertTrue(target in self.combat.positions)
        self.combat.remove(target)
        self.assertFalse(target in self.combat.positions)

    def test_approach(self):
        """ Test approaching. """
        self.combat.approach(self.char1, self.char2)
        self.assertEqual(
            self.combat.positions[self.char1], self.combat.positions[self.char2]
        )
        self.assertFalse(self.combat.approach(self.char1, self.char2))

    def test_retreat(self):
        """ Test retreating. """
        # retreating negative
        self.combat.retreat(self.char1, self.char2)
        self.assertEqual(self.combat.positions[self.char1], 0)
        self.assertEqual(self.combat.positions[self.char2], 2)
        # retreating positive
        self.combat.retreat(self.char2, self.char1)
        self.assertEqual(self.combat.positions[self.char1], 0)
        self.assertEqual(self.combat.positions[self.char2], 3)

    def test_in_range(self):
        """ Test if a specific combatant is in range. """
        self.assertTrue(self.combat.in_range(self.char1, self.char2, CombatRange.MELEE))
        self.combat.positions[self.char2] = 5
        self.assertFalse(self.combat.in_range(self.char1, self.char2, CombatRange.MELEE))
        self.assertTrue(self.combat.in_range(self.char1, self.char2, CombatRange.LONG_RANGE))

    def test_any_in_range(self):
        """ Test if any combatants are in range. """
        self.assertTrue(self.combat.any_in_range(self.char1, CombatRange.MELEE))
        self.combat.positions[self.char2] = 5
        self.assertFalse(self.combat.any_in_range(self.char1, CombatRange.MELEE))
        self.assertTrue(self.combat.any_in_range(self.char1, CombatRange.LONG_RANGE))

    def test_get_range(self):
        """ Test get combat range. """
        self.assertEqual(self.combat.get_range(self.char1, self.char2), CombatRange.MELEE)
        self.combat.positions[self.char2] = 5
        self.assertEqual(self.combat.get_range(self.char1, self.char2), CombatRange.MEDIUM_RANGE)


class TestCombatCommands(AinneveTestMixin, EvenniaCommandTest):
    """ Test Combat Commands. """
    def setUp(self):
        super().setUp()
        self.target = create_object(BaseMob, key="rat", location=self.room1)
        # make sure the rat won't die in our tests
        self.target.hp_max = self.target.hp = 9999

    def tearDown(self):
        super().tearDown()
        if self.target.dbid:
            self.target.delete()

    def test_engage(self):
        """ Test combat engage. """
        self.call(
            combat.CmdInitiateCombat(),
            "rat",
            "You prepare for combat! rat is at melee range.",
        )
        self.assertEqual(self.char1.ndb.combat, self.target.ndb.combat)

        self.call(
            combat.CmdInitiateCombat(),
            "char2",
            "You can't attack another player here.",
        )
        self.call(
            combat.CmdInitiateCombat(),
            "obj",
            "Invalid target.",
        )

    def test_hit(self):
        """ Test combat hit command. """
        self.char1.strength = 100 # guarantee a hit
        combat_instance = CombatHandler(self.char1, self.target)
        combat_instance.positions[self.target] = CombatRange.LONG_RANGE
        self.call(
            combat.CmdHit(),
            "rat",
            "rat is too far away.",
        )
        combat_instance.positions[self.target] = CombatRange.MELEE
        self.call(
            combat.CmdHit(),
            "rat",
            "You hit rat with your Bare Hands",
        )
        self.char1.cooldowns.clear()

    def test_shoot(self):
        """ Test combat shoot command. """
        self.char1.strength = 100 # guarantee a hit
        CombatHandler(self.char1, self.target)
        self.weapon.attack_range = CombatRange.LONG_RANGE
        self.weapon.location = self.char1
        self.char1.equipment.move(self.weapon)
        self.call(
            combat.CmdShoot(),
            "rat",
            "You shoot rat with your weapon",
        )
        self.char1.cooldowns.clear()

    def test_flee(self):
        """ Test combat flee command. """
        CombatHandler(self.char1, self.target)
        self.assertTrue(self.char1.combat)
        self.assertTrue(self.target.combat)
        self.call(
            combat.CmdFlee(),
            "",
            "You flee!",
        )
        self.assertFalse(self.char1.combat)
        self.assertFalse(self.target.combat)
        self.assertEqual(self.char1.location, self.room2)
