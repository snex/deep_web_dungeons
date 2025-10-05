"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""

from typing import TYPE_CHECKING

from evennia.contrib.game_systems.cooldowns import CooldownHandler
from evennia.objects.objects import DefaultCharacter
from evennia.typeclasses.attributes import AttributeProperty, NAttributeProperty
from evennia.utils.logger import log_err, log_trace
from evennia.utils.utils import inherits_from, lazy_property
from world import rules
from world.buffs import AbstractBuffHandler
from world.characters.classes import CharacterClasses, CharacterClass
from world.characters.races import Races, Race
from world.enums import Ability
from world.equipment import EquipmentError, EquipmentHandler
from world.levelling import LevelsHandler
from world.quests import QuestHandler


if TYPE_CHECKING:
    from world.combat import CombatHandler


# from world.utils import get_obj_stats


class BaseCharacter(DefaultCharacter):
    """ Base character is used for all characters, including PCs and NPCs. """
    is_pc = False

    hp = AttributeProperty(default=1)
    hp_max = AttributeProperty(default=1)
    mana = AttributeProperty(default=1)
    mana_max = AttributeProperty(default=1)
    stamina = AttributeProperty(default=1)
    stamina_max = AttributeProperty(default=1)

    strength = AttributeProperty(default=1)
    will = AttributeProperty(default=1)
    cunning = AttributeProperty(default=1)

    gender = AttributeProperty(default="male")
    cclass_key = AttributeProperty()
    race_key = AttributeProperty()

    coins = AttributeProperty(default=0)  # copper coins
    aggro = AttributeProperty(default="n")  # Defensive, Normal, or Aggressive (d/n/a)

    def get_ability(self, ability):
        """ Return the ability score of the ability supplied. """
        if ability not in Ability:
            raise TypeError(f"Invalid ability: {ability}")

        if ability == Ability.STR:
            return self.db.strength
        if ability == Ability.CUN:
            return self.db.cunning

        return self.db.will

    @property
    def cclass(self) -> CharacterClass | None:
        """ Return character's CharacterClass. """
        cclass = self.ndb.cclass
        if cclass is None:
            cclass = CharacterClasses.get(self.db.cclass_key)
            self.ndb.cclass = cclass

        return cclass

    @property
    def combat(self) -> 'CombatHandler | None':
        """ Return CombastHandler instance. """
        return self.ndb.combat

    @combat.setter
    def combat(self, value) -> None:
        self.ndb.combat = value


    @property
    def race(self) -> Race:
        """ Return character's race. """
        race = self.ndb.race
        if race is None:
            race = Races.get(self.db.race_key)
            self.ndb.race = race

        return race

    @lazy_property
    def cooldowns(self):
        """ Return CooldownHandler instance. """
        return CooldownHandler(self)

    @property
    def hurt_level(self):
        """
        String describing how hurt this character is.
        """
        percent = max(0, min(100, 100 * (self.hp / self.hp_max)))
        if 95 < percent <= 100:
            return "|gPerfect|n"
        if 80 < percent <= 95:
            return "|gScraped|n"
        if 60 < percent <= 80:
            return "|GBruised|n"
        if 45 < percent <= 60:
            return "|yHurt|n"
        if 30 < percent <= 45:
            return "|yWounded|n"
        if 15 < percent <= 30:
            return "|rBadly Wounded|n"
        if 1 < percent <= 15:
            return "|rBarely Hanging On|n"

        return "|RCollapsed!|n"

    @property
    def mana_level(self):
        """
        String describing how much mana the character has
        """
        percent = max(0, min(100, 100 * (self.mana / self.mana_max)))
        if 95 < percent <= 100:
            return "|gPerfect|n"
        if 80 < percent <= 95:
            return "|gWell Studied|n"
        if 60 < percent <= 80:
            return "|GStudied|n"
        if 45 < percent <= 60:
            return "|yLosing Concentration|n"
        if 30 < percent <= 45:
            return "|ySlightly Drained|n"
        if 15 < percent <= 30:
            return "|rDrained|n"
        if 1 < percent <= 15:
            return "|rBarely Hanging On|n"

        return "|REmpty!|n"

    @property
    def stamina_level(self):
        """
        String describing how tired this character is.
        """
        percent = max(0, min(100, 100 * (self.stamina / self.stamina_max)))
        if 95 < percent <= 100:
            return "|gPerfect|n"
        if 80 < percent <= 95:
            return "|gLight Sweat|n"
        if 60 < percent <= 80:
            return "|GSweaty|n"
        if 45 < percent <= 60:
            return "|yWinded|n"
        if 30 < percent <= 45:
            return "|yTired|n"
        if 15 < percent <= 30:
            return "|rExhausted|n"
        if 1 < percent <= 15:
            return "|rBarely Hanging On|n"

        return "|RCollapsed!|n"

    def heal(self, hp, healer=None):
        """
        Heal by a certain amount of HP.

        """
        damage = self.hp_max - self.hp
        healed = min(damage, hp)
        self.hp += healed

        if healer is self:
            self.msg("|gYou heal yourself and feel better.|n")
        elif healer:
            self.msg(f"|g{healer.key} heals you and you feel better.|n")
        else:
            self.msg("You are healed and feel better.")

    @lazy_property
    def equipment(self):
        """Allows to access equipment like char.equipment.worn"""
        return EquipmentHandler(self)

    @property
    def weapon(self):
        """ Character's current wielded weapon. """
        return self.equipment.weapon

    @property
    def armor(self):
        """ Character's current worn armor. """
        return self.equipment.armor

    @property
    def shield(self):
        """ Character's current worn shield. """
        return self.equipment.shield

    @lazy_property
    def levels(self):
        """Allows to access equipment like char.equipment.worn"""
        return LevelsHandler(self)

    @lazy_property
    def buffs(self):
        """ Get buffs on this character. """
        # TODO Implement
        return AbstractBuffHandler()

    def at_damage(self, damage, _attacker=None):
        """
        Called when attacked and taking damage.

        """
        self.hp -= damage
        if self.hp <= 0:
            self.at_defeat()

    def spend_stamina(self, amount):
        """
        Called when attacking and defending
        """
        self.stamina -= amount

    def spend_mana(self, amount):
        """
        Called when casting spells
        """
        self.mana -= amount

    def at_recovery(self):
        """
        Called periodically by the combat ticker

        """

        if self.stamina < self.stamina_max:
            self.stamina += max(self.strength, 1)

        if self.mana < self.mana_max:
            self.mana += max(self.will, 1)

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

    def pre_loot(self, defeated_enemy):
        """
        Called just before looting an enemy.

        Args:
            defeated_enemy (Object): The enemy soon to loot.

        Returns:
            bool: If False, no looting is allowed.

        """

    def at_do_loot(self, defeated_enemy):
        """
        Called when looting another entity.

        Args:
            defeated_enemy: The thing to loot.

        """
        defeated_enemy.at_looted(self)

    def post_loot(self, defeated_enemy):
        """
        Called just after having looted an enemy.

        Args:
            defeated_enemy (Object): The enemy just looted.

        """


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
