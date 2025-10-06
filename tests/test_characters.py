"""
Test characters.

"""

from unittest.mock import patch

from evennia.utils.test_resources import EvenniaTest
from world.characters.classes import CharacterClasses
from world.characters.races import Races


class TestCharacters(EvenniaTest):
    """ Test Character methods. """

    def test_abilities(self):
        """ Test abilities work. """
        self.char1.strength += 2
        self.assertEqual(self.char1.strength, 3)

    def test_cclass(self):
        """ Test character classes work. """
        self.char1.db.cclass_key = "paladin"
        self.assertEqual(self.char1.cclass, CharacterClasses.Paladin)
        self.char1.ndb.cclass = CharacterClasses.Warrior
        self.assertEqual(self.char1.cclass, CharacterClasses.Warrior)

    def test_race(self):
        """ Test races work. """
        self.char1.db.race_key = "dwarf"
        self.assertEqual(self.char1.race, Races.Dwarf)
        self.char1.ndb.race = Races.Human
        self.assertEqual(self.char1.race, Races.Human)

    def test_hurt_level(self):
        """ Test hurt_level text. """
        self.char1.hp = self.char1.hp_max = 100
        self.assertEqual(self.char1.hurt_level, "|gPerfect|n")
        self.char1.hp = 90
        self.assertEqual(self.char1.hurt_level, "|gScraped|n")
        self.char1.hp = 75
        self.assertEqual(self.char1.hurt_level, "|GBruised|n")
        self.char1.hp = 50
        self.assertEqual(self.char1.hurt_level, "|yHurt|n")
        self.char1.hp = 40
        self.assertEqual(self.char1.hurt_level, "|yWounded|n")
        self.char1.hp = 25
        self.assertEqual(self.char1.hurt_level, "|rBadly Wounded|n")
        self.char1.hp = 10
        self.assertEqual(self.char1.hurt_level, "|rBarely Hanging On|n")
        self.char1.hp = 0
        self.assertEqual(self.char1.hurt_level, "|RCollapsed!|n")
        self.char1.hp = -10
        self.assertEqual(self.char1.hurt_level, "|RCollapsed!|n")

    def test_mana_level(self):
        """ Test mana_level text. """
        self.char1.mana = self.char1.mana_max = 100
        self.assertEqual(self.char1.mana_level, "|gPerfect|n")
        self.char1.mana = 90
        self.assertEqual(self.char1.mana_level, "|gWell Studied|n")
        self.char1.mana = 75
        self.assertEqual(self.char1.mana_level, "|GStudied|n")
        self.char1.mana = 50
        self.assertEqual(self.char1.mana_level, "|yLosing Concentration|n")
        self.char1.mana = 40
        self.assertEqual(self.char1.mana_level, "|ySlightly Drained|n")
        self.char1.mana = 25
        self.assertEqual(self.char1.mana_level, "|rDrained|n")
        self.char1.mana = 10
        self.assertEqual(self.char1.mana_level, "|rBarely Hanging On|n")
        self.char1.mana = 0
        self.assertEqual(self.char1.mana_level, "|REmpty!|n")
        self.char1.mana = -10
        self.assertEqual(self.char1.mana_level, "|REmpty!|n")

    def test_stamina_level(self):
        """ Test stamina_level text. """
        self.char1.stamina = self.char1.stamina_max = 100
        self.assertEqual(self.char1.stamina_level, "|gPerfect|n")
        self.char1.stamina = 90
        self.assertEqual(self.char1.stamina_level, "|gLight Sweat|n")
        self.char1.stamina = 75
        self.assertEqual(self.char1.stamina_level, "|GSweaty|n")
        self.char1.stamina = 50
        self.assertEqual(self.char1.stamina_level, "|yWinded|n")
        self.char1.stamina = 40
        self.assertEqual(self.char1.stamina_level, "|yTired|n")
        self.char1.stamina = 25
        self.assertEqual(self.char1.stamina_level, "|rExhausted|n")
        self.char1.stamina = 10
        self.assertEqual(self.char1.stamina_level, "|rBarely Hanging On|n")
        self.char1.stamina = 0
        self.assertEqual(self.char1.stamina_level, "|RCollapsed!|n")
        self.char1.stamina = -10
        self.assertEqual(self.char1.stamina_level, "|RCollapsed!|n")

    def test_heal(self):
        """Make sure we don't heal too much"""
        self.char1.hp = 0
        self.char1.hp_max = 8

        self.char1.heal(1)
        self.assertEqual(self.char1.hp, 1)
        self.char1.heal(100)
        self.assertEqual(self.char1.hp, 8)

    def test_at_damage(self):
        """ Test that damage is applied properly. """
        self.char1.hp = 8
        self.char1.at_damage(5)
        self.assertEqual(self.char1.hp, 3)

    def test_at_recovery(self):
        """ Test that stamina and mana recover properly. """
        self.char1.strength = self.char1.will = 1
        self.char1.stamina = self.char1.mana = 1
        self.char1.at_recovery()
        self.assertEqual(self.char1.stamina, 2)
        self.assertEqual(self.char1.mana, 2)

        # dont recover more than max
        self.char1.strength = self.char1.will = 1
        self.char1.stamina_max = self.char1.stamina = self.char1.mana_max = self.char1.mana = 1
        self.char1.at_recovery()
        self.assertEqual(self.char1.stamina, 1)
        self.assertEqual(self.char1.mana, 1)

        # recover even if stats are < 1
        self.char1.strength = self.char1.will = 0
        self.char1.stamina = self.char1.mana = 0
        self.char1.at_recovery()
        self.assertEqual(self.char1.stamina, 1)
        self.assertEqual(self.char1.mana, 1)

    def test_at_pay(self):
        """ Test that paying deducts coins properly. """
        self.char1.coins = 100

        result = self.char1.at_pay(60)
        self.assertEqual(result, 60)
        self.assertEqual(self.char1.coins, 40)

        # can't get more coins than we have
        result = self.char1.at_pay(100)
        self.assertEqual(result, 40)
        self.assertEqual(self.char1.coins, 0)

    @patch("typeclasses.characters.Character.at_look")
    def test_at_post_move(self, mock_at_look):
        """ Test that look is called after a character moves. """
        mock_at_look.return_value = "room!"
        with patch("typeclasses.characters.Character.msg") as mock_msg:
            self.char1.at_post_move(self.char1.location)
            mock_msg.assert_called_once_with(
                text=("room!", {"type": "look"})
            )
