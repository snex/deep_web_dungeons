""" createchar command """

from evennia.commands.default.account import CmdCharCreate as DefaultCmdCharCreate

from world.chargen import start_chargen

# disable pylint for this as it's an override
# pylint: disable=too-few-public-methods
class CmdCharCreate(DefaultCmdCharCreate):
    """ createchar command """
    def func(self):
        account = self.account
        start_chargen(account, session=self.session)
