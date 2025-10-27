"""
Typeclasses defining NPCs. This includes both friends and enemies, only separated by their AI.

"""
import random
import time

from evennia.typeclasses.attributes import AttributeProperty
from evennia.utils.evmenu import EvMenu
from evennia.utils.utils import inherits_from, repeat, unrepeat
from world.common.dialog.insults import Insult
from world.enums import Allegiance, CardinalDirections
from .characters import BaseCharacter, Character

class NPC(BaseCharacter):
    """
    Base class for all NPCs.
    """

    is_pc = False

    desc = AttributeProperty(default="This is a character.", autocreate=False)
    armor = AttributeProperty(default=1, autocreate=False)  # +10 to get armor defense
    morale = AttributeProperty(default=9, autocreate=False)
    allegiance = AttributeProperty(default=Allegiance.ALLEGIANCE_HOSTILE, autocreate=False)

    is_idle = AttributeProperty(default=False, autocreate=False)

    weapon = AttributeProperty(autocreate=False)  # instead of inventory

    def at_object_creation(self):
        """
        Start with max health.

        """
        getattr(self, "full_recovery", lambda:None)()

    def _do_wander(self, allowed_directions):
        candidates = [
            direction.key for direction in self.location.exits
            if direction.key in allowed_directions
        ]

        if candidates:
            wander_dir = random.choice(candidates)
            self.execute_cmd(wander_dir)
        else:
            self.location.msg_contents(
                "$You() $conj(try) to escape but there is nowhere to go!",
                from_obj=self
            )

class WanderingNPC(NPC):
    """
    Wandering NPCs will wander around randomly."
    """

    wander_timer = AttributeProperty(default=None, autocreate=False)
    wander_rate = AttributeProperty(default=60, autocreate=False)
    wander_chance = AttributeProperty(default=0.5, autocreate=False)

    def at_object_creation(self):
        self.wander_rate = random.randrange(30, 120)
        self.wander_chance = random.randrange(300, 700) / 1000
        self.wander_timer = repeat(self.wander_rate, self.wander)

    def at_object_delete(self):
        if self.wander_timer is not None:
            unrepeat(self.wander_timer)
        return True

    def wander(self):
        """ Roll to see if the NPC should wander, then wander if so. """
        if random.random() < self.wander_chance:
            self._do_wander(CardinalDirections)

class InsultNPC(NPC):
    """
    Insult NPCs will wander around and insult any players they see.
    """

    insult_timer = AttributeProperty(default=None, autocreate=False)
    insult_rate = AttributeProperty(default=60, autocreate=False)
    insult_chance = AttributeProperty(default=0.5, autocreate=False)

    def at_object_creation(self):
        self.insult_rate = random.randrange(30, 120)
        self.insult_chance = random.randrange(300, 700) / 1000
        self.insult_timer = repeat(self.insult_rate, self.insult)

    def at_object_delete(self):
        if self.insult_timer is not None:
            unrepeat(self.insult_timer)
        return True

    def _say_insult(self, target):
        insult = Insult(target.key, target.gender).generate_insult()
        self.execute_cmd(f"say |w{insult}|n")
        self._do_wander(CardinalDirections)

    def at_talk(self, talker):
        """ When talked to, say an insult. """
        self._say_insult(talker)

    def at_damage(self, _damage, attacker=None):
        """
        Insult NPCs are generally immortal and will insult and run if hit."

        """

        if self.combat:
            self.combat.end_combat()
        self.location.msg_contents(
            "$You() swiftly $conj(dodge) a pathetic attack from $You(attacker).",
            from_obj=self,
            mapping={"attacker": attacker}
        )
        self._say_insult(attacker)

    def insult(self):
        """ Roll to see if the NPC should say an insult, then say it if so. """
        if random.random() < self.insult_chance:
            pcs = [obj for obj in self.location.contents if inherits_from(obj, Character)]
            if pcs:
                target = random.choice(pcs)
                self._say_insult(target)


