"""
Test custom commands.

"""

from unittest.mock import call, patch
from anything import Something

from evennia.utils.ansi import strip_ansi
from evennia.utils.create import create_object
from evennia.utils.test_resources import EvenniaCommandTest

from typeclasses.npcs import ShopKeeper
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
|wChar the female Human Antifa Rioter|n

STR +1
CUN -1
WIL +1

This is Char.

Current stats:
    Health: |gPerfect|n
    Mana: |gPerfect|n
    Stamina: |gPerfect|n
""")
        self.char1.gender = "female"
        self.char1.race_key = "human"
        self.char1.cclass_key = "antifa_rioter"
        self.char1.cunning = -1
        self.char1.db.desc = "This is Char."
        self.call(
            game.CmdCharSheet(),
            "charsheet",
            expected_output
        )

    def test_inventory(self):
        """ Test that the inventory command shows your inventory. """
        self.call(
            game.CmdInventory(),
            "inventory",
            """
You are fighting with your bare fists and have no shield.
You wear no armor and no helmet.
Backpack is empty.
You use 0/11 equipment slots.
""".strip(),
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

    def test_give__coins(self):
        """
        Test that the give coins command gives coins to the other character.
        It should also not let you give more coins than you have.
        """
        self.char2.key = "Friend"
        self.char2.coins = 0
        self.char1.coins = 100

        self.call(game.CmdGive(), "40 coins to friend", "You give Friend 40 coins.")
        self.assertEqual(self.char1.coins, 60)
        self.assertEqual(self.char2.coins, 40)

        self.call(game.CmdGive(), "10 to friend", "You give Friend 10 coins.")
        self.assertEqual(self.char1.coins, 50)
        self.assertEqual(self.char2.coins, 50)

        self.call(game.CmdGive(), "60 to friend", "You only have 50 coins to give.")

    @patch("commands.game.EvMenu")
    def test_give__item(self, mock_ev_menu):
        """ Test that the give item command creates a menu. """
        self.char2.key = "Friend"
        self.char1.equipment.add(self.helmet)

        self.call(game.CmdGive(), "helmet to friend", "")

        mock_ev_menu.assert_has_calls(
            (
                call(
                    self.char2,
                    {"node_receive": Something, "node_end": Something},
                    startnode="node_receive",
                    startnode_input=("", {"item": self.helmet, "giver": self.char1}),
                ),
                call(
                    self.char1,
                    {"node_give": Something, "node_end": Something},
                    startnode="node_give",
                    startnode_input=("", {"item": self.helmet, "receiver": self.char2}),
                ),
            )
        )

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
