"""
Commands and cmdsets for game-specific mechanics and functionality.

TODO: The base EvAdventure tutorial manages most functionality in menus,
so there are few commands here. More functionality or modifications may
be needed.

"""

from evennia.utils.utils import inherits_from

from typeclasses.npcs import TalkativeNPC, InsultNPC
from typeclasses.objects import QuantumLatticeObject

from world.enums import WieldLocation

from .command import Command

_CHAR_SHEET = """
|w{name} the {gender} {race} {cclass}|n

STR {str_plus_minus}{strength}
CUN {cun_plus_minus}{cunning}
WIL {wil_plus_minus}{will}

{description}

Current stats:
    Health: {hurt_level}
    Mana: {mana_level}
    Stamina: {stamina_level}
"""

class CmdCharSheet(Command):
    """View your character sheet

    Usage: charsheet

    """

    key = "charsheet"
    aliases = ("c", "cs", "char")

    def func(self):
        self.caller.msg(
            _CHAR_SHEET.format(
                name=self.caller.name,
                gender=self.caller.gender,
                str_plus_minus=("+" if self.caller.strength >= 0 else ""),
                strength=self.caller.strength,
                cun_plus_minus=("+" if self.caller.cunning >= 0 else ""),
                cunning=self.caller.cunning,
                wil_plus_minus=("+" if self.caller.will >= 0 else ""),
                will=self.caller.will,
                race=self.caller.race,
                cclass=self.caller.cclass,
                hurt_level=self.caller.hurt_level,
                mana_level=self.caller.mana_level,
                stamina_level=self.caller.stamina_level,
                description=self.caller.db.desc
            )
        )

class CmdCombine(Command):
    """
    Combine 3 quantum lattices into a lattice of the next tier

    Usage:
      combine <quantum_lattice>

    """

    key = "combine"

    def func(self):
        if not self.args:
            self.caller.msg("You must specify something to combine.")
            return

        ql = self.caller.search(
            self.args,
            quiet=True,
            candidates=self.caller.equipment.all(only_objs=True),
            typeclass=QuantumLatticeObject,
        )[:1]

        if not ql:
            self.caller.msg(f"Could not find '{self.args}' among your quantum lattices.")
            return

        self.caller.msg(ql[0].combine(self.caller))


class CmdInventory(Command):
    """
    View your inventory

    Usage:
      inventory

    """

    key = "inventory"
    aliases = ("i", "inv")

    def func(self):
        loadout = self.caller.equipment.display_loadout()
        backpack = self.caller.equipment.display_backpack()
        slot_usage = self.caller.equipment.display_slot_usage()

        self.caller.msg(f"{loadout}\n{backpack}\nYou use {slot_usage} equipment slots.")


class CmdWieldOrWear(Command):
    """
    Wield a weapon/shield, or wear a piece of armor or a helmet.

    Usage:
      wield <item>
      wear <item>

    The item will automatically end up in the suitable spot, replacing whatever
    was there previously.

    """

    key = "wield"
    aliases = ("wear",)
    auto_help = False

    out_txts = {
        WieldLocation.BACKPACK: "You shuffle the position of {key} around in your backpack.",
        WieldLocation.TWO_HANDS: "You hold {key} with both hands.",
        WieldLocation.WEAPON_HAND: "You hold {key} in your strongest hand, ready for action.",
        WieldLocation.SHIELD_HAND: "You hold {key} in your off hand, ready to protect you.",
        WieldLocation.BODY: "You strap {key} on yourself.",
        WieldLocation.HEAD: "You put {key} on your head.",
    }

    def func(self):
        # find the item among those in equipment
        item = self.caller.search(self.args, candidates=self.caller.equipment.all(only_objs=True))
        if not item:
            # An 'item not found' error will already have been reported; we add another line
            # here for clarity.
            self.caller.msg("You must carry the item you want to wield or wear.")
            return

        use_slot = getattr(item, "inventory_use_slot", WieldLocation.BACKPACK)

        # check what is currently in this slot
        current = self.caller.equipment.slots[use_slot]

        if current == item:
            self.caller.msg(f"You are already using {item.key}.")
            return

        # move it to the right slot based on the type of object
        self.caller.equipment.move(item)

        # inform the user of the change (and potential swap)
        if current:
            self.caller.msg(f"Returning {current.key} to the backpack.")
        self.caller.msg(self.out_txts[use_slot].format(key=item.key))


class CmdRemove(Command):
    """
    Remove a remove a weapon/shield, armor or helmet.

    Usage:
      remove <item>
      unwield <item>
      unwear <item>

    To remove an item from the backpack, use |wdrop|n instead.

    """

    key = "remove"
    aliases = ("unwield", "unwear")

    def func(self):
        caller = self.caller

        # find the item among those in equipment
        item = caller.search(self.args, candidates=caller.equipment.all(only_objs=True))
        if not item:
            # An 'item not found' error will already have been reported
            return

        current_slot = caller.equipment.get_current_slot(item)

        if current_slot is WieldLocation.BACKPACK:
            # we don't allow dropping this way since it may be unexepected by users who forgot just
            # where their item currently is.
            caller.msg(
                f"You already stashed away {item.key} in your backpack. Use 'drop' if "
                "you want to get rid of it."
            )
            return

        caller.equipment.remove(item)
        caller.equipment.add(item)
        caller.msg(f"You stash {item.key} in your backpack.")

class CmdTalk(Command):
    """
    Start a conversations with shop keepers and other NPCs in the world.

    Args:
      talk <npc>

    """

    key = "talk"

    def func(self):
        target = self.caller.search(self.args)
        if not target:
            return

        if not inherits_from(target, TalkativeNPC) and not inherits_from(target, InsultNPC):
            self.caller.msg(
                f"{target.get_display_name(looker=self.caller)} does not seem very talkative."
            )
            return
        target.at_talk(self.caller)
