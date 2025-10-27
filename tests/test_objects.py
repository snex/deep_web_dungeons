"""
Test Objects.
"""

from unittest.mock import patch

from evennia.prototypes.spawner import spawn
from evennia.utils.ansi import strip_ansi

from world.enums import WieldLocation
from .mixins import AinneveTestMixin

class TestObject(AinneveTestMixin):
    """ Test base Object. """

    def test_get_display_name(self):
        """
        get_display_name should add the material and a tier color for objects that have those.
        it should also handle objects with a custom `display_name` attribute.
        """
        ration = spawn("ration")[0]
        self.assertEqual(ration.get_display_name(self.char1), "ration")
        bike_lock = spawn("bike_lock")[0]
        self.assertEqual(bike_lock.get_display_name(self.char1), "|xplasteel bike lock|n")
        specs = spawn("specs")[0]
        self.assertEqual(specs.get_display_name(self.char1), "|xtinted polymer pair of specs|n")
        echo_stone = spawn("echo_stone")[0]
        self.assertEqual(echo_stone.get_display_name(self.char1), "|Gecho stone|n")

    def test_return_appaerance(self):
        """ show details about the object """
        ration = spawn("ration")[0]
        expected_output = strip_ansi("""
+------------------------------------------------------------------------------+
|                                                                              |
|                                    ration                                    |
|   A grey protein block covered in pale-green nutrient paste. Recovers some   |
|                              health when eaten.                              |
|                                                                              |
|                                                                              |
+------------------------------------------------------------------------------+
|                                                                              |
|  Weight:           0.25                Uses:              1                  |
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
+------------------------------------------------------------------------------+
""").strip()
        self.assertEqual(strip_ansi(ration.return_appearance(self.char1).strip()), expected_output)

class TestQuantumLatticeObject(AinneveTestMixin):
    """ Test QuantumLatticeObject. """

    def test_combine(self):
        """ test that combining quantum lattices works properly. """

        ql = spawn("nexus_diamond")[0]
        ql.location = self.char1
        self.assertEqual(ql.combine(self.char1), "|[w|xnexus diamond|n cannot be combined.")

        ql = spawn("dust_shard")[0]
        ql.location = self.char1
        self.char1.equipment.move(ql)
        self.assertEqual(ql.combine(self.char1), "You need 3 |xdust shards|n to combine.")

        ql1 = spawn("dust_shard")[0]
        ql1.location = self.char1
        self.char1.equipment.move(ql1)
        ql2 = spawn("dust_shard")[0]
        ql2.location = self.char1
        self.char1.equipment.move(ql2)
        ql3 = spawn("dust_shard")[0]
        ql3.location = self.char1
        self.char1.equipment.move(ql3)
        msg = ql.combine(self.char1)
        self.assertEqual(msg, "You combine 3 |xdust shards|n into |cstatic bloom|n.")
        # we created 4 total dust shards so we should still have 1
        self.assertEqual(
            [item.name for item in self.char1.equipment.slots[WieldLocation.BACKPACK]],
            ["dust shard", "static bloom"]
        )

class TestScrapObject(AinneveTestMixin):
    """ test scrap items used to repair gear """
    def setUp(self):
        super().setUp()
        self.scrap = spawn("scrap")[0]
        self.char1.equipment.move(self.scrap)
        self.weapon.quality = 50

    def test_at_pre_use(self):
        """ test at_pre_use to see if scrap can be used """
        self.assertFalse(self.scrap.at_pre_use(None, caller=self.char1))
        self.assertFalse(self.scrap.at_pre_use(self.scrap, caller=self.char1))
        self.assertTrue(self.scrap.at_pre_use(self.weapon, caller=self.char1))
        self.weapon.quality = 100
        self.assertFalse(self.scrap.at_pre_use(self.weapon, caller=self.char1))

    @patch("typeclasses.objects.ScrapObject.delete")
    @patch("typeclasses.objects.EquipmentObject.repair")
    def test_use(self, mock_repair, mock_delete):
        """ test using scrap to repair gear """
        self.assertIn(self.scrap, self.char1.equipment.slots[WieldLocation.BACKPACK])
        self.scrap.use(self.weapon, caller=self.char1)
        mock_repair.assert_called_once_with(10)
        mock_delete.assert_called_once()

class TestConsumableHealingObject(AinneveTestMixin):
    """ Test ConsumableHealingObject. """

    def test_at_use(self):
        """ test that using a ConsumableHealingObject heals the user. """

        ration = spawn("ration")[0]
        self.char1.equipment.move(ration)
        orig_hp = self.char1.hp
        self.char1.at_damage(5)
        damaged_hp = self.char1.hp
        self.assertEqual(damaged_hp, orig_hp - 5)
        ration.at_use(self.char1)
        self.assertEqual(self.char1.hp, damaged_hp + 3)

