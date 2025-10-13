"""
EvAdventure character generation.

"""
import random

from django.conf import settings

from evennia import logger
from evennia.contrib.grid.xyzgrid.xyzgrid import get_xyzgrid
from evennia.objects.models import ObjectDB
from evennia.prototypes.spawner import spawn
from evennia.utils.evmenu import EvMenu
from evennia.utils.evtable import EvTable
from evennia.utils.utils import inherits_from
from typeclasses.characters import Character
from world.characters.classes import CHARACTER_CLASSES
from world.characters.races import RACES, Race
from world.enums import Ability
from world.utils import each_slice
from .random_tables import chargen_tables
from .rules import dice


_TEMP_SHEET = """
{name} the {gender} {race} {cclass}

STR {str_plus_minus}{strength}
CUN {cun_plus_minus}{cunning}
WIL {wil_plus_minus}{will}

{description}

Your belongings:
{equipment}
"""

_ABILITIES = [a.value for a in Ability]
_APPEARANCE_OPTIONS = [
    "physique",
    "face",
    "skin",
    "hair",
    "clothing",
    "speech",
]

# disable too-many-instance-attributes since this is a temporary character sheet that needs
# to hold a lot of attributes
# pylint: disable=too-many-instance-attributes
class TemporaryCharacterSheet:
    """
    This collects all the rules for generating a new character. An instance of this class is used
    to pass around the current character state during character generation and also applied to
    the character at the end. This class instance can also be saved on the menu to make sure a user
    is not losing their half-created character.
    """

    def __init__(self):
        self.name = self.desc = self.physical_appearance = ""
        self.gender = "genderless"

        self.race = "raceless"
        self.cclass = "jobless bum"

        self.strength = 0
        self.will = 0
        self.cunning = 0

        # make it easy to apply and revert bonuses if the user changes their mind and goes back
        self.ability_bonus_stack = []

        self.hp = self.hp_max = 1
        self.mana = self.mana_max = 1
        self.stamina = self.stamina_max = 1

        self.weapon = self.weapon_desc = ""
        self.shield = self.shield_desc = ""
        self.helmet = self.helmet_desc = ""
        self.armor = self.armor_desc = ""

        self.backpack = [
            "ration",
            "ration",
            "ration",
        ]

        self.physique = self.face = self.skin = self.hair = self.clothing = self.speech = "RANDOM"

    def random_name(self):
        """ return a random name from the roll tables """
        return dice.roll_random_table("1d282", chargen_tables["name"])

    def random_gender(self):
        """ return a random gender """
        return random.choice(["male", "female", "other-gendered", "non-gendered"])

    def random_race(self):
        """ return a random Race """
        return random.choice(list(RACES.values()))

    def random_cclass(self):
        """ return a random CharacterClass """
        return random.choice(list(CHARACTER_CLASSES.values()))

    def random_appearance_attribute(self, attribute):
        """ return a random single physical_appearance attribute from the roll tables """
        return dice.roll_random_table("1d20", chargen_tables.get(attribute, "physique"))

    def random_appearance(self):
        """
        Generate a completely random physical_appearance
            and apply it to the TemporaryCharacterSheet
        """
        self.physique = self.random_appearance_attribute("physique")
        self.face = self.random_appearance_attribute("face")
        self.skin = self.random_appearance_attribute("skin")
        self.hair = self.random_appearance_attribute("hair")
        self.clothing = self.random_appearance_attribute("clothing")
        self.speech = self.random_appearance_attribute("speech")

        self.apply_appearance()

    def apply_ability_bonus(self, ability, mod):
        """
        Add an ability bonus to the stack (for possible later revert)
            and apply it to the TemporaryCharacterSheet
        """
        self.ability_bonus_stack.append((ability, mod))
        setattr(self, ability, getattr(self, ability) + mod)

    def revert_ability_bonuses(self):
        """ Revert the ability bonuses recorded on the stack. """
        while self.ability_bonus_stack:
            ability, mod = self.ability_bonus_stack.pop()
            setattr(self, ability, getattr(self, ability) - mod)

    def apply_race(self, new_race):
        """ Apply the new race, removing an old race if necessary. """

        if inherits_from(self.race, Race):
            self.revert_ability_bonuses()

        if not new_race:
            self.race = "raceless"
            return

        self.race = new_race
        self.apply_ability_bonus("strength", self.race.strength_mod)
        self.apply_ability_bonus("cunning", self.race.cunning_mod)
        self.apply_ability_bonus("will", self.race.will_mod)

    def apply_cclass(self, new_cclass):
        """ Apply the new class, removing an old class if necessary. """

        if not new_cclass:
            self.hp_max = self.hp = self.mana_max = self.mana = self.stamina_max = self.stamina = 0
            self.weapon = self.shield = self.helmet = self.armor = None
            self.weapon_desc = self.shield_desc = self.helmet_desc = self.armor_desc = None
            self.cclass = "jobless bum"
            return

        self.cclass = new_cclass
        self.hp_max = 10 + self.cclass.stat_dice.health_dice[1]
        self.hp = self.hp_max
        self.mana_max = 10 + self.cclass.stat_dice.mana_dice[1]
        self.mana = self.mana_max
        self.stamina_max = 10 + self.cclass.stat_dice.stamina_dice[1]
        self.stamina = self.stamina_max

        # class-based starting equipment
        self.weapon = new_cclass.starting_gear["weapon"]
        self.weapon_desc = new_cclass.starting_gear["weapon_desc"]
        self.shield = new_cclass.starting_gear["shield"]
        self.shield_desc = new_cclass.starting_gear["shield_desc"]
        self.helmet = new_cclass.starting_gear["helmet"]
        self.helmet_desc = new_cclass.starting_gear["helmet_desc"]
        self.armor = new_cclass.starting_gear["armor"]
        self.armor_desc = new_cclass.starting_gear["armor_desc"]

    def apply_appearance_attribute(self, attribute, value):
        """ apply one physical_appearance attribute to the TemporaryCharacterSheet """
        setattr(self, attribute, value)

    def apply_appearance(self):
        """ apply the entire physical_appearance to the TemporaryCharacterSheet """
        for appearance_option in _APPEARANCE_OPTIONS:
            if getattr(self, appearance_option) == "RANDOM":
                self.apply_appearance_attribute(
                    appearance_option, self.random_appearance_attribute(appearance_option)
                )

        self.physical_appearance = (
            f"{self.name} is a {self.gender} {self.race}, {self.physique} with a {self.face} face,"
            f" {self.skin} skin, {self.hair} hair, {self.speech} speech and"
            f" {self.clothing} clothing."
        )

    def show_sheet(self):
        """
        Show a temp character sheet, a compressed version of the real thing.

        """
        equipment_str = f"""
Weapon:   {self.weapon_desc}
Shield:   {self.shield_desc}
Armor:    {self.armor_desc}
Helmet:   {self.helmet_desc}
Backpack: {', '.join((str(eq) for eq in self.backpack))}
"""

        return _TEMP_SHEET.format(
            name=self.name,
            gender=self.gender,
            str_plus_minus=("+" if self.strength >=0 else ""),
            strength=self.strength,
            cun_plus_minus=("+" if self.cunning >=0 else ""),
            cunning=self.cunning,
            wil_plus_minus=("+" if self.will >=0 else ""),
            will=self.will,
            race=self.race,
            cclass=self.cclass,
            description=self.physical_appearance,
            equipment=equipment_str
        )

    def _add_gear_to_new_character(self, new_character):
        if self.weapon:
            try:
                weapon = spawn(self.weapon)
                weapon[0].move_to(new_character, quiet=True, move_type="get")
                new_character.equipment.move(weapon[0])
            except KeyError:
                logger.log_err(
                    f"[Chargen] Could not spawn Weapon: Prototype not found for '{self.weapon}'."
                )

        if self.armor:
            try:
                armor = spawn(self.armor)
                armor[0].move_to(new_character, quiet=True, move_type="get")
                new_character.equipment.move(armor[0])
            except KeyError:
                logger.log_err(
                    f"[Chargen] Could not spawn Armor: Prototype not found for '{self.armor}'."
                )

        if self.shield:
            try:
                shield = spawn(self.shield)
                shield[0].move_to(new_character, quiet=True, move_type="get")
                new_character.equipment.move(shield[0])
            except KeyError:
                logger.log_err(
                    f"[Chargen] Could not spawn Shield: Prototype not found for '{self.shield}'."
                )

        if self.helmet:
            try:
                helmet = spawn(self.helmet)
                helmet[0].move_to(new_character, quiet=True, move_type="get")
                new_character.equipment.move(helmet[0])
            except KeyError:
                logger.log_err(
                    f"[Chargen] Could not spawn Helmet: Prototype not found for '{self.helmet}'."
                )

        for item in self.backpack:
            try:
                item = spawn(item)
                item[0].move_to(new_character, quiet=True, move_type="get")
            except KeyError:
                logger.log_err(f"[Chargen] Could not spawn Item: Prototype not found for '{item}'.")


    def apply(self, account):
        """
        Once the chargen is complete, call this create and set up the character.

        """
        grid = get_xyzgrid()
        start_location = grid.get_room(('19', '9', 'control-station-7'))
        if start_location:
            # The room we got above is a queryset so we get it by index
            start_location = start_location[0]
        else:
            start_location = ObjectDB.objects.get_id(settings.START_LOCATION)

        default_home = ObjectDB.objects.get_id(settings.DEFAULT_HOME)
        permissions = settings.PERMISSION_ACCOUNT_DEFAULT

        # set the desc a final time to get the right details!
        self.physical_appearance = (
            f"{self.name} is a {self.gender} {self.race}, {self.physique} with a {self.face} face,"
            f" {self.skin} skin, {self.hair} hair, {self.speech} speech and"
            f" {self.clothing} clothing."
        )

        # creating character with given abilities
        new_character, err = Character.create(
            key=self.name,
            location=start_location,
            home=default_home,
            permissions=permissions,
            attributes=(
                ("gender", self.gender),
                ("strength", self.strength),
                ("cunning", self.cunning),
                ("will", self.will),
                ("race_key", self.race.key),
                ("cclass_key", self.cclass.key),
                ("hp", self.hp),
                ("hp_max", self.hp_max),
                ("mana", self.mana),
                ("mana_max", self.mana_max),
                ("stamina", self.stamina),
                ("stamina_max", self.stamina_max),
                ("physical_appearance", self.physical_appearance),
                ("desc", ""),
            ),
        )

        if err:
            logger.log_err(f"Error during character creation: #{err}")

        new_character.locks.add(
            f"puppet:id({new_character.id}) or pid({account.id}) or perm(Developer) or"
            " pperm(Developer);delete:id({account.id}) or"
            " perm(Admin)"
        )

        self._add_gear_to_new_character(new_character)

        return new_character

