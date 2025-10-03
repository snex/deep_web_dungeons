"""
Test the equipment handler.

"""


from unittest.mock import MagicMock, patch

from parameterized import parameterized

from evennia.utils.test_resources import EvenniaTest

from world.enums import Ability, WieldLocation
from world.equipment import EquipmentError
from .mixins import AinneveTestMixin


class TestEquipment(AinneveTestMixin, EvenniaTest):
    def test_count_slots(self):
        self.assertEqual(self.char1.equipment.count_slots(), 0)

    def test_max_slots(self):
        self.assertEqual(self.char1.equipment.max_slots, 11)
        setattr(self.char1, Ability.STR.value, 3)
        self.assertEqual(self.char1.equipment.max_slots, 13)

    def test_add__remove(self):
        self.char1.equipment.add(self.helmet)
        self.assertEqual(self.char1.equipment.slots[WieldLocation.BACKPACK], [self.helmet])
        self.char1.equipment.remove(self.helmet)
        self.assertEqual(self.char1.equipment.slots[WieldLocation.BACKPACK], [])

    def test_move__get_current_slot(self):
        self.char1.equipment.add(self.helmet)
        self.assertEqual(
            self.char1.equipment.get_current_slot(self.helmet), WieldLocation.BACKPACK
        )
        self.char1.equipment.move(self.helmet)
        self.assertEqual(self.char1.equipment.get_current_slot(self.helmet), WieldLocation.HEAD)

    def test_get_wearable_or_wieldable_objects_from_backpack(self):
        self.char1.equipment.add(self.helmet)
        self.char1.equipment.add(self.weapon)

        self.assertEqual(
            self.char1.equipment.get_wieldable_objects_from_backpack(), [self.weapon]
        )
        self.assertEqual(
            self.char1.equipment.get_wearable_objects_from_backpack(), [self.helmet]
        )

        self.assertEqual(
            self.char1.equipment.all(),
            [
                (None, WieldLocation.WEAPON_HAND),
                (None, WieldLocation.SHIELD_HAND),
                (None, WieldLocation.TWO_HANDS),
                (None, WieldLocation.BODY),
                (None, WieldLocation.HEAD),
                (self.helmet, WieldLocation.BACKPACK),
                (self.weapon, WieldLocation.BACKPACK),
            ],
        )

    def _get_empty_slots(self):
        return {
            WieldLocation.BACKPACK: [],
            WieldLocation.WEAPON_HAND: None,
            WieldLocation.SHIELD_HAND: None,
            WieldLocation.TWO_HANDS: None,
            WieldLocation.BODY: None,
            WieldLocation.HEAD: None,
        }

    def test_equipmenthandler_max_slots(self):
        self.assertEqual(self.char1.equipment.max_slots, 11)

    @parameterized.expand(
        [
            # size, pass_validation?
            (1, True),
            (2, True),
            (11, True),
            (12, False),
            (20, False),
            (25, False),
        ]
    )
    def test_validate_slot_usage(self, size, is_ok):
        obj = MagicMock()
        obj.size = size

        with patch("world.equipment.inherits_from") as mock_inherit:
            mock_inherit.return_value = True
            if is_ok:
                self.assertTrue(self.char1.equipment.validate_slot_usage(obj))
            else:
                with self.assertRaises(EquipmentError):
                    self.char1.equipment.validate_slot_usage(obj)

    def test_display_loadout(self):
        self.assertEqual(
            self.char1.equipment.display_loadout(),
            "You are fighting with your bare fists and have no shield.\n"
            "You wear no armor and no helmet."
        )
        self.char1.equipment.move(self.weapon)
        self.char1.equipment.move(self.shield)
        self.char1.equipment.move(self.armor)
        self.char1.equipment.move(self.helmet)
        self.assertEqual(
            self.char1.equipment.display_loadout(),
            "You are wielding weapon in one hand. You have shield in your off hand.\n"
            "You are wearing armor and helmet on your head."
        )
        self.char1.equipment.move(self.big_weapon)
        self.assertEqual(
            self.char1.equipment.display_loadout(),
            "You wield big_weapon with both hands.\n"
            "You are wearing armor and helmet on your head."
        )

    def test_display_backpack(self):
        self.assertEqual(
            self.char1.equipment.display_backpack(),
            "Backpack is empty."
        )
        self.char1.equipment.move(self.item)
        self.char1.equipment.move(self.item2)
        self.assertEqual(
            self.char1.equipment.display_backpack(),
            "backpack item [|b1|n] slot(s)\n"
            "backpack item 2 [|b5|n] slot(s)"
        )

    def test_display_slot_usage(self):
        self.assertEqual(
            self.char1.equipment.display_slot_usage(),
            "|b0/11|n"
        )
        self.char1.equipment.move(self.item)
        self.assertEqual(
            self.char1.equipment.display_slot_usage(),
            "|b1/11|n"
        )

    @parameterized.expand(
        [
            # item, where
            ("helmet", WieldLocation.HEAD),
            ("shield", WieldLocation.SHIELD_HAND),
            ("armor", WieldLocation.BODY),
            ("weapon", WieldLocation.WEAPON_HAND),
            ("big_weapon", WieldLocation.TWO_HANDS),
            ("item", WieldLocation.BACKPACK),
        ]
    )
    def test_move(self, itemname, where):
        self.assertEqual(self.char1.equipment.slots, self._get_empty_slots())

        obj = getattr(self, itemname)
        self.char1.equipment.move(obj)
        # check that item ended up in the right place
        if where is WieldLocation.BACKPACK:
            self.assertTrue(obj in self.char1.equipment.slots[where])
        else:
            self.assertEqual(self.char1.equipment.slots[where], obj)

    def test_add(self):
        self.char1.equipment.add(self.weapon)
        self.assertEqual(self.char1.equipment.slots[WieldLocation.WEAPON_HAND], None)
        self.assertTrue(self.weapon in self.char1.equipment.slots[WieldLocation.BACKPACK])

    def test_two_handed_exclusive(self):
        """Two-handed weapons can't be used together with weapon+shield"""
        self.char1.equipment.move(self.big_weapon)
        self.assertEqual(self.char1.equipment.slots[WieldLocation.TWO_HANDS], self.big_weapon)
        # equipping sword or shield removes two-hander
        self.char1.equipment.move(self.shield)
        self.assertEqual(self.char1.equipment.slots[WieldLocation.SHIELD_HAND], self.shield)
        self.assertEqual(self.char1.equipment.slots[WieldLocation.TWO_HANDS], None)
        self.char1.equipment.move(self.weapon)
        self.assertEqual(self.char1.equipment.slots[WieldLocation.WEAPON_HAND], self.weapon)

        # the two-hander removes the two weapons
        self.char1.equipment.move(self.big_weapon)
        self.assertEqual(self.char1.equipment.slots[WieldLocation.TWO_HANDS], self.big_weapon)
        self.assertEqual(self.char1.equipment.slots[WieldLocation.SHIELD_HAND], None)
        self.assertEqual(self.char1.equipment.slots[WieldLocation.WEAPON_HAND], None)

    def test_remove__with_obj(self):
        self.char1.equipment.move(self.shield)
        self.char1.equipment.move(self.item)
        self.char1.equipment.add(self.weapon)

        self.assertEqual(self.char1.equipment.slots[WieldLocation.SHIELD_HAND], self.shield)
        self.assertEqual(
            self.char1.equipment.slots[WieldLocation.BACKPACK], [self.item, self.weapon]
        )

        self.assertEqual(self.char1.equipment.remove(self.shield), [self.shield])
        self.assertEqual(self.char1.equipment.remove(self.item), [self.item])

        self.assertEqual(self.char1.equipment.slots[WieldLocation.SHIELD_HAND], None)
        self.assertEqual(self.char1.equipment.slots[WieldLocation.BACKPACK], [self.weapon])

    def test_remove__with_slot(self):
        self.char1.equipment.move(self.shield)
        self.char1.equipment.move(self.item)
        self.char1.equipment.add(self.helmet)

        self.assertEqual(self.char1.equipment.slots[WieldLocation.SHIELD_HAND], self.shield)
        self.assertEqual(
            self.char1.equipment.slots[WieldLocation.BACKPACK], [self.item, self.helmet]
        )

        self.assertEqual(self.char1.equipment.remove(WieldLocation.SHIELD_HAND), [self.shield])
        self.assertEqual(
            self.char1.equipment.remove(WieldLocation.BACKPACK), [self.item, self.helmet]
        )

        self.assertEqual(self.char1.equipment.slots[WieldLocation.SHIELD_HAND], None)
        self.assertEqual(self.char1.equipment.slots[WieldLocation.BACKPACK], [])

    def test_properties(self):
        self.char1.equipment.move(self.armor)
        self.assertEqual(self.char1.equipment.armor, 1)
        self.char1.equipment.move(self.shield)
        self.assertEqual(self.char1.equipment.armor, 2)
        self.char1.equipment.move(self.helmet)
        self.assertEqual(self.char1.equipment.armor, 3)

        self.char1.equipment.move(self.weapon)
        self.assertEqual(self.char1.equipment.weapon, self.weapon)
        self.char1.equipment.move(self.big_weapon)
        self.assertEqual(self.char1.equipment.weapon, self.big_weapon)
