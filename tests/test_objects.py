"""
Test Objects.
"""

from evennia.prototypes.spawner import spawn
from evennia.utils.test_resources import EvenniaTest

from .mixins import AinneveTestMixin

class TestConsumableHealingObject(AinneveTestMixin, EvenniaTest):
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

    def test_return_appaerance(self):
        """ show details about the object """
        ration = spawn("ration")[0]
        self.assertEqual(ration.return_appearance(self.char1), """
ration

A grey protein block covered in pale-green nutrient paste.

Slots: |w0.25|n, Used from: |wbackpack|n
Quality: |wN/A|n, Uses: |w1|n
Attacks using |wNo attack|n against |wNo defense|n
""")