def start_chargen(caller, session=None):
    """
    This is a start point for spinning up the chargen from a menu.
    """
    menu_tree = {
        "node_end_chargen": node_end_chargen,
        "node_set_name": node_set_name,
        "node_show_genders": node_show_genders,
        "node_apply_gender": node_apply_gender,
        "node_show_abilities": node_show_abilities,
        "node_apply_ability": node_apply_ability,
        "node_show_races": node_show_races,
        "node_apply_race": node_apply_race,
        "node_show_human_abilities": node_show_human_abilities,
        "node_apply_human_abilities": node_apply_human_abilities,
        "node_show_cclasses": node_show_cclasses,
        "node_apply_cclass": node_apply_cclass,
        "node_show_appearance": node_show_appearance,
        "node_show_appearance_option": node_show_appearance_option,
        "node_apply_appearance_option": node_apply_appearance_option,
        "node_apply_appearance": node_apply_appearance,
        "node_apply_character": node_apply_character,
    }

    tmp_character = TemporaryCharacterSheet()

    EvMenu(
        caller,
        menu_tree,
        startnode="node_set_name",
        session=session,
        startnode_input=("", {"tmp_character": tmp_character}),
    )

def node_end_chargen(caller, raw_string, **kwargs):
    """ End chargen and go back to the main menu. """

    return "", None

