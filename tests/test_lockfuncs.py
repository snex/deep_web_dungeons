""" test lockfuncs """

from unittest.mock import Mock
from unittest.mock import patch

from evennia.utils.create import create_object
from evennia.utils.test_resources import EvenniaTest

from server.conf.lockfuncs import (
    in_combat,
    in_range,
    melee_equipped,
    ranged_equipped,
    not_in_foreign_backpack,
    character_can_equip_item,
)
from typeclasses.objects import WeaponObject
from world.characters.classes import CHARACTER_CLASSES
from world.combat import CombatHandler
from world.enums import CombatRange, WieldLocation

class LockfuncsTest(EvenniaTest):
    """ test our lockfuncs """

    def setUp(self):
        super().setUp()
        self.dummy = Mock(spec=int)

    def test_in_combat(self):
        """ test the in_combat lockfunc """

        self.assertFalse(in_combat(self.dummy, None))

        self.assertFalse(in_combat(self.char1, None))

        self.char1.nattributes.add("combat", True)
        self.assertTrue(in_combat(self.char1, None))

    @patch("world.combat.CombatHandler.any_in_range")
    def test_in_range(self, mock_any_in_range):
        """ test the in_range lockfunc """

        self.assertFalse(in_range(self.dummy, None))

        self.assertFalse(in_range(self.char1, None))

        ch = CombatHandler(self.char1, self.char2)
        self.char1.nattributes.add("combat", True)
        self.char1.ndb.combat = ch

        mock_any_in_range.return_value = False
        self.assertFalse(in_range(self.char1, None))

        mock_any_in_range.return_value = True
        self.assertTrue(in_range(self.char1, None))

    def test_melee_equipped(self):
        """ test the melee_equipped lockfunc """

        self.assertFalse(melee_equipped(self.dummy, None))

        weapon = create_object(WeaponObject, key="weapon")
        weapon.attack_range = CombatRange.REACH
        self.char1.equipment.move(weapon)
        self.assertFalse(melee_equipped(self.char1, None))

        weapon.attack_range = CombatRange.MELEE
        self.assertTrue(melee_equipped(self.char1, None))

    def test_ranged_equipped(self):
        """ test the range_equipped lockfunc """

        self.assertFalse(ranged_equipped(self.dummy, None))

        weapon = create_object(WeaponObject, key="weapon")
        weapon.attack_range = CombatRange.REACH
        self.char1.equipment.move(weapon)
        self.assertFalse(ranged_equipped(self.char1, None))

        weapon.attack_range = CombatRange.LONG_RANGE
        self.assertTrue(ranged_equipped(self.char1, None))

    def test_not_in_foreign_backpack(self):
        """ test the in_foreign_backpack lockfunc """

        weapon = create_object(WeaponObject, key="weapon")
        weapon.move_to(self.char1, quiet=True, move_type="get")
        self.char1.equipment.add(weapon)

        self.assertTrue(not_in_foreign_backpack(self.char1, weapon))
        self.assertFalse(not_in_foreign_backpack(self.char2, weapon))

        weapon2 = create_object(WeaponObject, key="weapon")
        self.assertTrue(not_in_foreign_backpack(self.char1, weapon2))
        self.assertTrue(not_in_foreign_backpack(self.char2, weapon2))

        weapon2.move_to(self.char2, quiet=True, move_type="get")
        self.char2.equipment.move(weapon2)
        self.assertTrue(not_in_foreign_backpack(self.char1, weapon2))
        self.assertTrue(not_in_foreign_backpack(self.char2, weapon2))

    def test_character_can_equip_item(self):
        """
        test that a character can equip an item based on their character class and level
        """

        trash = create_object(WeaponObject, key="weapon")
        self.assertFalse(character_can_equip_item(self.char1, trash))
        trash = create_object(WeaponObject, key="weapon", attributes=[("required_level", 0)])
        self.assertFalse(character_can_equip_item(self.char1, trash))
        weapon = create_object(
            WeaponObject,
            key="weapon",
            attributes=[
                ("inventory_use_slot", WieldLocation.WEAPON_HAND),
                ("allowed_classes", [CHARACTER_CLASSES["antifa_rioter"]]),
                ("required_level", 5),
            ],
        )
        self.assertFalse(character_can_equip_item(weapon, weapon))
        self.char1.ndb.cclass = CHARACTER_CLASSES["antifa_rioter"]
        self.char1.levels.level = 5
        self.char1.save()
        self.assertTrue(character_can_equip_item(self.char1, weapon))
        self.char1.ndb.cclass = CHARACTER_CLASSES["hacker"]
        self.char1.levels.level = 5
        self.char1.save()
        self.assertFalse(character_can_equip_item(self.char1, weapon))
        self.char1.ndb.cclass = CHARACTER_CLASSES["antifa_rioter"]
        self.char1.levels.level = 5
        self.char1.save()
        self.assertTrue(character_can_equip_item(self.char1, weapon))
        self.char1.ndb.cclass = CHARACTER_CLASSES["antifa_rioter"]
        self.char1.levels.level = 4
        self.char1.save()
        self.assertFalse(character_can_equip_item(self.char1, weapon))
