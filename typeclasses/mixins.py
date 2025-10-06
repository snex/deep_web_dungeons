"""
Mixins that can be imported to make an entity more character-like.

These are all added to BaseCharacter, but they can be individually added to anything
    to make it have the desired behaviors.
"""
import bisect

from evennia.contrib.game_systems.cooldowns import CooldownHandler
from evennia.typeclasses.attributes import AttributeProperty
from evennia.utils.utils import lazy_property

from world.buffs import AbstractBuffHandler
from world.characters.classes import CHARACTER_CLASSES, CharacterClass
from world.characters.races import RACES, Race
from world.equipment import EquipmentHandler
from world.levelling import LevelsHandler
from world.enums import Ability

class HasRaceMixin:
    """ Used in entities that have a race. All races have ability mods, so abilities are here. """
    race_key = AttributeProperty()

    strength = AttributeProperty(default=1)
    will = AttributeProperty(default=1)
    cunning = AttributeProperty(default=1)

    @property
    def race(self) -> Race:
        """ Return character's race. """
        race = self.ndb.race
        if race is None:
            race = RACES.get(self.db.race_key)
            self.ndb.race = race

        return race

    def get_ability(self, ability):
        """ Return the ability score of the ability supplied. """
        if ability not in Ability:
            raise TypeError(f"Invalid ability: {ability}")

        if ability == Ability.STR:
            return self.db.strength
        if ability == Ability.CUN:
            return self.db.cunning

        return self.db.will

class HasCClassMixin:
    """ Used in entities that have a character class. """
    cclass_key = AttributeProperty()

    @property
    def cclass(self) -> CharacterClass | None:
        """ Return character's CharacterClass. """
        cclass = self.ndb.cclass
        if cclass is None:
            cclass = CHARACTER_CLASSES.get(self.db.cclass_key)
            self.ndb.cclass = cclass

        return cclass

    @lazy_property
    def levels(self):
        """ Character level handler. """
        return LevelsHandler(self)

class CombatMixin:
    """ Used in entities that can engage in combat. """
    @property
    def combat(self) -> 'CombatHandler | None':
        """ Return CombastHandler instance. """
        return self.ndb.combat

    @combat.setter
    def combat(self, value) -> None:
        self.ndb.combat = value

    @lazy_property
    def cooldowns(self):
        """ Return CooldownHandler instance. """
        return CooldownHandler(self)

    @lazy_property
    def buffs(self):
        """ Get buffs on this character. """
        # TODO Implement
        return AbstractBuffHandler()

class HasDrainableStatsMixin:
    """ Used in entities that have HP, mana, and stamina """
    hp = AttributeProperty(default=1)
    hp_max = AttributeProperty(default=1)

    mana = AttributeProperty(default=1)
    mana_max = AttributeProperty(default=1)

    stamina = AttributeProperty(default=1)
    stamina_max = AttributeProperty(default=1)

    def full_recovery(self):
        """ Recover all drainable stats to the max instantly. """
        self.hp = self.hp_max
        self.mana = self.mana_max
        self.stamina = self.stamina_max

    @property
    def hurt_level(self):
        """
        String describing how hurt this character is.
        """

        hurt_levels = [
            (1, "|RCollapsed!|n"),
            (15, "|rBarely Hanging On|n"),
            (30, "|rBadly Wounded|n"),
            (45, "|yWounded|n"),
            (60, "|yHurt|n"),
            (80, "|GBruised|n"),
            (95, "|gScraped|n"),
            (100, "|gPerfect|n"),
        ]
        percent = max(0, min(100, 100 * (self.hp / self.hp_max)))

        return hurt_levels[bisect.bisect_left(hurt_levels, (percent,))][1]

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

    def at_damage(self, damage, _attacker=None):
        """
        Called when attacked and taking damage.

        """
        self.hp -= damage
        if self.hp <= 0:
            self.at_defeat()

    def spend_mana(self, amount):
        """
        Called when casting spells
        """
        self.mana -= amount

    def spend_stamina(self, amount):
        """
        Called when attacking and defending
        """
        self.stamina -= amount

    def at_recovery(self):
        """
        Called periodically by the combat ticker

        """

        if self.stamina < self.stamina_max:
            self.stamina += max(self.strength, 1)

        if self.mana < self.mana_max:
            self.mana += max(self.will, 1)

class HasEquipmentMixin:
    """ Used in entities that can have equipment. """
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
