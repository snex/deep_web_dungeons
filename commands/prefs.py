"""
Commands for entering the user preferences menu.
"""

from evennia.utils.logger import log_err
from evennia.utils.utils import inherits_from

from typeclasses.accounts import Account
from world.prefs import start_prefs
from .command import Command

class CmdPrefs(Command):
    """ Handle the prefs command. """
    key = "prefs"

    def func(self):
        account = self.caller

        if not inherits_from(account, Account):
            account = getattr(account, "account", None)

        if not account:
            log_err(f"Something called the `prefs` command without an account! {self.caller}")
            raise RuntimeError

        start_prefs(account)
