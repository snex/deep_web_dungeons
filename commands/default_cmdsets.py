"""
Command sets

All commands in the game must be grouped in a cmdset.  A given command
can be part of any number of cmdsets and cmdsets can be added/removed
and merged onto entities at runtime.

To create new commands to populate the cmdset, see
`commands/command.py`.

This module wraps the default command sets of Evennia; overloads them
to add/remove commands from the default lineup. You can create your
own cmdsets by inheriting from them or directly from `evennia.CmdSet`.

"""

from evennia import default_cmds
from evennia.contrib.grid.xyzgrid.commands import XYZGridCmdSet

from .game import CmdCharSheet, CmdInventory, CmdWieldOrWear, CmdRemove, CmdGive, CmdTalk
from .look import CmdLook
from .ooc import CmdCharCreate
from .prefs import CmdPrefs
from .combat import CmdInitiateCombat, CmdHit, CmdShoot, CmdAdvance, CmdRetreat, CmdFlee

class CharacterCmdSet(default_cmds.CharacterCmdSet):
    """
    The `CharacterCmdSet` contains general in-game commands like `look`,
    `get`, etc available on in-game Character objects. It is merged with
    the `AccountCmdSet` when an Account puppets a Character.
    """

    key = "DefaultCharacter"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        self.add(CmdLook())  # We override the look func to display the map
        self.add(XYZGridCmdSet()) # xyzgrid pathfinding and building commands

        # non-combat commands
        self.add(CmdCharSheet())
        self.add(CmdInventory())
        self.add(CmdWieldOrWear())
        self.add(CmdRemove())
        self.add(CmdGive())
        self.add(CmdTalk())

        # combat commands
        # self.add(CombatCmdSet()) # combat-specific commands
        self.add(CmdInitiateCombat())
        self.add(CmdHit())
        self.add(CmdShoot())
        self.add(CmdAdvance())
        self.add(CmdRetreat())
        self.add(CmdFlee())

class AccountCmdSet(default_cmds.AccountCmdSet):
    """
    This is the cmdset available to the Account at all times. It is
    combined with the `CharacterCmdSet` when the Account puppets a
    Character. It holds game-account-specific commands, channel
    commands, etc.
    """

    key = "DeepWebAccount"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        self.add(CmdCharCreate()) # Override default creation
        self.add(CmdPrefs())
