"""
Test chargen.

"""

from unittest.mock import MagicMock, patch

from evennia import create_object
from evennia.utils.test_resources import BaseEvenniaTest

from typeclasses import objects
from world import chargen, enums
from world.characters.classes import CharacterClasses
from world.characters.races import Races


class CharacterGenerationTest(BaseEvenniaTest):
    """
    Test the Character generator in the rule engine.

    """

    def setUp(self):
        super().setUp()
        self.randint_patcher = patch("world.rules.randint")
        self.mock_randint = self.randint_patcher.start()
        self.mock_randint.return_value = 15

        self.choice_patcher = patch("random.choice")
        self.mock_choice = self.choice_patcher.start()
        self.mock_choice.side_effect = ["female", Races.Human, CharacterClasses.Warrior]

        self.chargen = chargen.TemporaryCharacterSheet()

    def tearDown(self):
        self.randint_patcher.stop()
        self.choice_patcher.stop()

    def test_base_chargen(self):
        """ Test that the chargen has the TemporaryCharacter. """
        self.assertEqual(self.chargen.strength, 3)
        self.assertEqual(self.chargen.armor, "Leather Armor")
        self.assertEqual(self.chargen.shield, "buckler")
        self.assertEqual(
            self.chargen.backpack, ["ration", "ration"]
        )

    def test_build_desc(self):
        """ Test that the character description is properly created. """
        self.assertEqual(
            self.chargen.desc,
            "Enio is a female Human, statuesque with a sunken face, sallow skin, oily hair,"
            " rapid-fire speech and oversized clothing."
        )

    @patch("world.chargen.spawn")
    def test_apply(self, mock_spawn):
        """ Test accepting the character and creating it. """
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
        """ Test changing character race. """
        base_str = self.chargen.strength
        self.chargen.swap_race(Races.Orc)
        self.assertEqual(self.chargen.strength, base_str + 2)  # Orc bonus is +2
        self.chargen.swap_race(Races.Elf)
        self.assertEqual(self.chargen.strength, base_str - 1)  # Elf bonus is -1
        self.chargen.swap_race(Races.Human)
        self.assertEqual(self.chargen.strength, base_str) # Back to base
