"""
Test scripts.
"""

from unittest.mock import MagicMock, patch
from evennia.utils.create import create_script
from evennia.utils.test_resources import EvenniaTest

class TestGlobalRecoveryScript(EvenniaTest):
    """ Test GlobalRecoveryScript """
    def setUp(self):
        super().setUp()
        self.grs = create_script(
            typeclass="typeclasses.scripts.GlobalRecoveryScript",
            key="grs",
            obj=None,
            interval=6,
            persistent=False,
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
