"""
Commands and cmdsets for game-specific mechanics and functionality.

TODO: The base EvAdventure tutorial manages most functionality in menus,
so there are few commands here. More functionality or modifications may
be needed.

"""

from evennia.commands.cmdhandler import InterruptCommand
from evennia.utils import evform, evtable
from evennia.utils.utils import inherits_from

from typeclasses.npcs import TalkativeNPC, InsultNPC
from typeclasses.objects import QuantumLatticeObject

from world.enums import WieldLocation

from .command import Command

class CmdCharSheet(Command):
    """View your character sheet

    Usage: charsheet

    """

    key = "charsheet"
    aliases = ("c", "cs", "char")

    def func(self):
        charsheet = evform.EvForm("world.charsheet")
        base_info = evtable.EvTable(border=None)
        base_info.add_row("|cGender|n: ", self.caller.gender)
        base_info.add_row("|cRace|n: ", self.caller.race.name)
        base_info.add_row("|cClass|n: ", self.caller.cclass.name)
        abilities = evtable.EvTable(border=None)
        abilities.add_row(
            "|cSTR|n: ",
            f"{'+' if self.caller.strength >=0 else ''}{self.caller.strength}"
        )
        abilities.add_row(
            "|cCUN|n: ",
            f"{'+' if self.caller.cunning >=0 else ''}{self.caller.cunning}"
        )
        abilities.add_row(
            "|cWIL|n: ",
            f"{'+' if self.caller.will >= 0 else ''}{self.caller.will}"
        )
        abilities.reformat_column(1, align="r")
        description = evtable.EvTable(border=None, valign="b")
        description.add_row(f"{self.caller.physical_appearance}\n{self.caller.db.desc}")
        cur_status = evtable.EvTable(border=None)
        cur_status.add_row("|cHealth|n: ", self.caller.hurt_level)
        cur_status.add_row("|cSystem Load|n: ", self.caller.mana_level)
        cur_status.add_row("|cStamina|n: ", self.caller.stamina_level)
        status_effects = evtable.EvTable(border=None)
        status_effects.add_row("No Status Effects")
        charsheet.map(
            tables={
                "2": base_info,
                "3": abilities,
                "4": description,
                "5": cur_status,
                "6": status_effects,
            },
            cells={
                "1": evtable.EvCell(f"|c{self.caller.name}|n", align="c")
            },
        )
        self.caller.msg(charsheet)

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
      inventory [page]

    """

    key = "inventory"
    aliases = ("i", "inv")

    def parse(self):
        self.args = self.args.strip().split(' ', 1)[0]

    def func(self):
        eq = self.caller.equipment
        inventory = evform.EvForm("world.inventory")
        equipped_l = evtable.EvTable(border=None)
        equipped_l.add_row(
            "R.Hand: ",
            eq.weapon if eq.weapon else "None",
            f"|b{float(eq.weapon.size):0.2f}|n" if eq.weapon else "",
        )
        equipped_l.add_row(
            "Body: ",
            eq.armor_item if eq.armor_item else "None",
            f"|b{float(eq.armor_item.size):0.2f}|n" if eq.armor_item else "",
        )
        equipped_l.add_row(
            "Arms: ",
            "None",
            "",
        )
        equipped_l.reformat_column(0, width=8)
        equipped_l.reformat_column(2, align="r", width=6)
        equipped_r = evtable.EvTable(border=None)
        l_hand = "None"
        if eq.weapon.inventory_use_slot == WieldLocation.TWO_HANDS:
            l_hand = eq.weapon
        if eq.shield:
            l_hand = eq.shield

        equipped_r.add_row(
            "L.Hand: ",
            l_hand,
            f"|b{float(eq.shield.size):0.2f}|n" if eq.shield else "",
        )
        equipped_r.add_row(
            "Helmet: ",
            eq.helmet if eq.helmet else "None",
            f"|b{float(eq.helmet.size):0.2f}|n" if eq.helmet else "",
        )
        equipped_r.add_row(
            "Legs: ",
            "None",
            "",
        )
        equipped_r.reformat_column(0, width=8)
        equipped_r.reformat_column(2, align="r", width=6)

        page, total_pages, backpack = self.caller.equipment.paged_backpack(self.args)
        backpack_l = evtable.EvTable(border=None)
        backpack_l.add_header("|uQty|U", "|uItem|U", "|uWt|U")
        for item in backpack[:12]:
            backpack_l.add_row(
                item[1]["quantity"],
                item[0],
                f"|b{round(float(item[1]['capacity']), 2):0.2f}|n",
            )
        backpack_l.reformat_column(0, align="r", width=4)
        backpack_l.reformat_column(1, pad_left=1)
        backpack_l.reformat_column(2, align="r", width=6)
        backpack_r = evtable.EvTable(border=None)
        backpack_r.add_header("|uQty|U", "|uItem|U", "|uWt|U")
        for item in backpack[12:]:
            backpack_r.add_row(
                item[1]["quantity"],
                item[0],
                f"|b{round(float(item[1]['capacity']), 2):0.2f}|n",
            )
        backpack_r.reformat_column(0, align="r", width=4)
        backpack_r.reformat_column(1, pad_left=1)
        backpack_r.reformat_column(2, align="r", width=6)
        inventory.map(
            tables={
                "1": equipped_l,
                "2": equipped_r,
                "3": backpack_l,
                "4": backpack_r,
            },
            cells={
                "5": eq.display_slot_usage(),
                "6": evtable.EvCell(f"Page {page}/{total_pages}", align="r"),
            },
        )
        self.caller.msg(inventory)

class CmdUse(Command):
    """
    Use a usable item.

    Usage:
      use <item>
      use <item> [on otheritem]
    """

    key = "use"

    def __init__(self):
        super().__init__()
        self.subject_obj = None
        self.object_obj = None

    def parse(self):
        """ assign the object to be used and the object to be used upon, if available """
        args = self.args.strip().rsplit(" on ", 1)

        subject_obj = self.caller.search(
            args[0],
            quiet=True,
            candidates=self.caller.equipment.all(only_objs=True),
        )

        if len(args) > 1:
            object_obj = self.caller.search(
                args[1],
                quiet=True,
                candidates=self.caller.equipment.all(only_objs=True),
            )

            if not object_obj:
                subject_obj_retry = self.caller.search(
                    self.args.strip(),
                    quiet=True,
                    candidates=self.caller.equipment.all(only_objs=True),
                )

                if not subject_obj_retry and not subject_obj:
                    self.caller.msg(f"Could not find '{args[0]}' or '{self.args.strip()}'.")
                    raise InterruptCommand

                self.caller.msg(f"Could not find '{args[1]}'.")
                raise InterruptCommand

            self.object_obj = self.caller.search(
                args[1],
                candidates=self.caller.equipment.all(only_objs=True),
            )

        self.subject_obj = self.caller.search(
            args[0],
            candidates=self.caller.equipment.all(only_objs=True),
        )

    def func(self):
        if not self.subject_obj:
            return

        if self.subject_obj.at_pre_use(self.object_obj, caller=self.caller):
            self.subject_obj.use(self.object_obj, caller=self.caller)

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

        if not item.access(self.caller, "wear_wield"):
            self.caller.msg("You cannot equip that item.")
            return

        use_slot = getattr(item, "inventory_use_slot", WieldLocation.BACKPACK)

        # check what is currently in this slot
        current = self.caller.equipment.slots[use_slot]

        if current == item:
            self.caller.msg(f"You are already using {item}.")
            return

        # move it to the right slot based on the type of object
        self.caller.equipment.move(item)

        # inform the user of the change (and potential swap)
        if current:
            self.caller.msg(f"Returning {current} to the backpack.")
        self.caller.msg(self.out_txts[use_slot].format(key=item))


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
        caller.msg(f"You stash {item} in your backpack.")

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

        if not inherits_from(target, TalkativeNPC) and not inherits_from(target, ShoutNPC):
            self.caller.msg(
                f"{target} does not seem very talkative."
            )
            return
        target.at_talk(self.caller)