class TalkativeNPC(NPC):
    """
    Talkative NPCs can be addressed by `talk [to] <npc>`. This opens a chat menu with
    communication options. The menu is created with the npc and we override the .create
    to allow passing in the menu nodes.

    """

    menudata = AttributeProperty({}, autocreate=False)
    menu_kwargs = AttributeProperty({}, autocreate=False)
    # text shown when greeting at the start of a conversation. If this is an
    # iterable, a random reply will be chosen by the menu
    hi_text = AttributeProperty("Hi!", autocreate=False)

    def at_damage(self, _damage, attacker=None):
        """
        Talkative NPCs are generally immortal (we don't deduct HP here by default)."

        """
        attacker.msg(f'{self.key} dodges the damage and shouts "|wHey! What are you doing?|n"')
        if self.combat:
            self.combat.end_combat()

    @classmethod
    def create(cls, key, account=None, caller=None, method="create", **kwargs):
        """
        Overriding the creation of the NPC, allowing some extra `**kwargs`.

        Args:
            key (str): Name of the new object.
            account (Account, optional): Account to attribute this object to.

        Keyword Args:
            description (str): Brief description for this object (same as default Evennia)
            ip (str): IP address of creator (for object auditing) (same as default Evennia).
            menudata (dict or str): The `menudata` argument to `EvMenu`. This is either a dict of
                `{"nodename": <node_callable>,...}` or the python-path to a module containing
                such nodes (see EvMenu docs). This will be used to generate the chat menu
                chat menu for the character that talks to the NPC (which means the `at_talk` hook
                is called (by our custom `talk` command).
            menu_kwargs (dict): This will be passed as `**kwargs` into `EvMenu` when it
                is created. Make sure this dict can be pickled to an Attribute.

        Returns:
            tuple: `(new_character, errors)`. On error, the `new_character` is `None` and
            `errors` is a `list` of error strings (an empty list otherwise).


        """
        menudata = kwargs.pop("menudata", None)
        menu_kwargs = kwargs.pop("menu_kwargs", {})

        new_object, errors = super().create(
            key, account=account, attributes=(("menudata", menudata), ("menu_kwargs", menu_kwargs))
        )

        return new_object, errors

    def at_talk(self, talker, startnode="node_start", session=None, **kwargs):
        """
        Called by the `talk` command when another entity addresses us.

        Args:
            talker (Object): The one talking to us.
            startnode (str, optional): Allows to start in a different location in the menu tree.
                The given node must exist in the tree.
            session (Session, optional): The talker's current session, allows for routing
                correctly in multi-session modes.
            **kwargs: This will be passed into the `EvMenu` creation and appended and `menu_kwargs`
                given to the NPC at creation.

        Notes:
            We pass `npc=self` into the EvMenu for easy back-reference. This will appear in the
            `**kwargs` of the start node.

        """
        menu_kwargs = {**self.menu_kwargs, **kwargs}
        EvMenu(
            talker,
            self.menudata,
            startnode=startnode,
            session=session,
            cmd_on_exit=None,
            auto_quit=False,
            npc=self,
            **menu_kwargs
        )

class QuestGiver(TalkativeNPC):
    """
    An NPC that acts as a dispenser of quests.

    """


class ShopKeeper(TalkativeNPC):
    """
    ShopKeeper NPC.

    """

    def at_damage(self, _damage, attacker=None):
        """
        Immortal - we don't deduct any damage here.

        """
        attacker.msg(
            f"{self.key} brushes off the hit and shouts "
            '"|wHey! This is not the way to get a discount!|n"'
        )
        if self.combat:
            self.combat.end_combat()

    def clean_old_inventory(self):
        """
        delete items that were created over a day ago from shopkeeper's inventory to avoid
            database buildup
        """

        for item in self.contents:
            if time.time() - item.created_at > (60 * 60 * 24):
                item.delete()