def _update_name(caller, raw_string, **kwargs):
    """
    Used by node_set_name below to set the character's name.
    If blank is sent in, a random name will be chosen.

    """

    tmp_character = kwargs["tmp_character"]
    tmp_character.name = tmp_character.random_name()

    if raw_string and raw_string.strip() != "":
        tmp_character.name = raw_string.strip().lower().capitalize()

    return "node_show_genders", kwargs


def node_set_name(caller, raw_string, **kwargs):
    """
    Set the name of the character.
    Choose a random name if the user enters nothing.

    """

    tmp_character = kwargs["tmp_character"]

    if kwargs.get("go_back"):
        tmp_character.gender = "genderless"

    text = (
        "Set a name for your character. Leave empty to have a random one chosen for you."
    )
    options = {"key": "_default", "goto": (_update_name, kwargs)}

    return text, options


def node_apply_character(caller, raw_string, **kwargs):
    """
    End chargen and create the character. We will also puppet it.

    """
    tmp_character = kwargs["tmp_character"]
    new_character = tmp_character.apply(caller)
    caller.db._playable_characters.append(new_character)
    session = caller.ndb._evmenu._session
    caller.puppet_object(session=session, obj=new_character)

    text = "Character created!"

    return text, None


def node_show_genders(caller, raw_string, **kwargs):
    """ Let user select a gender. """

    tmp_character = kwargs["tmp_character"]

    if kwargs.get("go_back"):
        tmp_character.gender = "genderless"
        tmp_character.strength = tmp_character.cunning = tmp_character.will = 0

    gender_table = EvTable(
        "Gender",
        "Description",
        table=[
            ["|cMale|n", "|cFemale|n", "|cOther-Gendered|n", "|cNon-Gendered|n"],
            [
                "Your pronouns will be `he` `him` and `his`.",
                "Your pronouns will be `she` `her` and `hers`.",
                "You have a gender but nobody is sure what it is, least of all you. Your pronouns"
                    " will be `they` `them` and `their`.",
                "You have no gender at all. Your pronouns will be `it` and `its`.",
            ],
        ],
        border="cells",
        valign="t",
        width=80,
    )

    text = f"""Your character so far:
{tmp_character.show_sheet()}

Select a |cGender|n. There are no game mechanic differences among genders, but there may be roleplay and story differences.

{gender_table}

Select one by number below or Go Back.
"""

    options = [
        {
            "desc": "|cMale|n",
            "goto": ("node_apply_gender", {"gender": "male", **kwargs})
        },
        {
            "desc": "|cFemale|n",
            "goto": ("node_apply_gender", {"gender": "female", **kwargs})
        },
        {
            "desc": "|cOther-Gendered|n",
            "goto": ("node_apply_gender", {"gender": "other-gendered", **kwargs})
        },
        {
            "desc": "|cNon-Gendered|n",
            "goto": ("node_apply_gender", {"gender": "non-gendered", **kwargs})
        },
        {
            "desc": "Random",
            "goto": ("node_apply_gender", {"gender": tmp_character.random_gender(), **kwargs})
        },
        {
            "desc": "Go Back",
            "goto": ("node_set_name", {"go_back": True, **kwargs})
        },
        {
            "desc": "Cancel and Return to Main Menu",
            "goto": ("node_end_chargen", {})
        },
    ]

    return (text, ""), options

