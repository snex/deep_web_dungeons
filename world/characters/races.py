""" Races list. """

from dataclasses import dataclass

@dataclass(frozen=True)
class Race:
    """ Dataclass for a race. """
    key: str
    name: str
    desc: str
    strength_mod: int = 0
    cunning_mod: int = 0
    will_mod: int = 0

    def __str__(self):
        return self.name

class Races:
    """ List of all races. """

    _cached_dict = None

    Human = Race(
        key="human",
        name="Human",
        cunning_mod=1,
        desc="Humans are versatile and cunning. +1 CUN.",
    )

    Dwarf = Race(
        key="dwarf",
        name="Dwarf",
        strength_mod=1,
        desc="Dwarves are short and strong. +1 STR",
    )

    HalfElf = Race(
        key="half_elf",
        name="Half Elf",
        will_mod=1,
        desc="Half-elves are intelligent and graceful. +1 WIL"
    )

    Elf = Race(
        key="elf",
        name="Elf",
        strength_mod=-1,
        will_mod=2,
        desc="Elves are very intelligent but frail. -1 STR, +2 WIL",
    )

    Goblin = Race(
        key="goblin",
        name="Goblin",
        cunning_mod=1,
        strength_mod=-2,
        will_mod=1,
        desc="Goblins are small, but cunning. -2 STR, +1 CUN, +1 WIL"
    )

    Orc = Race(
        key="orc",
        name="Orc",
        strength_mod=2,
        will_mod=-1,
        desc="Orcs are very strong but not very bright. +2 STR, -1 WIL",
    )

    Lizardman = Race(
        key="lizardman",
        name="Lizardman",
        cunning_mod=1,
        strength_mod=1,
        will_mod=-2,
        desc="Lizardmen are strong and quick, but quite stupid. +1 STR, +1 CUN, -2 WIL"
    )

    Ratman = Race(
        key="ratman",
        name="Ratman",
        cunning_mod=2,
        strength_mod=-2,
        desc="Ratmen are very cunning, but weak. -2 STR, +2 CUN"
    )

    @classmethod
    def _get_cached_dict(cls):
        if not cls._cached_dict:
            new_dict = {
                value.key: value for value in cls.__dict__.values() if isinstance(value, Race)
            }
            cls._cached_dict = new_dict

        return cls._cached_dict

    @classmethod
    def items(cls):
        """ Return all races keyed by key. """
        return cls._get_cached_dict().items()

    @classmethod
    def values(cls):
        """ Return all races. """
        return cls._get_cached_dict().values()

    @classmethod
    def get(cls, key):
        """ Return the race by key. """
        return cls._get_cached_dict().get(key)
