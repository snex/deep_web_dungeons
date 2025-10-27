"""
Object

The Object is the base class for things in the game world.

Note that the default Character, Room and Exit do not inherit from Object.
"""
import bisect
import time

import inflect

from evennia import AttributeProperty
from evennia.objects.objects import DefaultObject
from evennia.prototypes.spawner import spawn
from evennia.utils import ansi, logger
from evennia.utils.utils import compress_whitespace, inherits_from, make_iter

from world import quantum_lattices
from world.affixes import AFFIXES
from world.characters.classes import CHARACTER_CLASSES
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
from world.utils import get_obj_stats

_INFLECT = inflect.engine()

class NoneObject:
    """
    This exists for situations where we expect an object but no object was available
        so that chained methods don't crash.

        e.g. me.weapon.get_display_name()
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(NoneObject, cls).__new__(cls)
        return cls.instance

    def __bool__(self):
        return False

    def __str__(self):
        return "None"

    def get_display_name(self, *args, **kwargs):
        """ Return 'None' no matter what. """
        return "None"

class Object(DefaultObject):
    """
    Base in-game entity.

    """

    created_at = AttributeProperty(default=0)
    # inventory management
    inventory_use_slot = AttributeProperty(WieldLocation.BACKPACK)
    # how many inventory slots it uses (can be a fraction)
    size = AttributeProperty(1)
    value = AttributeProperty(0)
    material = AttributeProperty(default="")
    tier = AttributeProperty(default=0)
    display_name = AttributeProperty(default=None)

    # can also be an iterable, for adding multiple obj-type tags
    obj_type = ObjType.GEAR

    def __str__(self):
        return self.get_display_name()

    def at_object_creation(self):
        self.created_at = int(time.time())
        for obj_type in make_iter(self.obj_type):
            self.tags.add(obj_type.value, category="obj_type")
        self.locks.add("view: not_in_foreign_backpack()")
        self.locks.add("wear_wield: character_can_equip_item()")

    def at_object_delete(self):
        if hasattr(self.location, "equipment"):
            self.location.equipment.remove(self)

        return True

    def at_pre_use(self, *args, **kwargs):
        """
        called before an object is used.
        returns `False` if object cannot be used. override in subclasses.
        """
        kwargs["caller"].msg("Nothing happens.")
        return False

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
            plural = f"{_INFLECT.number_to_words(count, threshold=12)} {plural}".strip()
        except IndexError:
            # this is raised by inflect if the input is not a proper noun
            plural = raw_key
        singular = _INFLECT.an(raw_key).strip()
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

    @property
    def damage_level(self):
        """ base Objects don't get damaged. override this in subclasses """
        return "|gPerfect|n"

    def get_item_type_stats(self, _looker=None):
        """
        a dict of item stats special to a given object type. override in subclasses

        when overriding, you likely want to merge with super()
        """
        return {}

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
        },
        QuantumLatticeType.STATIC_BLOOM: {
            "prototype": item_prototypes.QL_STATIC_BLOOM,
        },
        QuantumLatticeType.ECHO_STONE: {
            "prototype": item_prototypes.QL_ECHO_STONE,
        },
        QuantumLatticeType.RESONANCE_CRYSTAL: {
            "prototype": item_prototypes.QL_RESONANCE_CRYSTAL,
        },
        QuantumLatticeType.SINGULARITY_SHARD: {
            "prototype": item_prototypes.QL_SINGULARITY_SHARD,
        },
        QuantumLatticeType.PHASE_PEARL: {
            "prototype": item_prototypes.QL_PHASE_PEARL,
        },
        QuantumLatticeType.VOID_SPARK: {
            "prototype": item_prototypes.QL_VOID_SPARK,
        },
        QuantumLatticeType.CHROMATIC_HEART: {
            "prototype": item_prototypes.QL_CHROMATIC_HEART,
        },
        QuantumLatticeType.NEXUS_DIAMOND: {
            "prototype": item_prototypes.QL_NEXUS_DIAMOND,
        }
    }

    def at_pre_use(self, *args, **kwargs):
        item = args[0]
        caller = kwargs["caller"]

        if not item:
            caller.msg(f"What do you want to use {self} on?")
            return False

        try:
            ql = getattr(quantum_lattices, self.key.title().replace(" ", ""))(self)
            if not ql.can_use(item):
                caller.msg(f"You can't use {self} on {item}")
                return False
            return True
        except AttributeError:
            logger.log_err(f"Tried to use a QuantumLatticeObject with unknown key: {self.key}")
            return False

    def _apply_color(self, custom_text=None):
        """ Apply color based on QuantumLatticeType. """

        try:
            ql = getattr(quantum_lattices, self.key.title().replace(" ", ""))(self)
            return ql.get_display_name(custom_text)
        except AttributeError:
            logger.log_err(f"Tried to use a QuantumLatticeObject with unknown key: {self.key}")
            return ""

    def combine(self, owner):
        """ Combines 3 of a type of QL into the next level of QL. """

        next_tier = self._get_next_tier()

        if not next_tier:
            return f"{self} cannot be combined."

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
            old_ql.delete()

        new_ql = spawn(
            self._QL_TIERS[next_tier]["prototype"] | {
                "location": owner,
            }
        )[0]
        owner.equipment.move(new_ql)
        return f"You combine 3 {old_ql_display_name} into {new_ql}."

    def use(self, *args, **kwargs):
        """
        use the QL by calling a specific class per QL

        at_post_use should be called inside the class so it can pass the msg and perform any
        other side effects
        """
        item = args[0]
        caller = kwargs["caller"]

        try:
            ql = getattr(quantum_lattices, self.key.title().replace(" ", ""))(self)
            ql.use(caller, item)
        except AttributeError:
            logger.log_err(f"Tried to use a QuantumLatticeObject with unknown key: {self.key}")

    def at_post_use(self, caller, msg):
        """ call after using a QL. message the caller what it did and delete it """
        caller.msg(msg)
        self.delete()

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

    def get_item_type_stats(self, _looker=None):
        """ ConsumableObjects have uses count """
        return {
            "Uses": self.uses
        }

