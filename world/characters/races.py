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

RACES = {
    "human": Race(
        key="human",
        name="Human",
        cunning_mod=1,
        desc="Humans are versatile and cunning. +1 CUN.",
    ),
    "dwarf":  Race(
        key="dwarf",
        name="Dwarf",
        strength_mod=1,
        desc="Dwarves are short and strong. +1 STR",
    ),
    "half_elf": Race(
        key="half_elf",
        name="Half Elf",
        will_mod=1,
        desc="Half-elves are intelligent and graceful. +1 WIL"
    ),
    "elf": Race(
        key="elf",
        name="Elf",
        strength_mod=-1,
        will_mod=2,
        desc="Elves are very intelligent but frail. -1 STR, +2 WIL",
    ),
    "goblin": Race(
        key="goblin",
        name="Goblin",
        cunning_mod=1,
        strength_mod=-2,
        will_mod=1,
        desc="Goblins are small, but cunning. -2 STR, +1 CUN, +1 WIL"
    ),
    "orc": Race(
        key="orc",
        name="Orc",
        strength_mod=2,
        will_mod=-1,
        desc="Orcs are very strong but not very bright. +2 STR, -1 WIL",
    ),
    "lizardman": Race(
        key="lizardman",
        name="Lizardman",
        cunning_mod=1,
        strength_mod=1,
        will_mod=-2,
        desc="Lizardmen are strong and quick, but quite stupid. +1 STR, +1 CUN, -2 WIL"
    ),
    "ratman": Race(
        key="ratman",
        name="Ratman",
        cunning_mod=2,
        strength_mod=-2,
        desc="Ratmen are very cunning, but weak. -2 STR, +2 CUN"
    )
}