def node_apply_gender(caller, raw_string, **kwargs):
    """ Apply the selected gender. """

    gender = kwargs.get('gender')
    tmp_character = kwargs["tmp_character"]
    tmp_character.gender = gender

    return node_show_abilities(caller, "", tmp_character=tmp_character)

def node_show_abilities(caller, raw_string, **kwargs):
    """ Let user assign ability scores. """

    tmp_character = kwargs["tmp_character"]

    if kwargs.get("go_back"):
        tmp_character.strength = tmp_character.cunning = tmp_character.will = 0
        tmp_character.race = "raceless"

    abilities_selected = kwargs.pop("abilities_selected", [])
    abilities_remaining = [ability for ability in _ABILITIES if ability not in abilities_selected]
    ability_to_select = 3 - len(abilities_selected)

    ability_table = EvTable(
        border="cells",
        valign="t",
        width=80,
    )
    ability_table.add_column("Ability", "|cStrength|n", "|cCunning|n", "|cWill|n", width=12)
    ability_table.add_column(
        "Explanation",
        "Determines how much damage you do with physical weapons, helps you earn more |cHP|n and"
            " |cStamina|n when gaining a level and affects carrying capacity.",
        "Affects your accuracy rating with physical attacks, evasion from physical attacks and can"
            " help at picking locks or sneaking around undetected.",
        "Affects your accuracy rating and damage with tech attacks, your resistance to tech attacks"
            " and helps you earn more |cMax System Load|n when gaining a level.",
    )
    ability_table.add_column(
        "Class w/ Primary",
        "Antifa Rioter\nGym Bro",
        "Gooner\nMin-Maxer\nShitposter",
        "Conspiracy Nut\nHacker\nPusher",
        width=18
    )
    ability_table.add_column(
        "Class w/ Secondary",
        "Conspiracy Nut\nGooner\nPusher",
        "Antifa Rioter\nHacker",
        "Gym Bro\nMin-Maxer\nShitposter",
        width=18
    )

    text = f"""Your character so far:
{tmp_character.show_sheet()}

Assign your |cAbility Scores|n. There are 3 ability scores in Deep Web Dungeons, strength (STR), cunning (CUN), and will (WIL), described below. You must assign one score with a +3 bonus, one with a +2 bonus, and one with a +1 bonus. When you select a race in the next section, you will be given bonuses and penalties depending on your race choice. These abilities will also rise with your level, at rates determined by your chosen character class' primary and secondary stats.

{ability_table}

Select the |cAbility Score|n by number to receive a +{ability_to_select} bonus below or Go Back.
"""

    options = []
    for ability in abilities_remaining:
        new_abilities_selected = abilities_selected + [ability]
        options.append(
            {
                "desc": f"|c{ability.capitalize()}|n",
                "goto": (
                    "node_apply_ability",
                    {"abilities_selected": new_abilities_selected, **kwargs}
                )
            }
        )

    options += [
        {
            "desc": "Go Back",
            "goto": ("node_show_genders", {"go_back": True, **kwargs})
        },
        {
            "desc": "Cancel and Return to Main Menu",
            "goto": ("node_end_chargen", {})
        },
    ]

    return (text, ""), options

