"""
Object

The Object is the base class for things in the game world.

Note that the default Character, Room and Exit do not inherit from Object.
"""
import inflect

from evennia import AttributeProperty
from evennia.objects.objects import DefaultObject
from evennia.prototypes.spawner import spawn
from evennia.utils import ansi, logger
from evennia.utils.utils import compress_whitespace, make_iter

from world.common import item_prototypes
from world.enums import (
    Ability,
    AttackType,
    CombatRange,
    DefenseType,
    ObjType,
    QuantumLatticeType,
    WieldLocation,
)
from world.utils import get_obj_stats, rainbow

_INFLECT = inflect.engine()

class Object(DefaultObject):
    """
    Base in-game entity.

    """

    # inventory management
    inventory_use_slot = AttributeProperty(WieldLocation.BACKPACK)
    # how many inventory slots it uses (can be a fraction)
    size = AttributeProperty(1)
    value = AttributeProperty(0)
    material = AttributeProperty(default="")
    tier = AttributeProperty(default=0)
    display_name = AttributeProperty(default=None)
    color = AttributeProperty(default="|n")

    # can also be an iterable, for adding multiple obj-type tags
    obj_type = ObjType.GEAR

    def at_object_creation(self):
        for obj_type in make_iter(self.obj_type):
            self.tags.add(obj_type.value, category="obj_type")
        self.locks.add("view: not_in_foreign_backpack()")

    def _apply_color(self, custom_text=None):
        """
        Function to apply a color to an object's name.
        Subclasses can inject custom functions to do more than just single colors,
        e.g. rainbow effect.

        Args: custom_text - if supplied, the color function should be applied to the custom_text
        """

        display_name = custom_text or self.display_name or self.name

        return display_name

    def get_display_name(self, looker=None, **kwargs):
        """ Apply the proper color function to the object's name before returning it. """
        return self._apply_color(kwargs.get("custom_text", None))

    def get_numbered_name(self, count, looker, **kwargs):
        """
        Return the numbered (singular, plural) forms of this object's key. This is by default called
        by return_appearance and is used for grouping multiple same-named of this object. Note that
        this will be called on *every* member of a group even though the plural name will be only
        shown once. Also the singular display version, such as 'an apple', 'a tree' is determined
        from this method.

        Overridden here to apply colors.

        Args:
            count (int): Number of objects of this type
            looker (DefaultObject): Onlooker. Not used by default.

        Keyword Args:
            key (str): Optional key to pluralize. If not given, the object's `.get_display_name()`
                method is used.
            return_string (bool): If `True`, return only the singular form if count is 0,1 or
                the plural form otherwise. If `False` (default), return both forms as a tuple.
            no_article (bool): If `True`, do not return an article if `count` is 1.

        Returns:
            tuple: This is a tuple `(str, str)` with the singular and plural forms of the key
            including the count.

        Examples:
        ::

            obj.get_numbered_name(3, looker, key="foo")
                  -> ("a foo", "three foos")
            obj.get_numbered_name(1, looker, key="Foobert", return_string=True)
                  -> "a Foobert"
            obj.get_numbered_name(1, looker, key="Foobert", return_string=True, no_article=True)
                  -> "Foobert"
        """
        key = kwargs.get("key", self.get_display_name(looker))
        raw_key = ansi.ANSIString(key)  # this is needed to allow inflection of colored names
        try:
            plural = _INFLECT.plural(raw_key, count)
            plural = f"{_INFLECT.number_to_words(count, threshold=12)} {plural}"
        except IndexError:
            # this is raised by inflect if the input is not a proper noun
            plural = raw_key
        singular = _INFLECT.an(raw_key)
        if not self.aliases.get(plural, category=self.plural_category):
            # we need to wipe any old plurals/an/a in case key changed in the interrim
            self.aliases.clear(category=self.plural_category)
            self.aliases.add(plural, category=self.plural_category)
            # save the singular form as an alias here too so we can display "an egg" and also
            # look at 'an egg'.
            self.aliases.add(singular, category=self.plural_category)

        if kwargs.get("no_article") and count == 1:
            if kwargs.get("return_string"):
                return self._apply_color(custom_text=raw_key)
            return self._apply_color(custom_text=raw_key), self._apply_color(custom_text=raw_key)

        if kwargs.get("return_string"):
            if count == 1:
                return self._apply_color(custom_text=singular)

            return self._apply_color(custom_text=plural)

        return self._apply_color(custom_text=singular), self._apply_color(custom_text=plural)

    def return_appearance(self, looker, **kwargs):
        return get_obj_stats(self, owner=looker)

    def has_obj_type(self, objtype):
        """
        Check if object is of a particular type.

        typeobj_enum (enum.ObjType): A type to check, like enums.TypeObj.TREASURE.

        """
        return objtype.value in make_iter(self.obj_type)

    def get_help(self):
        """
        Get help text for the item.

        Returns:
            str: The help text, by default taken from the `.help_text` property.

        """
        return "No help for this item."


