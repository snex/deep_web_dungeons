from commands.debug.encounters import CmdDebugSpawnEncounter
from evennia import CmdSet


class DebugCmdSet(CmdSet):
    """ Commands specific to debugging should be plugged here."""
    key = 'debug_cmdset'

    def at_cmdset_creation(self):
        self.add(CmdDebugSpawnEncounter())
