"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""

import bisect
from typing import TYPE_CHECKING

from evennia.objects.objects import DefaultCharacter
from evennia.typeclasses.attributes import AttributeProperty, NAttributeProperty
from evennia.utils.logger import log_err, log_trace
from evennia.utils.utils import inherits_from, lazy_property

from typeclasses.mixins import (
    HasRaceMixin,
    HasCClassMixin,
    CombatMixin,
    HasDrainableStatsMixin,
    HasEquipmentMixin,
)
from world import rules
from world.equipment import EquipmentError
from world.quests import QuestHandler


if TYPE_CHECKING:
    from world.combat import CombatHandler

class BaseCharacter(
    DefaultCharacter,
    HasRaceMixin,
    HasCClassMixin,
    CombatMixin,
    HasDrainableStatsMixin,
    HasEquipmentMixin,
):
    """ Base character is used for all characters, including PCs and NPCs. """
    is_pc = False

    gender = AttributeProperty(default="male")
    coins = AttributeProperty(default=0)  # copper coins
    aggro = AttributeProperty(default="n")  # Defensive, Normal, or Aggressive (d/n/a)

    def at_defeat(self):
        """
        Called when this living thing reaches HP 0.

        """
        # by default, defeat means death
        self.at_death()

    def at_death(self):
        """
        Called when this living thing dies.

        """
        if self.combat:
            self.combat.remove(self)

        self.location.msg_contents("$You() $conj(die).", from_obj=self)

    def at_pay(self, amount):
        """
        Get coins, but no more than we actually have.

        """
        amount = min(amount, self.coins)
        self.coins -= amount
        return amount

    def at_looted(self, looter):
        """
        Called when being looted (after defeat).

        Args:
            looter (Object): The one doing the looting.

        """
        max_steal = rules.dice.roll("1d10")
        stolen = self.at_pay(max_steal)

        looter.coins += stolen

        self.location.msg_contents(
            f"$You(looter) loots $You() for {stolen} coins!",
            from_obj=self,
            mapping={"looter": looter},
        )

    def at_do_loot(self, defeated_enemy):
        """
        Called when looting another entity.

        Args:
            defeated_enemy: The thing to loot.

        """
        defeated_enemy.at_looted(self)