def node_apply_ability(caller, raw_string, **kwargs):
    """ Apply the ability selected by the user. """

    abilities_selected = kwargs["abilities_selected"]
    tmp_character = kwargs["tmp_character"]

    if len(abilities_selected) == 1:
        setattr(tmp_character, abilities_selected[0], 3)

        return node_show_abilities(
            caller,
            "",
            tmp_character=tmp_character,
            abilities_selected=abilities_selected,
        )

    for ability in abilities_selected:
        if getattr(tmp_character, ability) == 0:
            setattr(tmp_character, ability, 2)

    ability_remaining = [ability for ability in _ABILITIES if ability not in abilities_selected][0]
    setattr(tmp_character, ability_remaining, 1)

    return node_show_races(caller, "", tmp_character=tmp_character)

def node_show_races(caller, raw_string, **kwargs):
    """ Let user select a race. """

    tmp_character = kwargs["tmp_character"]

    if kwargs.get("go_back"):
        tmp_character.apply_race(None)

    race_table = EvTable(
        border="cells",
        valign="t",
        width=80
    )

    races = list(RACES.values())
    race_data = each_slice(races, 2)

    for race_pair in race_data:
        race1 = race2 = Race(key="dummy", name="", desc="")

        if len(race_pair) == 2:
            race1, race2 = race_pair
        else:
            race1 = race_pair[0]

        race_table.add_row(f"|c{race1.name}|n", f"|c{race2.name}|n")
        race_table.add_row(race1.desc, race2.desc)

    text = f"""Your character so far:
{tmp_character.show_sheet()}

Select a |cRace|n. Your race is immutable and affects your starting ability scores.

{race_table}

Select one by number below or Go Back.
"""

    options = [
        {
            "desc": f"|c{race.name}|n",
            "goto": ("node_apply_race", {"race": race, **kwargs}),
        }
        for race in RACES.values()
    ] + [
        {
            "desc": "Random",
            "goto": ("node_apply_race", {"race": tmp_character.random_race(), **kwargs})
        },
        {
            "desc": "Go Back",
            "goto": ("node_show_abilities", {"go_back": True, **kwargs})
        },
        {
            "desc": "Cancel and Return to Main Menu",
            "goto": ("node_end_chargen", {})
        },
    ]

    return (text, ""), options

