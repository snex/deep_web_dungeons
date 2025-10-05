"""
Place for game-wide enums.
"""

from enum import IntEnum, Enum


class Criticals(Enum):
    """ Critical success and failure. """
    CRITICAL_FAILURE = "critical_failure"
    CRITICAL_SUCCESS = "critical_success"

class Ability(Enum):
    """
    Ability stats.
    """

    STR = "strength"
    CUN = "cunning"
    WIL = "will"

class WieldLocation(Enum):
    """
    Wield (or wear) locations.

    """

    # wield/wear location
    BACKPACK = "backpack"
    WEAPON_HAND = "weapon_hand"
    SHIELD_HAND = "shield_hand"
    TWO_HANDS = "two_handed_weapons"
    BODY = "body"  # armor
    HEAD = "head"  # helmets


class ObjType(Enum):
    """
    Object types

    """

    WEAPON = "weapon"
    ARMOR = "armor"
    SHIELD = "shield"
    HELMET = "helmet"
    CONSUMABLE = "consumable"
    GEAR = "gear"
    MAGIC = "magic"
    QUEST = "quest"
    TREASURE = "treasure"

class Allegiance(Enum):
    """
    Allegiance flags.
    """

    ALLEGIANCE_HOSTILE = "hostile"
    ALLEGIANCE_NEUTRAL = "neutral"
    ALLEGIANCE_FRIENDLY = "friendly"

class CombatRange(IntEnum):
    """
    Maximum combat range values
    """
    MELEE = 1
    REACH = 2
    SHORT = 3
    MEDIUM = 4
    RANGED = 6


class AttackType(IntEnum):
    """
    Attack types.
    """
    MELEE = 1
    RANGED = 2
    THROWN = 3
    MAGIC = 4


class DefenseType(Enum):
    """
    Defense types.
    """
    STR = "strength"
    CUN = "cunning"
    WIL = "will"
    ARMOR = "armor"

class CardinalDirections(Enum):
    """
    Cardinal directions on the compass.
    """

    NORTH = "north"
    NORTHEAST = "northeast"
    EAST = "east"
    SOUTHEAST = "southeast"
    SOUTH = "south"
    SOUTHWEST = "southwest"
    WEST = "west"
    NORTHWEST = "northwest"