class ObjectFiller(Object):
    """
    In _Knave_, the inventory slots act as an extra measure of how you are affected by
    various averse effects. For example, mud or water could fill up some of your inventory
    slots and make the equipment there unusable until you cleaned it. Inventory is also
    used to track how long you can stay under water etc - the fewer empty slots you have,
    the less time you can stay under water due to carrying so much stuff with you.

    This class represents such an effect filling up an empty slot. It has a quality of 0,
    meaning it's unusable.

    """

    obj_type = ObjType.QUEST.value  # can't be sold
    quality = AttributeProperty(0)

class QuantumLatticeObject(Object):
    """ A Quantum Lattice, the base currency items. """

    obj_type = ObjType.CURRENCY
    ql_type = AttributeProperty(default=QuantumLatticeType.DUST_SHARD)
    size = AttributeProperty(0.01)

    _QL_TIERS = {
        QuantumLatticeType.DUST_SHARD: {
            "prototype": item_prototypes.QL_DUST_SHARD,
            "color": "|x",
        },
        QuantumLatticeType.STATIC_BLOOM: {
            "prototype": item_prototypes.QL_STATIC_BLOOM,
            "color": "|c",
        },
        QuantumLatticeType.ECHO_STONE: {
            "prototype": item_prototypes.QL_ECHO_STONE,
            "color": "|G",
        },
        QuantumLatticeType.RESONANCE_CRYSTAL: {
            "prototype": item_prototypes.QL_RESONANCE_CRYSTAL,
            "color": "|y",
        },
        QuantumLatticeType.SINGULARITY_SHARD: {
            "prototype": item_prototypes.QL_SINGULARITY_SHARD,
            "color": "|[x|X",
        },
        QuantumLatticeType.PHASE_PEARL: {
            "prototype": item_prototypes.QL_PHASE_PEARL,
            "color": "|530",
        },
        QuantumLatticeType.VOID_SPARK: {
            "prototype": item_prototypes.QL_VOID_SPARK,
            "color": "|M",
        },
        QuantumLatticeType.CHROMATIC_HEART: {
            "prototype": item_prototypes.QL_CHROMATIC_HEART,
        },
        QuantumLatticeType.NEXUS_DIAMOND: {
            "prototype": item_prototypes.QL_NEXUS_DIAMOND,
            "color": "|[w|x",
        }
    }

    def _apply_color(self, custom_text=None):
        """ Apply color based on QuantumLatticeType. """

        if self.ql_type == QuantumLatticeType.CHROMATIC_HEART:
            return rainbow(custom_text or self.name)

        color = self._QL_TIERS[self.ql_type]["color"]

        return compress_whitespace(f"{color}{custom_text or self.name}|n")

    def combine(self, owner):
        """ Combines 3 of a type of QL into the next level of QL. """

        next_tier = self._get_next_tier()

        if not next_tier:
            return f"{self.get_display_name()} cannot be combined."

        candidates = owner.search(
            self.key,
            quiet=True,
            candidates=owner.equipment.all(only_objs=True),
            typeclass=QuantumLatticeObject
        )[:3]
        old_ql_display_name = self.get_display_name(custom_text=_INFLECT.plural(self.key, 3))

        if len(candidates) < 3:
            return f"You need 3 {old_ql_display_name} to combine."

        for old_ql in candidates:
            owner.equipment.remove(old_ql)
            old_ql.delete()

        new_ql = spawn(
            self._QL_TIERS[next_tier]["prototype"] | {
                "location": owner,
            }
        )[0]
        owner.equipment.move(new_ql)
        return f"You combine 3 {old_ql_display_name} into {new_ql.get_display_name()}."

    def _get_next_tier(self):
        """ Gets the next tier of QuantumLattice from the current one. """

        tiers = list(self._QL_TIERS.keys())
        next_tier_idx = tiers.index(self.ql_type) + 1

        if next_tier_idx >= len(tiers):
            return None

        return tiers[next_tier_idx]

