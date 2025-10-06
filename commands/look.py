"""
Override the default `look` command to display the mini-map.
"""

from evennia.commands.default.general import CmdLook as _CmdLook

# disable too-few-public-methods as this is just here to override the default
# pylint: disable=too-few-public-methods
class CmdLook(_CmdLook):
    """
    look at location or object

    Usage:
      look
      look <obj>
      look *<account>

    Observes your location or objects in your vicinity.
    """

    key = "look"
    aliases = ["l", "ls"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """
        Handle the looking.
        """
        caller = self.caller
        if not self.args:
            target = caller.location
            if not target:
                caller.msg("You have no location to look at!")
                return
        else:
            target = caller.search(self.args)
            if not target:
                return

        desc = caller.at_look(target)

        map_display = None
        if map_getter := getattr(target, 'get_map_display', None):
            map_display = map_getter(looker=caller)

        self.msg(text=(desc, {"type": "look"}), options=None, map=map_display)
