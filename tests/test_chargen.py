"""
Test chargen.

"""

from unittest.mock import MagicMock, patch

from parameterized import parameterized

from evennia import create_object
from evennia.utils.test_resources import BaseEvenniaTest

from world import chargen, enums
from typeclasses import objects
from world.characters.classes import CharacterClasses
from world.characters.races import Races


class CharacterGenerationTest(BaseEvenniaTest):
    """
    Test the Character generator in the rule engine.

    """

    @patch('world.chargen.TemporaryCharacterSheet._random_gender')
    @patch('world.chargen.TemporaryCharacterSheet._random_class')
    @patch('world.chargen.TemporaryCharacterSheet._random_race')
    @patch("world.rules.randint")
    def setUp(self, mock_randint, mock_random_race, mock_random_class, mock_random_gender):
        super().setUp()
        mock_randint.return_value = 15
        mock_random_gender.return_value = "female"
        mock_random_race.return_value = Races.Human
        mock_random_class.return_value = CharacterClasses.Warrior
        self.chargen = chargen.TemporaryCharacterSheet()

    def test_base_chargen(self):
        self.assertEqual(self.chargen.strength, 3)
        self.assertEqual(self.chargen.armor, "Leather Armor")
        self.assertEqual(self.chargen.shield, "buckler")
        self.assertEqual(
            self.chargen.backpack, ["ration", "ration"]
        )

    def test_build_desc(self):
        self.assertEqual(
            self.chargen.desc,
            "Enio is a female Human, statuesque with a sunken face, sallow skin, oily hair, rapid-fire speech, and "
            "oversized clothing."
        )

    @patch("world.chargen.spawn")
    def test_apply(self, mock_spawn):
        gambeson = create_object(objects.ArmorObject, key="gambeson")
        mock_spawn.return_value = [gambeson]
        account = MagicMock()
        account.id = 2222

        character = self.chargen.apply(account)

        self.assertEqual(
            character.equipment.all(),
            [
                (None, enums.WieldLocation.WEAPON_HAND),
                (None, enums.WieldLocation.SHIELD_HAND),
                (None, enums.WieldLocation.TWO_HANDS),
                (gambeson, enums.WieldLocation.BODY),
                (None, enums.WieldLocation.HEAD),
            ],
        )

        gambeson.delete()
        character.delete()

    def test_swap_race(self):
        base_str = self.chargen.strength
        self.chargen.swap_race(Races.Orc)
        self.assertEqual(self.chargen.strength, base_str + 2)  # Orc bonus is +2
        self.chargen.swap_race(Races.Elf)
        self.assertEqual(self.chargen.strength, base_str - 1)  # Elf bonus is -1
        self.chargen.swap_race(Races.Human)
        self.assertEqual(self.chargen.strength, base_str) # Back to base