class Character(BaseCharacter):
    """
    The Character typeclass for the game. This is the default typeclass new player
    characters are created as, so the EvAdventure player character is appropriate here.
    """

    is_pc = True

    hp = AttributeProperty(default=10)
    hp_max = AttributeProperty(default=10)
    mana = AttributeProperty(default=10)
    mana_max = AttributeProperty(default=10)
    stamina = AttributeProperty(default=4)
    stamina_max = AttributeProperty(default=4)

    # Combat State Tracking


    adelay = NAttributeProperty( default=0.0 ) # delay attacks until float time
    mdelay = NAttributeProperty( default=0.0 ) # delay movement until float time

    @property
    def mana_level(self):
        """
        String describing how much mana the character has
        """

        mana_levels = [
            (1, "|REmpty!|n"),
            (15, "|rBarely Hanging On|n"),
            (30, "|rDrained|n"),
            (45, "|ySlightly Drained|n"),
            (60, "|yLosing Concentration|n"),
            (80, "|GStudied|n"),
            (95, "|gWell Studied|n"),
            (100, "|gPerfect|n"),
        ]
        percent = max(0, min(100, 100 * (self.mana / self.mana_max)))

        return mana_levels[bisect.bisect_left(mana_levels, (percent,))][1]

    @property
    def stamina_level(self):
        """
        String describing how tired this character is.
        """

        stamina_levels = [
            (1, "|RCollapsed!|n"),
            (15, "|rBarely Hanging On|n"),
            (30, "|rExhausted|n"),
            (45, "|yTired|n"),
            (60, "|yWinded|n"),
            (80, "|GSweaty|n"),
            (95, "|gLight Sweat|n"),
            (100, "|gPerfect|n"),
        ]
        percent = max(0, min(100, 100 * (self.stamina / self.stamina_max)))

        return stamina_levels[bisect.bisect_left(stamina_levels, (percent,))][1]

    @lazy_property
    def quests(self):
        """Access and track quests"""
        return QuestHandler(self)

    def at_pre_object_receive(self, arriving_object, source_location, **kwargs):
        """
        Hook called by Evennia before moving an object here. Return False to abort move.

        Args:
            moved_object (Object): Object to move into this one (that is, into inventory).
            source_location (Object): Source location moved from.
            **kwargs: Passed from move operation; the `move_type` is useful; if someone is giving
                us something (`move_type=='give'`) we want to ask first.

        Returns:
            bool: If move should be allowed or not.

        """
        # this will raise EquipmentError if inventory is full
        return self.equipment.validate_slot_usage(arriving_object)

    def at_object_receive(self, moved_obj, source_location, move_type="move", **kwargs):
        """
        Hook called by Evennia as an object is moved here. We make sure it's added
        to the equipment handler.

        Args:
            moved_object (Object): Object to move into this one (that is, into inventory).
            source_location (Object): Source location moved from.
            **kwargs: Passed from move operation; unused here.

        """
        try:
            self.equipment.add(moved_obj)
        except EquipmentError as err:
            log_trace(f"at_object_receive error: {err}")

    def at_pre_object_leave(self, leaving_object, destination, **kwargs):
        """
        Hook called when dropping an item. We don't allow to drop weilded/worn items
        (need to unwield/remove them first). Return False to

        """
        return True

    def at_object_leave(self, moved_obj, _destination, move_type="move", **kwargs):
        """
        Called just before an object leaves from inside this object

        Args:
            moved_obj (Object): The object leaving
            destination (Object): Where `moved_obj` is going.
            **kwargs (dict): Arbitrary, optional arguments for users
                overriding the call (unused by default).

        """
        self.equipment.remove(moved_obj)

    def at_defeat(self):
        """
        This happens when character drops <= 0 HP. For Characters, this means rolling on
        the death table.

        """
        if self.location.allow_death:
            rules.dice.roll_death(self)
        else:
            self.location.msg_contents(
                "|y$You() $conj(yield), beaten and out of the fight.|n"
            )
            self.hp = self.hp_max

    def at_death(self):
        """
        Called when character dies.

        """
        self.location.msg_contents(
            "|r$You() $conj(collapse) in a heap.\nDeath embraces you ...|n",
            from_obj=self,
        )

    def at_pre_loot(self):
        """
        Called before allowing to loot. Return False to block enemy looting.
        """
        # don't allow looting in pvp
        return not self.location.allow_pvp

    def at_looted(self, looter):
        """
        Called when being looted.

        """

    def at_post_puppet(self, **kwargs):
        super().at_post_puppet(**kwargs)
        # Here we add Keybinds for Evelite Webclient so we can walk around with the numpad
        self.msg(
            key_cmds=(
                '', {
                    '7': 'northwest',
                    '8': 'north',
                    '9': 'northeast',
                    '1': 'southwest',
                    '2': 'south',
                    '3': 'southeast',
                    '4': 'west',
                    '6': 'east',
                    '5': 'look',
                }
            )
        )

    def at_post_move(self, source_location, move_type="move", **kwargs):
        obj = self

        if inherits_from(self, Character):
            # disable pylint on this as it's a dynamically created django method
            obj = self.account # pylint: disable=no-member

        if not obj:
            log_err(f"at_post_move called on a Character with no account: {self}")
            return

        if self.location.access(self, "view"):
            text = self.at_look(
                self.location,
                show_desc=obj.preferences.get("look_on_enter", True)
            )
            self.msg(text=(text, {"type": "look"}))

        if map_getter := getattr(self.location, 'get_map_display', None):
            # Send the map to the WebClient
            self.msg(map=map_getter(looker=self))
