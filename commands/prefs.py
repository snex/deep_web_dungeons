"""
Commands for entering the user preferences menu.
"""

from world.prefs import start_prefs
from .command import Command

class CmdPrefs(Command):
    key = "prefs"

    def func(self):
        account = self.account
        start_prefs(account, session=self.session)
