"""
a command for Builders to be able to spawn randomly rolled objects
using the ItemSpawner system.
"""

from evennia.commands.default.muxcommand import MuxCommand

from world.item_spawner import item_spawner

class CmdSpawnRand(MuxCommand):
    """
    spawn randomly rolled objects using ItemSpawner

    Usage:
        spawn_rand [count] [level]

    Args:
        |wcount|n     - The number of items to spawn. Defaults to 1.
        |wlevel|n     - Only allow items of [level] or below to spawn. Defaults to 1.

    Example:
        spawn 5
        spawn 5 10
    """

    key = "@spawn_rand"
    aliases = ["sr"]
    locks = "cmd:perm(spawn) or perm(Builder)"
    help_category = "Building"

    def __init__(self):
        super().__init__()
        self.level = 1
        self.count = 1

    def parse(self):
        """ assign the level and count """

        super().parse()
        self.level = self.caller.levels.level
        args = self.args.split(" ", 1)

        try:
            self.count = int(args[0])
        except ValueError:
            self.count = 1

        if len(args) == 1:
            return

        try:
            self.level = int(args[1])
        except ValueError:
            self.level = self.caller.levels.level

    def func(self):
        """ perform the spawning """

        for _ in range(self.count):
            item_spawner.spawn_item(self.level, caller=self.caller)