class ScrapObject(Object):
    """ Scrap is used to repear equipment. """

    obj_type = ObjType.CONSUMABLE
    size = AttributeProperty(default=0.01)
    repair_amount = AttributeProperty(default=10)

    def at_pre_use(self, *args, **kwargs):
        """ test if scrap can be used on the item """
        item = args[0]
        caller = kwargs["caller"]

        if not item:
            caller.msg(f"What do you want to use {self} on?")
            return False

        if not inherits_from(item, EquipmentObject):
            caller.msg(f"You can't use {self} on {item}.")
            return False

        if item.quality == 100:
            caller.msg(f"{item} is already in {item.damage_level} condition.")
            return False

        return True

    def use(self, *args, **kwargs):
        """ use the scrap, repairing some gear """
        item = args[0]
        caller = kwargs["caller"]

        caller.msg(f"You use {self} to repair {item}")
        item.repair(self.repair_amount)
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

    allowed_classes = AttributeProperty(default=list(CHARACTER_CLASSES.values()))
    required_level = AttributeProperty(default=1)
    quality = AttributeProperty(default=100)
    affixes = AttributeProperty(default=[])
    scrap_base_value = AttributeProperty(default=1)

    _TIER_DISPLAY_COLORS = [
        "|n", # Tier 0 items are not equippable and display in normal text
        "|x", # Tier 1 items have no affixes
        "|C", # Tier 2 items have 1 or 2 affixes
        "|Y", # Tier 3 items have 3 or 4 affixes
        "|g", # Tier 4 items have 5 or 6 affixes
    ]

    def _display_prefixes(self):
        return " ".join([
            AFFIXES[prefix]["desc"]
            for prefix in sorted(getattr(self, "affixes", []))
            if prefix.startswith("prefix_")
        ])

    def _display_suffixes(self):
        suffixes = [
            AFFIXES[suffix]["desc"]
            for suffix in sorted(getattr(self, "affixes", []))
            if suffix.startswith("suffix_")
        ]
        if not suffixes:
            return ""

        if len(suffixes) == 1:
            return f"of {suffixes[0]}"

        joined_suffixes = ", ".join(suffixes[:-1]) + " and " + suffixes[-1]
        return f"of {joined_suffixes}"

    def _apply_color(self, custom_text=None):
        """ Apply color based on equipment tier. """

        material = getattr(getattr(self, "material", ""), "value", None)
        color = self._TIER_DISPLAY_COLORS[self.tier]
        display_name = self.display_name or self.name

        if custom_text:
            return f"{color}{custom_text}|n"

        if not material:
            logger.log_err(
                f"Somehow we got an EquipmentObject with no material! {self.key}({self.dbid})"
            )

            return f"{color}{display_name}|n"

        uncolored_name = compress_whitespace(
            f"{self._display_prefixes()} {material} {display_name} {self._display_suffixes()}"
        ).strip()
        return f"{color}{uncolored_name}|n"

    @property
    def damage_level(self):
        """ String describing how damaged an object is """

        damage_levels = [
            (1, "|RBroken!|n"),
            (15, "|rFalling Apart|n"),
            (30, "|rDamaged|n"),
            (45, "|yDented|n"),
            (60, "|yWorn|n"),
            (80, "|GScratched|n"),
            (95, "|gScuffed|n"),
            (100, "|gPerfect|n"),
        ]
        percent = max(0, min(100, 100 * (self.quality / 100)))

        return damage_levels[bisect.bisect_left(damage_levels, (percent,))][1]

    @property
    def scrap_value(self):
        """ Amount of scrap vendors will give you for this item """
        return self.tier * self.scrap_base_value + int(self.required_level / 10)

    @property
    def vendor_price(self):
        """ Price vendors charge to sell this item """
        price_l = 2 * self.scrap_value * ["scrap"]

        match self.tier:
            case 2:
                price_l.extend(2 * ["resonance crystal"])
            case 3:
                price_l.extend(2 * ["resonance crystal", "phase pearl"])
            case 4:
                price_l.extend(2 * ["resonance crystal", "phase pearl", "chromatic heart"])

        price_l.extend(len(self.affixes) * ["echo stone"])

        price_d = {}
        for currency in sorted(price_l):
            if not price_d.get(currency, None):
                price_d[currency] = {"count": 0}
            price_d[currency]["count"] += 1
            price_d[currency]["ql"] = quantum_lattices.QuantumLattice.from_name(currency)

        return price_d

    def repair(self, amount):
        """ repair the equipment, up to a max of 100 """
        self.quality = min(100, self.quality + amount)
        self.save()

    def get_item_type_stats(self, looker=None):
        """
        EquipmentObjects have allowed classes and required level

        Display in red if the looker does not meet the reqs, green if they do
        """

        req_level = self.required_level

        if looker and looker.levels.level < req_level:
            req_level = f"|r{req_level}|n"
        else:
            req_level = f"|g{req_level}|n"

        allowed_cclasses = ", ".join([
            f"|g{cclass.name}|n" if looker and looker.cclass == cclass else f"|r{cclass.name}|n"
            for cclass in self.allowed_classes
        ])

        return super().get_item_type_stats(looker) | {
            "Req. Level": req_level,
            "Allowed Classes": allowed_cclasses,
        }