class QuestObject(Object):
    """
    A quest object. These cannot be sold and only be used for quest resolution.

    """

    obj_type = ObjType.QUEST
    value = AttributeProperty(0)


class TreasureObject(Object):
    """
    A 'treasure' is mainly useful to sell for coin.

    """

    obj_type = ObjType.TREASURE
    value = AttributeProperty(100)


class ConsumableObject(Object):
    """
    Item that can be 'used up', like a potion or food. Weapons, armor etc does not
    have a limited usage in this way.

    """

    obj_type = ObjType.CONSUMABLE
    size = AttributeProperty(0.25)
    uses = AttributeProperty(default=1)

    def at_use(self, user, *args, **kwargs):
        """
        Consume a 'use' of this item. Once it reaches 0 uses, it should normally
        not be usable anymore and probably be deleted.

        Args:
            user (Object): The one using the item.
            *args, **kwargs: Extra arguments depending on the usage and item.

        """

    def at_post_use(self, user, *args, **kwargs):
        """
        Called after this item was used.

        Args:
            user (Object): The one using the item.
            *args, **kwargs: Optional arguments.

        """
        self.uses -= 1
        if self.uses <= 0:
            user.msg(f"{self.key} was used up.")
            self.delete()

class ConsumableHealingObject(ConsumableObject):
    """
    Item that heals when used.
    """

    heal_value = AttributeProperty(default=3)
    consume_method = AttributeProperty(default="drink")

    def at_use(self, user, *args, **kwargs):
        """
        Heal the user `heal_value` HP on use.
        """

        user.heal(self.heal_value)

class EquipmentObject(Object):
    """ Base class for all equippable items. """

    _TIER_DISPLAY_COLORS = [
        "|n", # Tier 0 items are not equippable and display in normal text
        "|x", # Tier 1 items have no affixes
        "|C", # Tier 2 items have 1 or 2 affixes
        "|Y", # Tier 3 items have 3 or 4 affixes
        "|g", # Tier 4 items have 5 or 6 affixes
    ]

    def _apply_color(self, custom_text=None):
        """ Apply color based on equipment tier. """

        material = getattr(getattr(self, "material", ""), "value", None)
        color = self._TIER_DISPLAY_COLORS[self.tier]
        display_name = self.display_name or self.name

        if custom_text:
            return f"{color}{custom_text}|n"

        if not material:
            logger.log_err("Somehow we got an EquipmentObject with no material!")

            return f"{color}{display_name}|n"

        return compress_whitespace(f"{color}{material} {display_name}|n")

class WeaponObject(EquipmentObject):
    """
    Base weapon class for all  weapons.

    """

    obj_type = ObjType.WEAPON
    inventory_use_slot: WieldLocation = AttributeProperty(WieldLocation.WEAPON_HAND)
    quality: int = AttributeProperty(3)

    # maximum attack range for this weapon
    attack_range: CombatRange = AttributeProperty(CombatRange.MELEE)
    attack_type: AttackType = AttributeProperty(Ability.STR)
    # what defense stat of the enemy it must defeat
    defense_type: Ability = AttributeProperty(DefenseType.ARMOR)

    damage_roll: str = AttributeProperty("1d4")
    stamina_cost: int = AttributeProperty(2)
    cooldown: int = AttributeProperty(2)

    parry: bool = AttributeProperty(False)

    def can_parry(self):
        """ Can this weapon parry attacks? """
        return self.parry

class WeaponBareHands(WeaponObject):
    """
    Special class for bare hands when no weapon is wielded.
    """
    obj_type = ObjType.WEAPON
    inventory_use_slot = WieldLocation.WEAPON_HAND
    attack_type = Ability.STR
    defense_type = DefenseType.ARMOR
    damage_roll = "1d4"

    def can_parry(self):
        return False

class ArmorObject(EquipmentObject):
    """
    Base class for all wearable Armors.

    """

    obj_type = ObjType.ARMOR
    inventory_use_slot = WieldLocation.BODY

    armor = AttributeProperty(1)
    quality = AttributeProperty(3)


class Shield(ArmorObject):
    """
    Base class for all Shields.

    """

    obj_type = ObjType.SHIELD
    inventory_use_slot = WieldLocation.SHIELD_HAND


class Helmet(ArmorObject):
    """
    Base class for all Helmets.

    """

    obj_type = ObjType.HELMET
    inventory_use_slot = WieldLocation.HEAD
