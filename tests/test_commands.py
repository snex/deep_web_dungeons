"""
Test custom commands.

"""

from unittest.mock import patch

from evennia.prototypes.spawner import spawn
from evennia.utils.ansi import strip_ansi
from evennia.utils.create import create_object
from evennia.utils.test_resources import EvenniaCommandTest

from typeclasses.npcs import ShopKeeper
from world.common import item_prototypes
from commands import game, prefs
from .mixins import AinneveTestMixin


class TestCommands(AinneveTestMixin, EvenniaCommandTest):
    """ Test commands. """

    def test_prefs__acount(self):
        """ Test the prefs command when caller is an account. """

        expected_output = """
______________________________________________________________________________

Select a preference by number to change it, or type `quit` to go back.
______________________________________________________________________________

 1: look_on_enter: True                                           
 Whether or not to show the flavor text of a room upon entering.
"""

        self.call(
            prefs.CmdPrefs(),
            "",
            expected_output,
            caller=self.account
        )

    def test_prefs__character(self):
        """ Test the prefs command when caller is a character. """

        expected_output = """
______________________________________________________________________________

Select a preference by number to change it, or type `quit` to go back.
______________________________________________________________________________

 1: look_on_enter: True                                           
 Whether or not to show the flavor text of a room upon entering.
"""
        self.call(
            prefs.CmdPrefs(),
            "",
            expected_output,
            caller=self.char1,
            receiver=self.account
        )


    def test_prefs__other(self):
        """ Test the prefs command when caller is something that has no account. """

        with self.assertRaises(RuntimeError):
            self.call(
                prefs.CmdPrefs(),
                "",
                "",
                caller=self.char1.weapon
            )

    def test_charsheet(self):
        """ Test that the charsheet command shows your character sheet. """
        expected_output = strip_ansi("""
+------------------------------------------------------------------------------+
|                                                                              |
|                                     Char                                     |
|                                                                              |
|  Gender:          female               STR:                              +1  |
|  Race:            Human                CUN:                              -1  |
|  Class:           Antifa Rioter        WIL:                              +1  |
|                                                                              |
|                                                                              |
|                                                                              |
|  One ugly motherfucker.                                                      |
|  This is Char.                                                               |
|                                                                              |
+------------------------------------------------------------------------------+
|                                                                              |
|  Health:            Perfect            No Status Effects                     |
|  System Load:       Perfect                                                  |
|  Stamina:           Perfect                                                  |
|                                                                              |
+------------------------------------------------------------------------------+
""")
        self.char1.gender = "female"
        self.char1.race_key = "human"
        self.char1.cclass_key = "antifa_rioter"
        self.char1.cunning = -1
        self.char1.db.desc = "This is Char."
        self.call(
            game.CmdCharSheet(),
            "",
            expected_output,
            stripmenu=False,
        )

    @patch("typeclasses.objects.QuantumLatticeObject.combine")
    def test_combine(self, mock_combine):
        """ Test the command for combining quantum lattices. """

        self.call(
            game.CmdCombine(),
            "",
            "You must specify something to combine."
        )

        self.call(
            game.CmdCombine(),
            "junk",
            "Could not find 'junk' among your quantum lattices."
        )

        ql = spawn(item_prototypes.QL_DUST_SHARD | {"location": self.char1})[0]
        self.char1.equipment.move(ql)
        self.call(game.CmdCombine(), "dust shard")
        mock_combine.assert_called_with(self.char1)

    def test_inventory(self):
        """ Test that the inventory command shows your inventory. """

        plate = spawn(item_prototypes.ARMOR_CHEST_PLATE | {"location": self.char1})[0]
        self.char1.equipment.move(plate)
        ql = spawn(item_prototypes.QL_DUST_SHARD | {"location": self.char1})[0]
        self.char1.equipment.move(ql)
        expected_output = strip_ansi("""
+------------------------------------------------------------------------------+
|                                                                              |
|  R.Hand: bare hands              1.00  L.Hand: None                          |
|  Body:   plasteel chest plate    1.00  Helmet: None                          |
|  Arms:   None                          Legs:   None                          |
|                                                                              |
+------------------------------------------------------------------------------+
|                                                                              |
|   Qty Item                         Wt   Qty Item                         Wt  |
|     1 dust shard                 0.01                                        |
|                                                                              |
|                                                                              |
|                                                                              |
|                                                                              |
|                                                                              |
|                                                                              |
|                                                                              |
|                                                                              |
|                                                                              |
|                                                                              |
|                                                                              |
|                                                                              |
|  Capacity 1.01/11                                                  Page 1/1  |
+------------------------------------------------------------------------------+
""")
        self.call(
            game.CmdInventory(),
            "",
            expected_output,
            stripmenu=False,
        )

    def test_wield_or_wear(self):
        """ Test that wearing or wielding gear equips it. """
        self.char1.equipment.add(self.helmet)
        self.char1.equipment.add(self.weapon)
        self.shield.location = self.room1

        self.call(game.CmdWieldOrWear(), "shield", "Could not find 'shield'")
        self.call(game.CmdWieldOrWear(), "helmet", "You put helmet on your head.")
        self.call(
            game.CmdWieldOrWear(),
            "weapon",
            "You hold weapon in your strongest hand, ready for action.",
        )
        self.call(game.CmdWieldOrWear(), "helmet", "You are already using helmet.")

    def test_remove(self):
        """ Test that removing gear removes it. """
        self.char1.equipment.add(self.helmet)
        self.call(game.CmdWieldOrWear(), "helmet", "You put helmet on your head.")

        self.call(game.CmdRemove(), "helmet", "You stash helmet in your backpack.")

    @patch("typeclasses.npcs.EvMenu")
    def test_talk(self, mock_ev_menu):
        """ Test that talking to a ShopKeeper creates a menu. """
        npc = create_object(ShopKeeper, key="shopkeep", location=self.room1)

        npc.menudata = {"foo": None, "bar": None}

        self.call(game.CmdTalk(), "shopkeep")

        mock_ev_menu.assert_called_with(
            self.char1,
            {"foo": None, "bar": None},
            startnode="node_start",
            session=None,
            npc=npc,
        )
