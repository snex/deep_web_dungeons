""" Character classes list. """

from dataclasses import dataclass

@dataclass(frozen=True)
class StatDice:
    """ Dataclass for StatDice """
    health_dice: tuple[int, int]
    mana_dice: tuple[int, int]
    stamina_dice: tuple[int, int]


@dataclass(frozen=True)
class CharacterClass:
    """ Dataclass for a character class. """
    key: str
    name: str
    desc: str
    primary_stat: str
    secondary_stat: str
    stat_dice: StatDice

    def __str__(self):
        return self.name

CHARACTER_CLASSES = {
    "warrior": CharacterClass(
        key="warrior",
        name="Warrior",
        primary_stat="strength",
        secondary_stat="cunning",
        desc="Warriors are very strong in melee combat. They rely on strength and cunning, have"
             " excellent health, low mana, and excellent stamina.",
        stat_dice=StatDice(
            health_dice=(1, 10),
            mana_dice=(1, 6),
            stamina_dice=(1, 12),
        )
    ),
    "paladin": CharacterClass(
        key="paladin",
        name="Paladin",
        primary_stat="strength",
        secondary_stat="will",
        desc="Paladins are strong in melee combat and can use some divine spells. They rely on"
             " strength and will, have excellent health, low mana, and excellent stamina.",
        stat_dice=StatDice(
            health_dice=(1, 10),
            mana_dice=(1, 6),
            stamina_dice=(1, 12),
        )
    ),
    "rogue": CharacterClass(
        key="rogue",
        name="Rogue",
        primary_stat="cunning",
        secondary_stat="strength",
        desc="Rogues are adept fighters that prefer stealthy tactics and evasion. They rely on"
             " cunning and strength, have moderate health, moderate mana, and moderate stamina.",
        stat_dice=StatDice(
            health_dice=(1, 8),
            mana_dice=(1, 8),
            stamina_dice=(1, 10),
        )
    ),
    "bard": CharacterClass(
        key="bard",
        name="Bard",
        primary_stat="cunning",
        secondary_stat="will",
        desc="Bards focusing on buffing allies and debuffing enemies while being able to"
             " contribute in combat. They rely on cunning and will, have moderate health, moderate"
             " mana, and moderate stamina.",
        stat_dice=StatDice(
            health_dice=(1, 8),
            mana_dice=(1, 8),
            stamina_dice=(1, 10),
        )
    ),
    "shaman": CharacterClass(
        key="shaman",
        name="Shaman",
        primary_stat="will",
        secondary_stat="strength",
        desc="Shamans are spell casters capable of fighting with heavy weapons. They rely on will"
             " and strength, have low health, excellent mana, and low stamina.",
        stat_dice=StatDice(
            health_dice=(1, 6),
            mana_dice=(1, 10),
            stamina_dice=(1, 8),
        )
    ),
    "wizard": CharacterClass(
        key="wizard",
        name="Wizard",
        primary_stat="will",
        secondary_stat="cunning",
        desc="Wizards are focused spell casters. They rely on will and cunning, have low health,"
             " excellent mana, and low stamina.",
        stat_dice=StatDice(
            health_dice=(1, 6),
            mana_dice=(1, 10),
            stamina_dice=(1, 8),
        )
    )
}