class WeaponObject(EquipmentObject):
    """
    Base weapon class for all  weapons.

    """

    obj_type = ObjType.WEAPON
    inventory_use_slot: WieldLocation = AttributeProperty(WieldLocation.WEAPON_HAND)

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

    def get_item_type_stats(self, looker=None):
        """
        WeaponObjects have the following:
            Range
            Attack Type (what stat of yours boosts this weapon)
            Defense Type (what stat of the enemy you roll against)
            Cooldown (number of seconds before you can attack with this again)
            Parry (whether this weapon can parry attacks)
        """
        return {
            "Range": self.attack_range.value,
            "Att. Type": self.attack_type.value,
            "Def. Type": self.defense_type.value,
            "Cooldown": f"{self.cooldown}s",
            "Parry": "|gYes|n" if self.can_parry() else "|rNo|n",
        } | super().get_item_type_stats(looker)

class WeaponBareHands(WeaponObject):
    """
    Special class for bare hands when no weapon is wielded.
    """
    obj_type = ObjType.WEAPON
    inventory_use_slot = WieldLocation.WEAPON_HAND
    attack_type = Ability.STR
    defense_type = DefenseType.ARMOR
    damage_roll = "1d4"

    def _apply_color(self, custom_text=None):
        return "|xbare hands|n"

    def can_parry(self):
        return False

class ArmorObject(EquipmentObject):
    """
    Base class for all wearable Armors.

    """

    obj_type = ObjType.ARMOR
    inventory_use_slot = WieldLocation.BODY

    armor = AttributeProperty(1)

    def get_item_type_stats(self, looker=None):
        #TODO make armor bonus a physical description somehow
        """
        ArmorObjects have the following:
            Armor (amount of armor bonus)
        """
        return {
            "Armor": self.armor
        } | super().get_item_type_stats(looker)

class Shield(ArmorObject):
    """
    Base class for all Shields.

    """

    obj_type = ObjType.SHIELD
    inventory_use_slot = WieldLocation.SHIELD_HAND
    block = AttributeProperty(default=0)

    def get_item_type_stats(self, looker=None):
        #TODO block % a physical description somehow
        """
        ShieldObjects have the following:
            Block (block chance)
        """
        return {
            "Block": self.block
        } | super().get_item_type_stats(looker)


class Helmet(ArmorObject):
    """
    Base class for all Helmets.

    """

    obj_type = ObjType.HELMET
    inventory_use_slot = WieldLocation.HEAD
