"""

Lockfuncs

Lock functions are functions available when defining lock strings,
which in turn limits access to various game systems.

All functions defined globally in this module are assumed to be
available for use in lockstrings to determine access. See the
Evennia documentation for more info on locks.

A lock function is always called with two arguments, accessing_obj and
accessed_obj, followed by any number of arguments. All possible
arguments should be handled with *args, **kwargs. The lock function
should handle all eventual tracebacks by logging the error and
returning False.

Lock functions in this module extend (and will overload same-named)
lock functions from evennia.locks.lockfuncs.

"""

from evennia.utils.utils import inherits_from

from typeclasses.characters import BaseCharacter, Character
from typeclasses.objects import Object

from world.enums import WieldLocation

def in_combat(accessing_obj, _accessed_obj, *args, **kwargs):
    """returns true if an active combat handler is present"""
    if hasattr(accessing_obj, 'nattributes'):
        return accessing_obj.nattributes.get('combat')

    return False

def in_range(accessing_obj, _accessed_obj, *args, **kwargs):
    """returns true if accessing_obj has any targets in specified range"""
    combat_range = args[0] if args else "MELEE"
    if hasattr(accessing_obj, 'nattributes'):
        if not (combat := accessing_obj.ndb.combat):
            return False

        return combat.any_in_range(accessing_obj, combat_range)

    return False

def melee_equipped(accessing_obj, _accessed_obj, *args, **kwargs):
    """returns true if accessing_obj has a melee weapon equipped"""
    if hasattr(accessing_obj, 'weapon'):
        if hasattr(accessing_obj.weapon, 'attack_range'):
            return accessing_obj.weapon.attack_range.name == "MELEE"

        return False

    return False

def ranged_equipped(accessing_obj, _accessed_obj, *args, **kwargs):
    """returns true if accessing_obj has a ranged weapon equipped"""
    if hasattr(accessing_obj, 'weapon'):
        if hasattr(accessing_obj.weapon, 'attack_range'):
            return accessing_obj.weapon.attack_range.name == "LONG_RANGE"

        return False

    return False

def not_in_foreign_backpack(accessing_obj, accessed_obj, *args, **kwargs):
    """ returns false if another character has the accessed_obj in their backpack """

    if accessed_obj.location == accessing_obj:
        return True

    if not inherits_from(accessed_obj.location, Character):
        return True

    return accessed_obj.location.equipment.get_current_slot(accessed_obj) != WieldLocation.BACKPACK

def character_can_equip_item(character: BaseCharacter, item: Object, *args, **kwargs):
    """
    returns True if character can equip item, False if not
    items are currently restricted by class and level
    this lockfunc does not care about the item's location because EquipmentHandler handles that
    """

    if not hasattr(item, "required_level"):
        return False

    if not hasattr(item, "allowed_classes"):
        return False

    if not inherits_from(character, BaseCharacter):
        return False

    return (
        character.cclass in item.allowed_classes and
        character.levels.level >= item.required_level
    )
