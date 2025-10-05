"""
Object

The Object is the base class for things in the game world.

Note that the default Character, Room and Exit do not inherit from Object.
"""

from evennia import AttributeProperty
from evennia.objects.objects import DefaultObject
from evennia.utils.utils import make_iter

from world.enums import Ability, CombatRange, ObjType, WieldLocation, AttackType, DefenseType
from world.utils import get_obj_stats

class Object(DefaultObject):
    """
    Base in-game entity.

    """

    # inventory management
    inventory_use_slot = AttributeProperty(WieldLocation.BACKPACK)
    # how many inventory slots it uses (can be a fraction)
    size = AttributeProperty(1)
    value = AttributeProperty(0)

    # can also be an iterable, for adding multiple obj-type tags
    obj_type = ObjType.GEAR

    def at_object_creation(self):
        for obj_type in make_iter(self.obj_type):
            self.tags.add(obj_type.value, category="obj_type")

    def get_display_header(self, looker, **kwargs):
        return ""  # this is handled by get_obj_stats

    def get_display_desc(self, looker, **kwargs):
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


class WeaponObject(Object):
    """
    Base weapon class for all  weapons.

    """

    obj_type = ObjType.WEAPON
    inventory_use_slot: WieldLocation = AttributeProperty(WieldLocation.WEAPON_HAND)
    quality: int = AttributeProperty(3)

    # maximum attack range for this weapon
    attack_range: CombatRange = AttributeProperty(CombatRange.MELEE)
    attack_type: AttackType = AttributeProperty(AttackType.MELEE)
    # what defense stat of the enemy it must defeat
    defense_type: Ability = AttributeProperty(DefenseType.ARMOR)

    min_damage: int = AttributeProperty(1)
    max_damage: int = AttributeProperty(4)
    stamina_cost: int = AttributeProperty(2)
    cooldown: int = AttributeProperty(2)

class WeaponBareHands(WeaponObject):
    """
    Special class for bare hands when no weapon is wielded.
    """
    obj_type = ObjType.WEAPON
    inventory_use_slot = WieldLocation.WEAPON_HAND
    attack_type = Ability.STR
    defense_type = DefenseType.ARMOR
    damage_roll = "1d4"

class Runestone(WeaponObject, ConsumableObject):
    """
    Base class for magic runestones. In _Knave_, every spell is represented by a rune stone
    that takes up an inventory slot. It is wielded as a weapon in order to create the specific
    magical effect provided by the stone. Normally each stone can only be used once per day but
    they are quite powerful (and scales with caster level).

    """

    obj_type = (ObjType.WEAPON, ObjType.MAGIC)
    inventory_use_slot = WieldLocation.TWO_HANDS
    quality = AttributeProperty(3)

    attack_type = AttributeProperty(Ability.WIL)
    defense_type = AttributeProperty(Ability.CUN)
    damage_roll = AttributeProperty("1d8")

    def at_post_use(self, user, *args, **kwargs):
        """ Called after the spell was cast. """
        self.uses -= 1

    def refresh(self):
        """ Reset the runestone after it was used. """
        self.uses = 1


class ArmorObject(Object):
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
