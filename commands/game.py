"""
Commands and cmdsets for game-specific mechanics and functionality.

TODO: The base EvAdventure tutorial manages most functionality in menus,
so there are few commands here. More functionality or modifications may
be needed.

"""

from evennia import InterruptCommand
from evennia.utils.evmenu import EvMenu
from evennia.utils.utils import inherits_from

from typeclasses.npcs import TalkativeNPC, InsultNPC

from world.enums import WieldLocation
from world.equipment import EquipmentError
from world.utils import get_obj_stats

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


# give / accept menu


def _rescind_gift(_caller, raw_string, **kwargs):
    """
    Called when giver rescinds their gift in `node_give` below.
    It means they entered 'cancel' on the gift screen.

    """
    # kill the gift menu for the receiver immediately
    receiver = kwargs["receiver"]
    receiver.ndb._evmenu.close_menu()
    receiver.msg("The offer was rescinded.")
    return "node_end"


def node_give(caller, raw_string, **kwargs):
    """
    This will show to the giver until receiver accepts/declines. It allows them
    to rescind their offer.

    The `caller` here is the one giving the item. We also make sure to feed
    the 'item' and 'receiver' into the Evmenu.

    """
    item = kwargs["item"]
    receiver = kwargs["receiver"]
    text = f"""
You are offering {item.key} to {receiver.get_display_name(looker=caller)}.
|wWaiting for them to accept or reject the offer ...|n
""".strip()

    options = {
        "key": ("cancel", "abort"),
        "desc": "Rescind your offer.",
        "goto": (_rescind_gift, kwargs),
    }
    return text, options


def _accept_or_reject_gift(caller, raw_string, **kwargs):
    """
    Called when receiver enters yes/no in `node_receive` below. We first need to
    figure out which.

    """
    item = kwargs["item"]
    giver = kwargs["giver"]
    if raw_string.lower() in ("yes", "y"):
        # they accepted - move the item!
        item = giver.equipment.remove(item)
        if item:
            try:
                # this will also add them to the equipment backpack, if possible
                item.move_to(caller, quiet=True, move_type="give")
            except EquipmentError:
                caller.location.msg_contents(
                    f"$You({giver.key.key}) $conj(try) to give "
                    f"{item.key} to $You({caller.key}), but they can't accept it since their "
                    "inventory is full.",
                    mapping={giver.key: giver, caller.key: caller},
                )
            else:
                caller.location.msg_contents(
                    f"$You({giver.key}) $conj(give) {item.key} to $You({caller.key}), "
                    "and they accepted the offer.",
                    mapping={giver.key: giver, caller.key: caller},
                )
        giver.ndb._evmenu.close_menu()

    return "node_end"


def node_receive(caller, raw_string, **kwargs):
    """
    Will show to the receiver and allow them to accept/decline the offer for
    as long as the giver didn't rescind it.

    The `caller` here is the one receiving the item. We also make sure to feed
    the 'item' and 'giver' into the EvMenu.

    """
    item = kwargs["item"]
    giver = kwargs["giver"]
    text = f"""
{giver.get_display_name()} is offering you {item.key}:

{get_obj_stats(item)}

[Your inventory usage: {caller.equipment.display_slot_usage()}]
|wDo you want to accept the given item? Y/[N]
    """
    options = ({"key": "_default", "goto": (_accept_or_reject_gift, kwargs)},)
    return text, options


def node_end(_caller, raw_string, **kwargs):
    """ End the give/receive menu. """
    return "", None


class CmdGive(Command):
    """
    Give item or money to another person. Items need to be accepted before
    they change hands. Money changes hands immediately with no wait.

    Usage:
      give <item> to <receiver>
      give <number of coins> [coins] to receiver

    If item name includes ' to ', surround it in quotes.

    Examples:
      give apple to ranger
      give "road to happiness" to sad ranger
      give 10 coins to ranger
      give 12 to ranger

    """

    def __init__(self):
        super().__init__()
        self.item_name = None
        self.receiver_name = None
        self.receiver = None
        self.coins = None

    key = "give"

    def parse(self):
        """
        Parsing is a little more complex for this command.

        """
        super().parse()
        args = self.args
        if " to " not in args:
            self.caller.msg(
                "Usage: give <item> to <recevier>. Specify e.g. '10 coins' to pay money. "
                "Use quotes around the item name it if includes the substring ' to '. "
            )
            # disable pylint here as evennnia defines this Exception strangely
            raise InterruptCommand # pylint: disable=raising-bad-type

        self.item_name = ""
        self.coins = 0

        # make sure we can use '...' to include items with ' to ' in the name
        if args.startswith('"') and args.count('"') > 1:
            end_ind = args[1:].index('"') + 1
            item_name = args[:end_ind]
            _, receiver_name = args.split(" to ", 1)
        elif args.startswith("'") and args.count("'") > 1:
            end_ind = args[1:].index("'") + 1
            item_name = args[:end_ind]
            _, receiver_name = args.split(" to ", 1)
        else:
            item_name, receiver_name = args.split(" to ", 1)

        # a coin count rather than a normal name
        if " coins" in item_name:
            item_name = item_name[:-6]
        if item_name.isnumeric():
            self.coins = max(0, int(item_name))

        self.item_name = item_name
        self.receiver_name = receiver_name

    def _give_coins(self):
        current_coins = self.caller.coins
        if self.coins > current_coins:
            self.caller.msg(f"You only have |y{current_coins}|n coins to give.")
            return
        # do transaction
        self.caller.coins -= self.coins
        self.receiver.coins += self.coins
        self.caller.location.msg_contents(
            f"$You() $conj(give) $You({self.receiver.key}) {self.coins} coins.",
            from_obj=self.caller,
            mapping={self.receiver.key: self.receiver},
        )
        return

    def _give_item(self):
        item = self.caller.search(
            self.item_name,
            candidates=self.caller.equipment.all(only_objs=True)
        )
        if not item:
            return

        # testing hook
        if not item.at_pre_give(self.caller, self.receiver):
            return

        # before we start menus, we must check so either part is not already in a menu,
        # that would be annoying otherwise
        if self.receiver.ndb._evmenu:
            self.caller.msg(
                f"{self.receiver.get_display_name(looker=self.caller)}"
                " seems busy talking to someone else."
            )
            return
        if self.caller.ndb._evmenu:
            self.caller.msg("Close the current menu first.")
            return

        # this starts evmenus for both parties
        EvMenu(
            self.receiver,
            {"node_receive": node_receive, "node_end": node_end},
            startnode="node_receive",
            startnode_input=("", {"item": item, "giver": self.caller})
        )
        EvMenu(
            self.caller,
            {"node_give": node_give, "node_end": node_end},
            startnode="node_give",
            startnode_input=("", {"item": item, "receiver": self.receiver})
        )

    def func(self):
        self.receiver = self.caller.search(self.receiver_name)
        if not self.receiver:
            return

        # giving of coins is always accepted
        if self.coins:
            self._give_coins()
            return

        # giving of items require acceptance before it happens
        self._give_item()

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
