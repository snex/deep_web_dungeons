"""
Scripts

Scripts are powerful jacks-of-all-trades. They have no in-game
existence and can be used to represent persistent game systems in some
circumstances. Scripts can also have a time component that allows them
to "fire" regularly or a limited number of times.

There is generally no "tree" of Scripts inheriting from each other.
Rather, each script tends to inherit from the base Script class and
just overloads its hooks to have it perform its function.

"""

from evennia.scripts.scripts import DefaultScript
from evennia.utils.search import search_typeclass

class Script(DefaultScript):
    """ Script Base class. This is required for Evennia to create objects. """

class GlobalRecoveryScript(Script):
    """
    Script to handle periodic recovery for all players.
    """

    def at_stop(self, **kwargs):
        """
        This script should never stop, otherwise players might stop recovering.
        """

        self.start()

    def at_repeat(self, **kwargs):
        """
        Cycle through all characters and execute their recovery
        """
        characters = search_typeclass(
            "typeclasses.characters.BaseCharacter",
            include_children=True
        )
        for character in characters:
            character.at_recovery()