def node_apply_race(caller, raw_string, **kwargs):
    """ Apply the selected race. """

    race = kwargs.get('race')
    tmp_character = kwargs["tmp_character"]
    tmp_character.apply_race(race)

    if race.key == "human":
        return node_show_human_abilities(caller, "", tmp_character=tmp_character)

    return node_show_cclasses(caller, "", tmp_character=tmp_character)

def node_show_human_abilities(caller, raw_string, **kwargs):
    """
    If user chose Human race, they need to decide which abilities to apply race modifiers to.
    """

    tmp_character = kwargs["tmp_character"]
    bonus = kwargs.get("bonus", None)
    abilities_remaining = [ability for ability in _ABILITIES if ability != bonus]
    bonus_or_penalty = "+2 bonus"

    if bonus:
        bonus_or_penalty = "-2 penalty"

    text = f"""Your character so far:
{tmp_character.show_sheet()}

Since you are a |cHuman|n, you may choose which abilities to modify.
Chose which ability gets a {bonus_or_penalty}.

Select one by number below or Go Back.
"""

    options = [
        {
            "desc": f"|c{ability.capitalize()}|n",
            "goto": (
                "node_apply_human_abilities",
                {"bonus" if not bonus else "penalty": ability, **kwargs}
            ),
        }
        for ability in abilities_remaining
    ] + [
        {
            "desc": "Go Back",
            "goto": ("node_show_races", {"go_back": True, **kwargs})
        },
        {
            "desc": "Cancel and Return to Main Menu",
            "goto": ("node_end_chargen", {})
        },
    ]

    return (text, ""), options

def node_apply_human_abilities(caller, raw_string, **kwargs):
    """ Apply the chosen Human race modifiers to the character. """

    tmp_character = kwargs["tmp_character"]
    bonus = kwargs.get("bonus", None)
    penalty = kwargs.get("penalty", None)

    if penalty:
        # apply the the penalty and move to node_show_cclasses
        tmp_character.apply_ability_bonus(penalty, -2)
        return node_show_cclasses(caller, "", tmp_character=tmp_character)


    # apply the bonus and ask the user for the penalty
    tmp_character.apply_ability_bonus(bonus, 2)
    return node_show_human_abilities(caller, "", tmp_character=tmp_character, bonus=bonus)

def node_show_cclasses(caller, raw_string, **kwargs):
    """ Let user select a character class. """

    tmp_character = kwargs["tmp_character"]

    if kwargs.get("go_back"):
        tmp_character.apply_cclass(None)

    cclass_table = EvTable(
        border="cells",
        valign="t",
        width=80,
    )

    for cclass in list(CHARACTER_CLASSES.values()):
        cclass_table.add_row(f"|c{cclass.name}|n")
        cclass_table.add_row(cclass.desc)

    text = f"""Your character so far:
{tmp_character.show_sheet()}

Select a |cClass|n. Your class will define how you play the game - how your abilities will progress as you level, what gear you can use, and what skills you can learn.

{cclass_table}

Select one by number below or Go Back.
"""

    options = [
        {
            "desc": f"|c{cclass.name}|n",
            "goto": ("node_apply_cclass", {"cclass": cclass, **kwargs}),
        }
        for cclass in CHARACTER_CLASSES.values()
    ] + [
        {
            "desc": "Random",
            "goto": ("node_apply_cclass", {"cclass": tmp_character.random_cclass(), **kwargs})
        },
        {
            "desc": "Go Back",
            "goto": ("node_show_races", {"go_back": True, **kwargs})
        },
        {
            "desc": "Cancel and Return to Main Menu",
            "goto": ("node_end_chargen", {})
        },
    ]

    return (text, ""), options

