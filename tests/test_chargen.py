"""
Test chargen.

"""

from unittest.mock import patch

from evennia.utils.test_resources import EvenniaTest

from world import chargen
from world.characters.classes import CHARACTER_CLASSES
from world.characters.races import RACES


class CharacterGenerationTest(EvenniaTest):
    """
    Test the Character generator in the rule engine.

    """

    def setUp(self):
        super().setUp()
        self.randint_patcher = patch("world.rules.randint")
        self.mock_randint = self.randint_patcher.start()
        self.mock_randint.return_value = 2
        self.choice_patcher = patch("random.choice")
        self.mock_choice = self.choice_patcher.start()
        self.chargen = chargen.TemporaryCharacterSheet()

    def tearDown(self):
        self.randint_patcher.stop()
        self.choice_patcher.stop()
        super().tearDown()

    def test_random_name(self):
        """test that we can get a random name"""
        self.assertEqual(self.chargen.random_name(), "Adelaide")

    def test_random_gender(self):
        """test that we can get a random gender"""
        self.mock_choice.return_value = "female"
        self.assertEqual(self.chargen.random_gender(), "female")

    def test_random_race(self):
        """test that we can get a random race"""
        self.mock_choice.return_value = RACES["furry"]
        self.assertEqual(self.chargen.random_race(), RACES["furry"])

    def test_random_cclass(self):
        """test that we can get a random character class"""
        self.mock_choice.return_value = CHARACTER_CLASSES["min_maxer"]
        self.assertEqual(self.chargen.random_cclass(), CHARACTER_CLASSES["min_maxer"])

    def test_random_appearance_attribute(self):
        """test that we can get a random physical_appearance attribute"""
        self.assertEqual(self.chargen.random_appearance_attribute("physique"), "brawny")
        self.assertEqual(self.chargen.random_appearance_attribute("face"), "blunt")
        self.assertEqual(
            self.chargen.random_appearance_attribute("skin"), "birthmarked"
        )
        self.assertEqual(self.chargen.random_appearance_attribute("hair"), "braided")
        self.assertEqual(self.chargen.random_appearance_attribute("clothing"), "bloody")
        self.assertEqual(self.chargen.random_appearance_attribute("speech"), "booming")

    def test_random_appearance(self):
        """test that we can randomize the character's physical_appearance"""
        self.chargen.random_appearance()
        self.assertEqual(
            self.chargen.physical_appearance,
            " is a genderless raceless, brawny with a blunt face,"
            " birthmarked skin, braided hair, booming speech and"
            " bloody clothing.",
        )

    def test_apply_ability_bonus(self):
        """
        test that we can apply a racial ability bonus and it gets added to a stack in case it needs
            to be reverted later
        """
        self.chargen.apply_ability_bonus("strength", 10)
        self.assertEqual(self.chargen.ability_bonus_stack, [("strength", 10)])
        self.assertEqual(self.chargen.strength, 10)
        self.chargen.apply_ability_bonus("strength", 5)
        self.assertEqual(
            self.chargen.ability_bonus_stack, [("strength", 10), ("strength", 5)]
        )
        self.assertEqual(self.chargen.strength, 15)

    def test_revert_ability_bonuses(self):
        """test that we can revert ability bonuses applied by a race when we remove that race"""
        self.chargen.apply_ability_bonus("strength", 10)
        self.chargen.apply_ability_bonus("strength", 5)
        self.chargen.revert_ability_bonuses()
        self.assertEqual(self.chargen.ability_bonus_stack, [])
        self.assertEqual(self.chargen.strength, 0)

    def test_apply_race(self):
        """test applying a race to the TemporaryCharacterSheet"""
        self.chargen.apply_race(RACES["furry"])
        self.assertEqual(self.chargen.race, RACES["furry"])
        self.assertEqual(self.chargen.strength, -1)
        self.assertEqual(self.chargen.cunning, 2)
        self.assertEqual(self.chargen.will, -1)

        self.chargen.apply_race(RACES["robot_llm"])
        self.assertEqual(self.chargen.race, RACES["robot_llm"])
        self.assertEqual(self.chargen.strength, 0)
        self.assertEqual(self.chargen.cunning, -2)
        self.assertEqual(self.chargen.will, 2)

        self.chargen.apply_race(None)
        self.assertEqual(self.chargen.race, "raceless")
        self.assertEqual(self.chargen.strength, 0)
        self.assertEqual(self.chargen.cunning, 0)
        self.assertEqual(self.chargen.will, 0)

    def test_apply_cclass(self):
        """test applying a character class to the TemporaryCharacterSheet"""
        self.chargen.apply_cclass(CHARACTER_CLASSES["antifa_rioter"])
        self.assertEqual(self.chargen.cclass, CHARACTER_CLASSES["antifa_rioter"])
        self.assertEqual(self.chargen.hp_max, 20)
        self.assertEqual(self.chargen.hp, 20)
        self.assertEqual(self.chargen.mana_max, 16)
        self.assertEqual(self.chargen.mana, 16)
        self.assertEqual(self.chargen.stamina_max, 22)
        self.assertEqual(self.chargen.stamina, 22)
        self.assertEqual(self.chargen.weapon, "bike_lock")
        self.assertEqual(self.chargen.weapon_desc, "|xplasteel bike lock|n")
        self.assertEqual(self.chargen.shield, "garbage_lid")
        self.assertEqual(self.chargen.shield_desc, "|xplasteel garbage lid|n")
        self.assertEqual(self.chargen.helmet, "hockey_mask")
        self.assertEqual(self.chargen.helmet_desc, "|xplasteel hockey mask|n")
        self.assertEqual(self.chargen.armor, "chest_plate")
        self.assertEqual(self.chargen.armor_desc, "|xplasteel chest plate|n")

        self.chargen.apply_cclass(CHARACTER_CLASSES["hacker"])
        self.assertEqual(self.chargen.cclass, CHARACTER_CLASSES["hacker"])
        self.assertEqual(self.chargen.hp_max, 16)
        self.assertEqual(self.chargen.hp, 16)
        self.assertEqual(self.chargen.mana_max, 20)
        self.assertEqual(self.chargen.mana, 20)
        self.assertEqual(self.chargen.stamina_max, 18)
        self.assertEqual(self.chargen.stamina, 18)
        self.assertEqual(self.chargen.weapon, "laptop")
        self.assertEqual(self.chargen.weapon_desc, "|xquartz core laptop|n")
        self.assertEqual(self.chargen.shield, "none")
        self.assertEqual(self.chargen.shield_desc, "none")
        self.assertEqual(self.chargen.helmet, "specs")
        self.assertEqual(self.chargen.helmet_desc, "|xtinted polymer specs|n")
        self.assertEqual(self.chargen.armor, "trench")
        self.assertEqual(self.chargen.armor_desc, "|xdust-weave canvas trench|n")

        self.chargen.apply_cclass(None)
        self.assertEqual(self.chargen.cclass, "jobless bum")
        self.assertEqual(self.chargen.hp_max, 0)
        self.assertEqual(self.chargen.hp, 0)
        self.assertEqual(self.chargen.mana_max, 0)
        self.assertEqual(self.chargen.mana, 0)
        self.assertEqual(self.chargen.stamina_max, 0)
        self.assertEqual(self.chargen.stamina, 0)
        self.assertEqual(self.chargen.weapon, None)
        self.assertEqual(self.chargen.weapon_desc, None)
        self.assertEqual(self.chargen.shield, None)
        self.assertEqual(self.chargen.shield_desc, None)
        self.assertEqual(self.chargen.helmet, None)
        self.assertEqual(self.chargen.helmet_desc, None)
        self.assertEqual(self.chargen.armor, None)
        self.assertEqual(self.chargen.armor_desc, None)

    def test_apply_appearance_attribute(self):
        """test applying a single appearance attribute to the TemporaryCharacterSheet"""
        self.chargen.apply_appearance_attribute("physique", "gross")
        self.assertEqual(self.chargen.physique, "gross")

    def test_apply_appearance(self):
        """test applying the appearance to the TemporaryCharacterSheet"""
        self.chargen.apply_appearance()
        self.assertEqual(
            self.chargen.physical_appearance,
            " is a genderless raceless, brawny with a blunt face,"
            " birthmarked skin, braided hair, booming speech and"
            " bloody clothing.",
        )

    def test_show_sheet(self):
        """test showing the temporary character sheet"""
        self.chargen.name = "some name"
        self.chargen.gender = "female"
        self.chargen.apply_race(RACES["furry"])
        self.chargen.apply_cclass(CHARACTER_CLASSES["antifa_rioter"])
        self.chargen.random_appearance()
        self.assertEqual(
            self.chargen.show_sheet(),
            """
some name the female Furry Antifa Rioter

STR -1
CUN +2
WIL -1

some name is a female Furry, brawny with a blunt face, birthmarked skin, braided hair,"""
            """ booming speech and bloody clothing.

Your belongings:

Weapon:   |xplasteel bike lock|n
Shield:   |xplasteel garbage lid|n
Armor:    |xplasteel chest plate|n
Helmet:   |xplasteel hockey mask|n
Backpack: ration, ration, ration

""",
        )

    def test_apply(self):
        """test that apply creates a new character"""
        orig_char_classes = CHARACTER_CLASSES.copy()
        self.chargen.name = "some name"
        self.chargen.gender = "female"
        self.chargen.apply_race(RACES["furry"])
        self.chargen.apply_cclass(CHARACTER_CLASSES["antifa_rioter"])
        self.chargen.random_appearance()
        new_char = self.chargen.apply(self.account)

        self.assertEqual(new_char.name, "some name")
        self.assertEqual(new_char.gender, "female")
        self.assertEqual(new_char.strength, -1)
        self.assertEqual(new_char.cunning, 2)
        self.assertEqual(new_char.will, -1)
        self.assertEqual(new_char.race_key, "furry")
        self.assertEqual(new_char.cclass_key, "antifa_rioter")
        self.assertEqual(new_char.hp_max, 20)
        self.assertEqual(new_char.hp, 20)
        self.assertEqual(new_char.mana_max, 16)
        self.assertEqual(new_char.mana, 16)
        self.assertEqual(new_char.stamina_max, 22)
        self.assertEqual(new_char.stamina, 22)
        self.assertEqual(
            new_char.physical_appearance,
            "some name is a female Furry, brawny with a blunt face, birthmarked skin, braided hair,"
            " booming speech and bloody clothing.",
        )
        # test weird bug that caused the CHARACTER_CLASSES dict to change
        self.assertEqual(CHARACTER_CLASSES, orig_char_classes)
