"""
Test Objects.
"""

from evennia.utils import create
from evennia.utils.test_resources import EvenniaTest
from typeclasses.characters import Character
from typeclasses.objects import ConsumableHealingObject
from typeclasses.rooms import Room
from .mixins import AinneveTestMixin

class TestConsumableHealingObject(AinneveTestMixin, EvenniaTest):
    """ Test ConsumableHealingObject. """

    def setUp(self):
        super().setUp()
        self.char = create.create_object(
            Character,
            key="test char"
        )
        self.char.location = create.create_object(
            Room,
            key="test room"
        )

    def test_at_use(self):
        """ test that using a ConsumableHealingObject heals the user. """
        heal_pot = create.create_object(
            ConsumableHealingObject,
            key="ration"
        )
        self.char.equipment.move(heal_pot)
        orig_hp = self.char.hp
        self.char.at_damage(5)
        damaged_hp = self.char.hp
        self.assertEqual(damaged_hp, orig_hp - 5)
        heal_pot.at_use(self.char)
        self.assertEqual(self.char.hp, damaged_hp + 3)
