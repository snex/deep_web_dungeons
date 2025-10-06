"""
Handle all character level ups.
"""

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typeclasses.characters import BaseCharacter

class LevelsHandler:
    """
    Class to handle character level ups.
    """

    __slots__ = ('obj',)

    _ATTRIBUTE_CATEGORY = "levels"
    _LEVELS_FOR_STATS = {
        "primary": 4,
        "secondary": 5,
        "tertiary": 6,
    }

    def __init__(self, obj: 'BaseCharacter'):
        self.obj = obj
        if self.xp is None:
            self.xp = 0

        if self.level is None:
            self.level = 1

    @property
    def xp(self) -> int:
        """ Current XP of the character. """
        return self.obj.attributes.get("xp", category=self._ATTRIBUTE_CATEGORY)

    @xp.setter
    def xp(self, value: int):
        self.obj.attributes.add("xp", category=self._ATTRIBUTE_CATEGORY, value=value)

    @property
    def level(self) -> int:
        """ Current level of the character. """
        return self.obj.attributes.get("level", category=self._ATTRIBUTE_CATEGORY)

    @level.setter
    def level(self, value: int):
        self.obj.attributes.add("level", category=self._ATTRIBUTE_CATEGORY, value=value)

    def get_xp_for_next_level(self) -> int:
        """
        Returns the required xp for the next level.
        The equation is as follows:
            1000 * current_level ^ 1.5 rounded to the nearest 500.

        The first 5 levels should therefore be as follows:
            1          0
            2      2,500
            3      5,000
            4      8,000
            5     11,000
        """

        return int(round(1000 * (self.level ** 1.5) / 500) * 500)

    def add_xp(self, xp: int):
        """
        Add new XP.

        Args:
            xp (int): The amount of gained XP.
        """
        new_xp = self.xp + xp
        if new_xp > self.get_xp_for_next_level():
            self.xp = 0
            self.at_level_up()
        else:
            self.xp = new_xp

    def _level_hp(self):
        min_hp, max_hp = (1, 6)
        if cclass := self.obj.cclass:
            min_hp, max_hp = cclass.health_dice

        is_pc = self.obj.is_pc
        if is_pc:
            added_hp = max_hp
        else:
            added_hp = random.randint(min_hp, max_hp)

        self.obj.hp_max += added_hp

        # We add the new health directly unless the character is dead or dying.
        if self.obj.hp > 0:
            self.obj.hp += added_hp

    def _level_mana(self):
        min_mana, max_mana = (1, 6)
        if cclass := self.obj.cclass:
            min_mana, max_mana = cclass.mana_dice

        is_pc = self.obj.is_pc
        if is_pc:
            added_mana = max_mana
        else:
            added_mana = random.randint(min_mana, max_mana)

        self.obj.mana_max += added_mana
        self.obj.mana += added_mana

    def _level_stamina(self):
        min_stamina, max_stamina = (1, 6)
        if cclass := self.obj.cclass:
            min_stamina, max_stamina = cclass.stamina_dice

        is_pc = self.obj.is_pc
        if is_pc:
            added_stamina = max_stamina
        else:
            added_stamina = random.randint(min_stamina, max_stamina)

        self.obj.stamina_max += added_stamina
        self.obj.stamina += added_stamina

    def _level_stats(self):
        # By default, we use the lowest values, useful when generating mobs
        stats = {
            "strength": "tertiary",
            "cunning": "tertiary",
            "will": "tertiary"
        }

        # Get the adjustments based on the character class
        if cclass := self.obj.cclass:
            stats[cclass.primary_stat] = "primary"
            stats[cclass.secondary_stat] = "secondary"

        # We increase the stat when a threshold is reached
        added_stats = set()
        for stat, stat_focus in stats.items():
            levels_for_stat = self._LEVELS_FOR_STATS[stat_focus]
            if self.level % levels_for_stat != 0:
                continue

            stat_value = getattr(self.obj, stat, 1)
            setattr(self.obj, stat, stat_value + 1)
            added_stats.add(stat)

    def at_level_up(self):
        """
        Called when a character levels up
        """
        self.level = self.level + 1

        self._level_hp()
        self._level_mana()
        self._level_stamina()
        self._level_stats()

        # Send the player a nice message.
        is_pc = self.obj.is_pc
        if is_pc:
            msg = (
                "|wYou feel more powerful!\n"
            )
            self.obj.msg(msg)

        # If the object has a hook for additional level up effects, it is called here.
        if obj_hook := getattr(self.obj, "at_level_up", None):
            obj_hook()
