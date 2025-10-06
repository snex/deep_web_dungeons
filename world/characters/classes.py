""" Character classes list. """

from dataclasses import dataclass

@dataclass(frozen=True)
class CharacterClass:
    """ Dataclass for a character class. """
    key: str
    name: str
    desc: str
    primary_stat: str
    secondary_stat: str
    health_dice: tuple[int, int]
    mana_dice: tuple[int, int]
    stamina_dice: tuple[int, int]

    def __str__(self):
        return self.name

class CharacterClasses:
    """ List of all character classes. """
    _cached_dict = None

    Warrior = CharacterClass(
        key="warrior",
        name="Warrior",
        primary_stat="strength",
        secondary_stat="cunning",
        desc="Warriors are very strong in melee combat. They rely on strength and cunning, have"
             " excellent health, low mana, and excellent stamina.",
        health_dice=(1, 10),
        mana_dice=(1, 6),
        stamina_dice=(1, 12),
    )

    Paladin = CharacterClass(
        key="paladin",
        name="Paladin",
        primary_stat="strength",
        secondary_stat="will",
        desc="Paladins are strong in melee combat and can use some divine spells. They rely on"
             " strength and will, have excellent health, low mana, and excellent stamina.",
        health_dice=(1, 10),
        mana_dice=(1, 6),
        stamina_dice=(1, 12),
    )

    Rogue = CharacterClass(
        key="rogue",
        name="Rogue",
        primary_stat="cunning",
        secondary_stat="strength",
        desc="Rogues are adept fighters that prefer stealthy tactics and evasion. They rely on"
             " cunning and strength, have moderate health, moderate mana, and moderate stamina.",
        health_dice=(1, 8),
        mana_dice=(1, 8),
        stamina_dice=(1, 10),
    )

    Bard = CharacterClass(
        key="bard",
        name="Bard",
        primary_stat="cunning",
        secondary_stat="will",
        desc="Bards focusing on buffing allies and debuffing enemies while being able to"
             " contribute in combat. They rely on cunning and will, have moderate health, moderate"
             " mana, and moderate stamina.",
        health_dice=(1, 8),
        mana_dice=(1, 8),
        stamina_dice=(1, 10),
    )

    Shaman = CharacterClass(
        key="shaman",
        name="Shaman",
        primary_stat="will",
        secondary_stat="strength",
        desc="Shamans are spell casters capable of fighting with heavy weapons. They rely on will"
             " and strength, have low health, excellent mana, and low stamina.",
        health_dice=(1, 6),
        mana_dice=(1, 10),
        stamina_dice=(1, 8),
    )

    Wizard = CharacterClass(
        key="wizard",
        name="Wizard",
        primary_stat="will",
        secondary_stat="cunning",
        desc="Wizards are focused spell casters. They rely on will and cunning, have low health,"
             " excellent mana, and low stamina.",
        health_dice=(1, 6),
        mana_dice=(1, 10),
        stamina_dice=(1, 8),
    )

    @classmethod
    def _get_cached_dict(cls):
        if not cls._cached_dict:
            new_dict = {
                value.key: value for value in cls.__dict__.values()
                           if isinstance(value, CharacterClass)
            }
            cls._cached_dict = new_dict

        return cls._cached_dict

    @classmethod
    def items(cls):
        """ Return all character classes keyed by key. """
        return cls._get_cached_dict().items()

    @classmethod
    def values(cls):
        """ Return all character classes. """
        return cls._get_cached_dict().values()

    @classmethod
    def get(cls, key):
        """ Return the character class by key. """
        return cls._get_cached_dict().get(key)
