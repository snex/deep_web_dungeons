"""
test NPC behavior
"""

from unittest.mock import patch

from evennia.utils.create import create_object
from evennia.utils.test_resources import EvenniaTest

from typeclasses.npcs import InsultNPC, WanderingNPC
from world.enums import CardinalDirections

class TestWanderingNPC(EvenniaTest):
    """ test WanderingNPC behavior """
    def setUp(self):
        super().setUp()
        self.wandering_npc = create_object(
            WanderingNPC,
            key="wander"
        )

    @patch("random.randrange")
    def test_creation(self, mock_randrange):
        """ test that creating npc creates the timer """
        mock_randrange.side_effect = [66, 250]
        with patch("typeclasses.npcs.repeat") as mock_repeat:
            mock_repeat.return_value = True
            npc = create_object(
                WanderingNPC,
                key="wander"
            )
            mock_repeat.assert_called_once_with(66, npc.wander)
        self.assertEqual(npc.wander_rate, 66)
        self.assertEqual(npc.wander_chance, 0.25)

    def test_deletion(self):
        """ test that deleting npc disables their timer """
        timer = self.wandering_npc.wander_timer
        with patch("typeclasses.npcs.unrepeat") as mock_unrepeat:
            self.wandering_npc.delete()
            mock_unrepeat.assert_called_once_with(timer)

    @patch("random.random")
    def test_wander(self, mock_random):
        """ test wander action """
        mock_random.return_value = 0.01
        with patch("typeclasses.npcs.WanderingNPC._do_wander") as mock_do_wander:
            self.wandering_npc.wander()
            mock_do_wander.assert_called_once_with(CardinalDirections)

class TestShoutNPC(EvenniaTest):
    """ test ShoutNPC behavior """
    def setUp(self):
        super().setUp()
        self.insult_npc = create_object(
            InsultNPC,
            key="insult"
        )
        self.insult_npc.location = self.room1

    @patch("random.randrange")
    def test_creation(self, mock_randrange):
        """ test creating npc creates the timer """
        mock_randrange.side_effect = [66, 250]
        with patch("typeclasses.npcs.repeat") as mock_repeat:
            mock_repeat.return_value = True
            npc = create_object(
                InsultNPC,
                key="insult"
            )
            mock_repeat.assert_called_once_with(66, npc.shout)
        self.assertEqual(npc.shout_rate, 66)
        self.assertEqual(npc.shout_chance, 0.25)

    def test_deletion(self):
        """ test that deleting npc disables their timer """
        timer = self.insult_npc.shout_timer
        with patch("typeclasses.npcs.unrepeat") as mock_unrepeat:
            self.insult_npc.delete()
            mock_unrepeat.assert_called_once_with(timer)

    def test_at_talk(self):
        """ test shout NPC being talked to """
        with patch("typeclasses.npcs.InsultNPC._do_shout") as mock_do_shout:
            self.insult_npc.at_talk(self.char1)
            mock_do_shout.assert_called_once_with(self.char1)

    def test_at_damage(self):
        """ test shout NPC being immune to damage """
        with patch("typeclasses.npcs.InsultNPC._do_shout") as mock_do_shout:
            self.insult_npc.at_damage(10, self.char1)
            mock_do_shout.assert_called_once_with(self.char1)
        with patch("typeclasses.rooms.Room.msg_contents") as mock_msg:
            self.insult_npc.at_damage(10, self.char1)
            mock_msg.assert_any_call(
                "$You() swiftly $conj(dodge) a pathetic attack from $You(attacker).",
                from_obj=self.insult_npc,
                mapping={"attacker": self.char1}
            )

    @patch("random.choice")
    @patch("random.random")
    def test_shout(self, mock_random, mock_choice):
        """ test shout """
        mock_random.return_value = 0.01
        mock_choice.return_value = self.char2
        with patch("typeclasses.npcs.InsultNPC._do_shout") as mock_do_shout:
            self.insult_npc.shout()
            mock_do_shout.assert_called_once_with(self.char2)
