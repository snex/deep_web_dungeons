"""
Test rooms.
"""

from evennia.utils import create
from evennia.utils.test_resources import EvenniaTest

from typeclasses.rooms import Room, TownRoom

class TestRooms(EvenniaTest):
    """ Test Rooms. """

    def test_format_appearance(self):
        """ Test that room descs allow empty lines. """
        desc = "Desc with an empty line\n\nLine 2"
        room = create.create_object(
            Room,
            key="test room",
        )
        self.assertEqual(
            room.format_appearance(desc, None),
            "Desc with an empty line\n\nLine 2"
        )

class TestTownRooms(EvenniaTest):
    """ Test TownRooms. """
    def test_get_display_desc(self):
        """ Test that show_desc param is used to show the room desc or not. """
        room = create.create_object(
            TownRoom,
            key="test room"
        )
        self.assertEqual(
            room.get_display_desc(None),
            "This is a room."
        )
        self.assertEqual(
            room.get_display_desc(None, show_desc=True),
            "This is a room."
        )
        self.assertEqual(
            room.get_display_desc(None, show_desc=False),
            ""
        )
