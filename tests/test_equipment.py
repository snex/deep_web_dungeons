"""
Test the equipment handler.

"""


from unittest.mock import MagicMock, patch

from parameterized import parameterized

from evennia.utils import create
from evennia.utils.test_resources import EvenniaTest

from typeclasses.objects import NoneObject, Object
from world.enums import Ability, WieldLocation
from world.equipment import EquipmentError
from .mixins import AinneveTestMixin


class TestEquipment(AinneveTestMixin, EvenniaTest):
    """ Test Equipment. """
    def test_count_slots(self):
        """ Test count slots. """
        self.assertEqual(self.char1.equipment.count_slots(), 0)

    def test_max_slots(self):
        """ Test max slots. """
        self.assertEqual(self.char1.equipment.max_slots, 11)
        setattr(self.char1, Ability.STR.value, 3)
        self.assertEqual(self.char1.equipment.max_slots, 13)

    def test_add__remove(self):
        """ Test add and remove. """
        self.char1.equipment.add(self.helmet)
        self.assertEqual(self.char1.equipment.backpack, [self.helmet])
        self.char1.equipment.remove(self.helmet)
        self.assertEqual(self.char1.equipment.backpack, [])

    def test_move__get_current_slot(self):
        """ Test move and get_current_slot. """
        self.char1.equipment.add(self.helmet)
        self.assertEqual(
            self.char1.equipment.get_current_slot(self.helmet), WieldLocation.BACKPACK
        )
        self.char1.equipment.move(self.helmet)
        self.assertEqual(self.char1.equipment.get_current_slot(self.helmet), WieldLocation.HEAD)

    def test_get_wearable_or_wieldable_objects_from_backpack(self):
        """ Tests listing wearable or wieldable items from backpack. """
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
                (NoneObject(), WieldLocation.WEAPON_HAND),
                (NoneObject(), WieldLocation.SHIELD_HAND),
                (NoneObject(), WieldLocation.TWO_HANDS),
                (NoneObject(), WieldLocation.BODY),
                (NoneObject(), WieldLocation.HEAD),
                (self.helmet, WieldLocation.BACKPACK),
                (self.weapon, WieldLocation.BACKPACK),
            ],
        )

    @patch("typeclasses.objects.Object.at_pre_use")
    def test_get_usable_objects_from_backpack(self, mock_at_pre_use):
        """ test getting usable items from backpack """
        mock_at_pre_use.side_effect = [True, False]
        self.char1.equipment.add(self.item)
        self.char1.equipment.add(self.weapon)
        self.assertEqual([self.item], self.char1.equipment.get_usable_objects_from_backpack())

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
        """ Test validating slot usage. """
        obj = MagicMock()
        obj.size = size

        with patch("world.equipment.inherits_from") as mock_inherit:
            mock_inherit.return_value = False
            with self.assertRaisesRegex(EquipmentError, "not something that can be equipped"):
                self.char1.equipment.validate_slot_usage(obj)

            mock_inherit.return_value = True
            if is_ok:
                self.assertTrue(self.char1.equipment.validate_slot_usage(obj))
            else:
                with self.assertRaisesRegex(EquipmentError, "^Equipment full"):
                    self.char1.equipment.validate_slot_usage(obj)

    def test_get_current_slot(self):
        """ test that we can get a slot from an object """
        obj = MagicMock()
        self.assertIsNone(self.char1.equipment.get_current_slot(obj))

        self.char1.equipment.add(self.helmet)
        self.assertEqual(WieldLocation.BACKPACK, self.char1.equipment.get_current_slot(self.helmet))
        self.char1.equipment.move(self.helmet)
        self.assertEqual(WieldLocation.HEAD, self.char1.equipment.get_current_slot(self.helmet))

    def test_display_loadout(self):
        """ Test that displaying the loadout works. """
        self.assertEqual(
            self.char1.equipment.display_loadout(),
            """
Right Hand: |xbare hands|n
Left Hand: None
Body: None
Head: None
""".strip()
        )
        self.char1.equipment.move(self.weapon)
        self.char1.equipment.move(self.shield)
        self.char1.equipment.move(self.armor)
        self.char1.equipment.move(self.helmet)
        self.assertEqual(
            self.char1.equipment.display_loadout(),
            """
Right Hand: |xweapon|n
Left Hand: |nshield|n
Body: |narmor|n
Head: |nhelmet|n
""".strip()
        )
        self.char1.equipment.move(self.big_weapon)
        self.assertEqual(
            self.char1.equipment.display_loadout(),
            """
Right Hand: |nbig_weapon|n
Left Hand: |nbig_weapon|n
Body: |narmor|n
Head: |nhelmet|n
""".strip()
        )

    def test_organized_backpack(self):
        """ test that organized_backpack returns a sorted dict of the backpack contents """
        self.assertEqual({}, self.char1.equipment.organized_backpack())

        expected = {
            "backpack item": {
                "capacity": 2,
                "quantity": 2,
            },
            "backpack item 2": {
                "capacity": 5,
                "quantity": 1
            },
            "|xweapon|n": {
                "capacity": 1,
                "quantity": 1
            }
        }
        item_copy = create.create_object(
            Object,
            key="backpack item",
        )
        self.char1.equipment.add(self.weapon)
        self.char1.equipment.add(self.item2)
        self.char1.equipment.add(self.item)
        self.char1.equipment.add(item_copy)
        self.assertEqual(expected, self.char1.equipment.organized_backpack())

    def test_paged_backpack(self):
        """ test the paged_backpack function """
        item_copy = create.create_object(
            Object,
            key="backpack item",
        )
        self.char1.equipment.add(self.weapon)
        self.char1.equipment.add(self.item2)
        self.char1.equipment.add(self.item)
        self.char1.equipment.add(item_copy)
        expected = (
            1,
            1,
            [
                ("backpack item", {"capacity": 2, "quantity": 2}),
                ("backpack item 2", {"capacity": 5, "quantity": 1}),
                ("|xweapon|n", {"capacity": 1, "quantity": 1}),
            ],
        )
        self.assertEqual(expected, self.char1.equipment.paged_backpack())
        self.assertEqual(expected, self.char1.equipment.paged_backpack(page="abc"))
        self.assertEqual(expected, self.char1.equipment.paged_backpack(page="abc", per_page="abc"))
        expected = (
            1,
            2,
            [
                ("backpack item", {"capacity": 2, "quantity": 2}),
                ("backpack item 2", {"capacity": 5, "quantity": 1}),
            ],
        )
        self.assertEqual(expected, self.char1.equipment.paged_backpack(page=1, per_page=2))
        expected = (
            2,
            2,
            [
                ("|xweapon|n", {"capacity": 1, "quantity": 1}),
            ],
        )
        self.assertEqual(expected, self.char1.equipment.paged_backpack(page=2, per_page=2))

    def test_display_slot_usage(self):
        """ Test displaying slots. """
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
        """ Test that moving gear works. """
        obj = getattr(self, itemname)
        self.char1.equipment.move(obj)
        # check that item ended up in the right place
        if where is WieldLocation.BACKPACK:
            self.assertTrue(obj in self.char1.equipment.slots[where])
        else:
            self.assertEqual(self.char1.equipment.slots[where], obj)

    def test_add(self):
        """ Test that adding gear works. """
        self.char1.equipment.add(self.weapon)
        self.assertEqual(self.char1.equipment.slots[WieldLocation.WEAPON_HAND], NoneObject())
        self.assertTrue(self.weapon in self.char1.equipment.backpack)

    def test_two_handed_exclusive(self):
        """ Two-handed weapons can't be used together with weapon+shield """
        self.char1.equipment.move(self.big_weapon)
        self.assertEqual(self.char1.equipment.slots[WieldLocation.TWO_HANDS], self.big_weapon)
        # equipping sword or shield removes two-hander
        self.char1.equipment.move(self.shield)
        self.assertEqual(self.char1.equipment.slots[WieldLocation.SHIELD_HAND], self.shield)
        self.assertEqual(self.char1.equipment.slots[WieldLocation.TWO_HANDS], NoneObject())
        self.char1.equipment.move(self.weapon)
        self.assertEqual(self.char1.equipment.slots[WieldLocation.WEAPON_HAND], self.weapon)

        # the two-hander removes the two weapons
        self.char1.equipment.move(self.big_weapon)
        self.assertEqual(self.char1.equipment.slots[WieldLocation.TWO_HANDS], self.big_weapon)
        self.assertEqual(self.char1.equipment.slots[WieldLocation.SHIELD_HAND], NoneObject())
        self.assertEqual(self.char1.equipment.slots[WieldLocation.WEAPON_HAND], NoneObject())

    def test_remove__with_obj(self):
        """ Test that you can remove gear by referring to the item. """
        self.char1.equipment.move(self.shield)
        self.char1.equipment.move(self.item)
        self.char1.equipment.add(self.weapon)

        self.assertEqual(self.char1.equipment.slots[WieldLocation.SHIELD_HAND], self.shield)
        self.assertEqual(
            self.char1.equipment.slots[WieldLocation.BACKPACK], [self.item, self.weapon]
        )

        self.assertEqual(self.char1.equipment.remove(self.shield), [self.shield])
        self.assertEqual(self.char1.equipment.remove(self.item), [self.item])

        self.assertEqual(self.char1.equipment.slots[WieldLocation.SHIELD_HAND], NoneObject())
        self.assertEqual(self.char1.equipment.slots[WieldLocation.BACKPACK], [self.weapon])

    def test_remove__with_slot(self):
        """ Test that you can remove gear by referring to location. """
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

        self.assertEqual(self.char1.equipment.slots[WieldLocation.SHIELD_HAND], NoneObject())
        self.assertEqual(self.char1.equipment.slots[WieldLocation.BACKPACK], [])

    def test_properties(self):
        """ Test that properties change when equipping gear. """
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
