"""
Testing Quest functionality.

"""

from unittest.mock import MagicMock

from evennia.utils.test_resources import EvenniaTest

from world import quests
from typeclasses.objects import Object
from .mixins import AinneveTestMixin


class _TestQuest(quests.Quest):
    """
    Test quest.

    """

    key = "testquest"
    desc = "A test quest!"

    start_step = "a"
    end_text = "This task is completed."

    help_a = "You need to do A first."
    help_b = "Next, do B."

    def step_a(self, *args, **kwargs):
        """
        Quest-step A is completed when quester carries an item with tag "QuestA" and category
        "quests".
        """
        # note - this could be done with a direct db query instead to avoid a loop, for a
        # unit test it's fine though
        if any(obj for obj in self.quester.contents if obj.tags.has("QuestA", category="quests")):
            self.quester.msg("Completed step A of quest!")
            self.current_step = "b"
            self.progress()

    def step_b(self, *args, **kwargs):
        """
        Quest-step B is completed when the progress-check is called with a special kwarg
        "complete_quest_B"

        """
        if kwargs.get("complete_quest_B", False):
            self.quester.msg("Completed step B of quest!")
            self.quester.db.test_quest_counter = 0
            self.current_step = "c"
            self.progress()

    def help_c(self):
        """Testing the method-version of getting a help entry"""
        return f"Only C left now, {self.quester.key}!"

    def step_c(self, *args, **kwargs):
        """
        Step C (final) step of quest completes when a counter on quester is big enough.

        """
        if self.quester.db.test_quest_counter and self.quester.db.test_quest_counter > 5:
            self.quester.msg("Quest complete! Get XP rewards!")
            self.quester.levels.add_xp(10)
            self.complete()

    def cleanup(self):
        """
        Cleanup data related to quest.

        """
        del self.quester.db.test_quest_counter


class QuestTest(AinneveTestMixin, EvenniaTest):
    """
    Test questing.

    """

    def setUp(self):
        super().setUp()
        self.char1.quests.add(_TestQuest)
        self.char1.msg = MagicMock()

    def _get_quest(self):
        return self.char1.quests.get(_TestQuest.key)

    def _fulfill_a(self):
        """Fulfill quest step A"""
        Object.create(
            key="quest obj", location=self.char1, tags=(("QuestA", "quests"),)
        )

    def _fulfill_c(self):
        """Fullfill quest step C"""
        self.char1.db.test_quest_counter = 6

    def test_help(self):
        """Get help"""
        # get help for all quests
        help_txt = self.char1.quests.get_help()
        self.assertEqual(help_txt, ["|ctestquest|n\n A test quest!\n\n - You need to do A first."])

        # get help for one specific quest
        help_txt = self.char1.quests.get_help(_TestQuest.key)
        self.assertEqual(help_txt, ["|ctestquest|n\n A test quest!\n\n - You need to do A first."])

        # help for finished quest
        self._get_quest().is_completed = True
        help_txt = self.char1.quests.get_help()
        self.assertEqual(help_txt, ["|ctestquest|n\n A test quest!\n\n - This quest is completed!"])

    def test_progress__fail(self):
        """
        Check progress without having any.
        """
        # progress all quests
        self.char1.quests.progress()
        # progress one quest
        self.char1.quests.progress(_TestQuest.key)

        # still on step A
        self.assertEqual(self._get_quest().current_step, "a")

    def test_progress(self):
        """
        Fulfill the quest steps in sequess

        """
        # A requires a certain object in inventory
        self._fulfill_a()
        self.char1.quests.progress()
        self.assertEqual(self._get_quest().current_step, "b")

        # B requires progress be called with specific kwarg
        # should not step (no kwarg)
        self.char1.quests.progress()
        self.assertEqual(self._get_quest().current_step, "b")

        # should step (kwarg sent)
        self.char1.quests.progress(complete_quest_B=True)
        self.assertEqual(self._get_quest().current_step, "c")

        # C requires a counter Attribute on char be high enough
        self._fulfill_c()
        self.char1.quests.progress()
        self.assertEqual(self._get_quest().current_step, "c")  # still on last step
        self.assertEqual(self._get_quest().is_completed, True)
