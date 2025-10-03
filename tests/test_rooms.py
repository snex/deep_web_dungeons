"""
Test rooms.
"""

from evennia.utils import create
from evennia.utils.test_resources import EvenniaTest

from typeclasses.rooms import Room, TownRoom

class TestRooms(EvenniaTest):
    def test_format_appearance(self):
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
    def test_get_display_desc(self):
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
