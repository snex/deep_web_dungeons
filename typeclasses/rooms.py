"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia.contrib.grid.xyzgrid.xyzroom import XYZRoom
from evennia.objects.objects import DefaultRoom

CHAR_SYMBOL = "|w@|n"
CHAR_ALT_SYMBOL = "|w>|n"
ROOM_SYMBOL = "|bo|n"
LINK_COLOR = "|B"

_MAP_GRID = [
    [" ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " "],
    [" ", " ", "@", " ", " "],
    [" ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " "],
]
_EXIT_GRID_SHIFT = {
    "north": (0, 1, "||"),
    "east": (1, 0, "-"),
    "south": (0, -1, "||"),
    "west": (-1, 0, "-"),
    "northeast": (1, 1, "/"),
    "southeast": (1, -1, "\\"),
    "southwest": (-1, -1, "/"),
    "northwest": (-1, 1, "\\"),
}


class Room(DefaultRoom):
    """
    Simple room supporting game-specific mechanics.

    """

    allow_combat = False
    allow_pvp = False
    allow_death = False

    def format_appearance(self, appearance, looker, **kwargs):
        """
        By default, blank lines are removed. Override this behavior.
        """

        return appearance.strip()


class TownRoom(Room, XYZRoom):
    """
    Combines the XYZGrid functionality with Ainneve-specific room code.
    """
    map_area_client = False
    map_fill_all = False

    def get_display_desc(self, looker, **kwargs):
        """
        Override this so that we don't display room description if user preference turns it off.
        """

        if kwargs.get("show_desc", True) is False:
            return ""

        return super().get_display_desc(looker, **kwargs)




class PvPRoom(Room):
    """
    Room where PvP can happen, but noone gets killed.

    """

    allow_combat = True
    allow_pvp = True

    def get_display_footer(self, looker, **kwargs):
        """
        Display the room's PvP status.

        """
        return "|yNon-lethal PvP combat is allowed here!|n"