class TestEquipmentObject(AinneveTestMixin):
    """ test equippable items """
    def test_damage_level(self):
        """ test the item's quality display method """
        self.weapon.quality = 100
        self.assertEqual(self.weapon.damage_level, "|gPerfect|n")
        self.weapon.quality = 90
        self.assertEqual(self.weapon.damage_level, "|gScuffed|n")
        self.weapon.quality = 75
        self.assertEqual(self.weapon.damage_level, "|GScratched|n")
        self.weapon.quality = 50
        self.assertEqual(self.weapon.damage_level, "|yWorn|n")
        self.weapon.quality = 40
        self.assertEqual(self.weapon.damage_level, "|yDented|n")
        self.weapon.quality = 25
        self.assertEqual(self.weapon.damage_level, "|rDamaged|n")
        self.weapon.quality = 10
        self.assertEqual(self.weapon.damage_level, "|rFalling Apart|n")
        self.weapon.quality = 0
        self.assertEqual(self.weapon.damage_level, "|RBroken!|n")
        self.weapon.quality = -10
        self.assertEqual(self.weapon.damage_level, "|RBroken!|n")

    def test_scrap_value(self):
        """ test the sell to vendor price of an item """
        self.assertEqual(self.weapon.scrap_value, 1)
        self.weapon.tier = 2
        self.assertEqual(self.weapon.scrap_value, 2)
        self.weapon.tier = 3
        self.assertEqual(self.weapon.scrap_value, 3)
        self.weapon.required_level = 10
        self.assertEqual(self.weapon.scrap_value, 4)
        self.weapon.required_level = 20
        self.assertEqual(self.weapon.scrap_value, 5)

    @patch("world.quantum_lattices.QuantumLattice.from_name")
    def test_vendor_price(self, mock_ql_from_name):
        """ test calculating the vendor price demanded for an item """
        mock_ql_from_name.return_value = None
        self.assertEqual(
            self.weapon.vendor_price,
            {
                "scrap": {"count": 2, "ql": None},
            }
        )
        self.weapon.tier = 2
        self.assertEqual(
            self.weapon.vendor_price,
            {
                "scrap": {"count": 4, "ql": None},
                "resonance crystal": {"count": 2, "ql": None},
            }
        )
        self.weapon.tier = 3
        self.assertEqual(
            self.weapon.vendor_price,
            {
                "scrap": {"count": 6, "ql": None},
                "resonance crystal": {"count": 2, "ql": None},
                "phase pearl": {"count": 2, "ql": None},
            }
        )
        self.weapon.tier = 4
        self.assertEqual(
            self.weapon.vendor_price,
            {
                "scrap": {"count": 8, "ql": None},
                "resonance crystal": {"count": 2, "ql": None},
                "phase pearl": {"count": 2, "ql": None},
                "chromatic heart": {"count": 2, "ql": None},
            }
        )
        self.weapon.affixes = ["prefix_acidic"]
        self.assertEqual(
            self.weapon.vendor_price,
            {
                "chromatic heart": {"count": 2, "ql": None},
                "echo stone": {"count": 1, "ql": None},
                "phase pearl": {"count": 2, "ql": None},
                "resonance crystal": {"count": 2, "ql": None},
                "scrap": {"count": 8, "ql": None},
            }
        )
        self.weapon.affixes = ["prefix_acidic", "prefix_nucular"]
        self.assertEqual(
            self.weapon.vendor_price,
            {
                "chromatic heart": {"count": 2, "ql": None},
                "echo stone": {"count": 2, "ql": None},
                "phase pearl": {"count": 2, "ql": None},
                "resonance crystal": {"count": 2, "ql": None},
                "scrap": {"count": 8, "ql": None},
            }
        )

    def test_repair(self):
        """ test repairing an item """
        self.weapon.quality = 50
        self.weapon.repair(5)
        self.assertEqual(self.weapon.quality, 55)
        self.weapon.quality = 97
        self.weapon.repair(5)
        self.assertEqual(self.weapon.quality, 100)
        self.weapon.quality = 100
        self.weapon.repair(5)
        self.assertEqual(self.weapon.quality, 100)

    def test_get_item_type_stats(self):
        """ test gathering item stats for display on `look item` """
        self.assertEqual(
            self.weapon.get_item_type_stats(),
            {
                "Att. Type": "strength",
                "Cooldown": "2s",
                "Def. Type": "armor",
                "Parry": "|rNo|n",
                "Range": 1,
                "Req. Level": "|g1|n",
                "Allowed Classes": "|rAntifa Rioter|n, |rMin-Maxer|n, |rHacker|n, |rGooner|n,"
                                   " |rShitposter|n, |rConspiracy Nut|n, |rPusher|n, |rGym Bro|n",
            }
        )
        self.weapon.required_level = 10
        self.assertEqual(
            self.weapon.get_item_type_stats(self.char1),
            {
                "Att. Type": "strength",
                "Cooldown": "2s",
                "Def. Type": "armor",
                "Parry": "|rNo|n",
                "Range": 1,
                "Req. Level": "|r10|n",
                "Allowed Classes": "|gAntifa Rioter|n, |rMin-Maxer|n, |rHacker|n, |rGooner|n,"
                                   " |rShitposter|n, |rConspiracy Nut|n, |rPusher|n, |rGym Bro|n",
            }
        )