def node_apply_cclass(caller, raw_string, **kwargs):
    """ Apply the selected character class. """

    cclass = kwargs.get('cclass')
    tmp_character = kwargs["tmp_character"]
    tmp_character.apply_cclass(cclass)

    return node_show_appearance(caller, "", tmp_character=tmp_character)

def node_show_appearance(caller, raw_string, **kwargs):
    """ Show appearance options for the character. """

    tmp_character = kwargs["tmp_character"]

    appearance_table = EvTable(
        border="cells",
        valign="t",
        width=80,
    )
    appearance_data = each_slice(_APPEARANCE_OPTIONS, 2)
    appearance1 = appearance2 = ""

    for appearance_pair in appearance_data:
        if len(appearance_pair) == 2:
            appearance1, appearance2 = appearance_pair
        else:
            appearance1 = appearance_pair[0]

        appearance_table.add_row(
            f"|c{appearance1.capitalize()}|n",
            f"|c{appearance2.capitalize()}|n"
        )
        appearance_table.add_row(
            f"{getattr(tmp_character, appearance1)}",
            f"{getattr(tmp_character, appearance2)}"
        )

    text = f"""Your character so far:
{tmp_character.show_sheet()}

Finally, decide on your appearance. This, along with your equipment, is what others will see when they `look` at you in game.

{appearance_table}

Select one by number below or Go Back.
"""

    options = [
        {
            "desc": f"|c{appearance_option.capitalize()}|n",
            "goto": (
                "node_show_appearance_option",
                {"appearance_option": appearance_option, **kwargs}
            ),
        }
        for appearance_option in _APPEARANCE_OPTIONS
    ] + [
        {
            "desc": "Go Back",
            "goto": ("node_show_cclasses", {"go_back": True, **kwargs})
        },
        {
            "desc": "Cancel and Return to Main Menu",
            "goto": ("node_end_chargen", {})
        },
        {
            "desc": "Accept and play the game!",
            "goto": ("node_apply_appearance", kwargs)
        },
    ]

    return (text, ""), options

def node_show_appearance_option(caller, raw_string, **kwargs):
    """ Show the options for a given appearance attribute. """

    tmp_character = kwargs["tmp_character"]
    appearance_option = kwargs["appearance_option"]

    text = f"""Your character so far:
{tmp_character.show_sheet()}

Choose an option for how your |c{appearance_option.capitalize()}|n will appear to other players.

Select one by number below or Go Back.
"""
    options = [
        {
            "desc": f"|c{appearance_value}|n",
            "goto": (
                "node_apply_appearance_option",
                {
                    "appearance_option": appearance_option,
                    "appearance_value": appearance_value,
                    **kwargs
                }
            ),
        }
        for appearance_value in chargen_tables.get(appearance_option)
    ] + [
        {
            "desc": "Random",
            "goto": (
                "node_apply_appearance_option",
                {"appearance_option": appearance_option, "appearance_value": "RANDOM", **kwargs}
            ),
        },
    ]

    return (text, ""), options

def node_apply_appearance_option(caller, raw_string, **kwargs):
    """ Apply a chosen value to an appearance option. """

    tmp_character = kwargs["tmp_character"]
    appearance_option = kwargs["appearance_option"]
    appearance_value = kwargs["appearance_value"]
    tmp_character.apply_appearance_attribute(appearance_option, appearance_value)

    return node_show_appearance(caller, "", tmp_character=tmp_character)

def node_apply_appearance(caller, raw_string, **kwargs):
    """ Apply the appearance to the character. """

    tmp_character = kwargs["tmp_character"]
    tmp_character.apply_appearance()

    return node_apply_character(caller, "", tmp_character=tmp_character)
