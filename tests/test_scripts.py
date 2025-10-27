"""
Test scripts.
"""

from unittest.mock import MagicMock, patch
from evennia.utils.create import create_script
from evennia.utils.test_resources import EvenniaTest

from typeclasses.npcs import ShopKeeper

class TestGlobalRecoveryScript(EvenniaTest):
    """ Test GlobalRecoveryScript """
    def setUp(self):
        super().setUp()
        self.grs = create_script(
            typeclass="typeclasses.scripts.GlobalRecoveryScript",
            key="grs",
            obj=None,
            interval=1,
            persistent=True,
            autostart=True
        )

    def test_at_stop(self):
        """ Test that the script restarts itself if it ever stops. """
        with patch("typeclasses.scripts.GlobalRecoveryScript.start") as mock_start:
            self.grs.at_stop()
            mock_start.assert_called_once()

    def test_at_repeat(self):
        """ Test that the script repeats. """
        self.char1.at_recovery = MagicMock()
        self.grs.force_repeat()
        self.char1.at_recovery.assert_called_once()

class TestVendorRestockScript(EvenniaTest):
    """ Test VendorRestockScript """
    def setUp(self):
        super().setUp()
        self.shopkeeper = ShopKeeper.create(
            key="shopkeeper",
            menudata="world.npcs.your_mom"
        )[0]
        self.vrs = create_script(
            typeclass="typeclasses.scripts.VendorRestockScript",
            key="vrs",
            obj=None,
            interval=1,
            persistent=True,
            autostart=True
        )

    def test_at_stop(self):
        """ Test that the script restarts itself if it ever stops. """
        with patch("typeclasses.scripts.VendorRestockScript.start") as mock_start:
            self.vrs.at_stop()
            mock_start.assert_called_once()

    def test_at_repeat(self):
        """ Test that the script repeats. """
        self.char1.clear_buyable_gear = MagicMock()
        self.vrs.force_repeat()
        self.char1.clear_buyable_gear.assert_called_once_with([self.shopkeeper])

        self.shopkeeper.clean_old_inventory = MagicMock()
        self.vrs.force_repeat()
        self.shopkeeper.clean_old_inventory.assert_called_once()
