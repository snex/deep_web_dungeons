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
from evennia.contrib.game_systems.barter.barter import CmdTrade
from evennia.contrib.grid.xyzgrid.commands import XYZGridCmdSet

from .admin import CmdSpawnRand
from .game import (
    CmdCharSheet,
    CmdCombine,
    CmdInventory,
    CmdWieldOrWear,
    CmdRemove,
    CmdTalk,
    CmdUse
)
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
        self.add(CmdCombine())
        self.add(CmdInventory())
        self.add(CmdWieldOrWear())
        self.add(CmdRemove())
        self.add(CmdTalk())
        self.add(CmdTrade())
        self.add(CmdUse())

        # combat commands
        self.add(CmdInitiateCombat())
        self.add(CmdHit())
        self.add(CmdShoot())
        self.add(CmdAdvance())
        self.add(CmdRetreat())
        self.add(CmdFlee())

        # admin commands
        self.add(CmdSpawnRand())

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

class UnloggedinCmdSet(default_cmds.UnloggedinCmdSet):
    """
    Command set available to the Session before being logged in.  This
    holds commands like creating a new account, logging in, etc.
    """

    key = "DefaultUnloggedin"

    # disable useless-parent-delegation pylint here because this goofy setup is required
    #     for the app to run for some reason
    def at_cmdset_creation(self): # pylint: disable=useless-parent-delegation
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()

class SessionCmdSet(default_cmds.SessionCmdSet):
    """
    This cmdset is made available on Session level once logged in. It
    is empty by default.
    """

    key = "DefaultSession"

    # disable useless-parent-delegation pylint here because this goofy setup is required
    #     for the app to run for some reason
    def at_cmdset_creation(self): # pylint: disable=useless-parent-delegation
        """
        This is the only method defined in a cmdset, called during
        its creation. It should populate the set with command instances.
        As and example we just add the empty base `Command` object.
        It prints some info.
        """
        super().at_cmdset_creation()
