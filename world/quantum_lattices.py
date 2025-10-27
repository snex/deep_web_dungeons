"""
module for all quantum lattice behaviors
"""

import random
import sys

from evennia.prototypes import spawner
from evennia.utils.evmenu import EvMenu
from evennia.utils.utils import compress_whitespace

from world.affixes import AFFIXES
from world.item_spawner import item_spawner
from world.utils import rainbow

class QuantumLattice:
    """ base QL class with common init """
    def __init__(self, ql=None):
        self.color = "|n"
        self.name = "base quantum lattice"
        self.ql = ql
        self.msg = ("The {ql} crumbles away and transforms the"
                   " {orig_item_name} into {new_item_name}.")

    def __str__(self):
        return self.get_display_name()

    @classmethod
    def from_name(cls, name):
        """ create a QuantumLattice from name, or return None """
        if hasattr(sys.modules[__name__], name.title().replace(" ", "")):
            return getattr(sys.modules[__name__], name.title().replace(" ", ""))()
        return None

    def can_use(self, item):
        """ only implemented in subclasses """
        raise NotImplementedError

    def use(self, caller, item):
        """ only implemented in subclasses """
        raise NotImplementedError

    def get_display_name(self, custom_text=None):
        """ set color in subclass __init__, or override this method """
        return compress_whitespace(f"{self.color}{custom_text or self.name}|n")

class DustShard(QuantumLattice):
    """ dust shard rerolls a random affix """
    def __init__(self, ql=None):
        super().__init__(ql)
        self.name = "dust shard"
        self.color = "|x"

    def can_use(self, item):
        """ item must be tier 2, 3 or 4 """
        return item.tier > 1 and len(item.affixes) > 0

    def use(self, caller, item):
        """
        choose a random affix on the item, remove it, add a new random allowed affix but not the one
          that was removed
        """
        orig_item_name = str(item)
        item_prototype = spawner.prototype_from_object(item)
        current_affixes = item.affixes
        affix_to_remove = random.choice(current_affixes)
        new_affix = item_spawner.roll_affix(
            item_prototype,
            caller.levels.level,
            exclude=current_affixes + [affix_to_remove]
        )
        item.affixes.remove(affix_to_remove)
        item.affixes.append(new_affix)
        item.save()
        self.ql.at_post_use(
            caller,
            self.msg.format(
                ql=self.ql,
                orig_item_name=orig_item_name,
                new_item_name=item.get_numbered_name(1, caller)[0]
            )
        )

class StaticBloom(QuantumLattice):
    """ static bloom removes a user-selected affix """
    def __init__(self, ql=None):
        super().__init__(ql)
        self.name = "static bloom"
        self.color = "|c"
        self.menu_tree = {
            "node_select_affix": self._node_select_affix,
            "node_end_menu": self._node_end_menu,
        }

    def _node_select_affix(self, caller, raw_string, **kwargs):
        """ present the user with the affixes they can remove """
        item = caller.ndb._evmenu.item
        current_affixes = item.affixes
        text = "Select a property to remove."
        options = []
        for affix in current_affixes:
            options.append({
                "desc": AFFIXES[affix]["desc"],
                "goto": ("node_end_menu", {"item": item, "affix_to_remove": affix}),
            })
        options.append({
            "desc": "Cancel",
            "goto": ("node_end_menu", {}),
        })

        return (text, ""), options

    def _node_end_menu(self, caller, raw_string, **kwargs):
        """
        remove the chosen affix and destroy the static bloom

        do not destroy it if the user chose to cancel
        """
        item = kwargs["item"]
        orig_item_name = str(item)
        affix_to_remove = kwargs.get("affix_to_remove", None)

        if affix_to_remove:
            item.affixes.remove(affix_to_remove)
            item.save()
            self.ql.at_post_use(
                caller,
                self.msg.format(
                    ql=self.ql,
                    orig_item_name=orig_item_name,
                    new_item_name=item.get_numbered_name(1, caller)[0]
                )
            )

        return "", None

    def can_use(self, item):
        """ item must be tier 2, 3 or 4 and have at least 1 affix """
        return item.tier > 1 and len(item.affixes) > 0

    def use(self, caller, item):
        """ present the user with a menu asking them which affix to remove """
        EvMenu(
            caller,
            self.menu_tree,
            startnode="node_select_affix",
            cmd_on_exit=None,
            item=item,
        )

class EchoStone(QuantumLattice):
    """ echo stone adds a random affix """
    def __init__(self, ql=None):
        super().__init__(ql)
        self.name = "echo stone"
        self.color = "|G"

    def can_use(self, item):
        """ item must be tier 2, 3 or 4 and have less affixes than maximum allowed by the tier """
        return item.tier > 1 and len(item.affixes) < 2*(item.tier-1)

    def use(self, caller, item):
        """ add a random allowed affix to the item """
        orig_item_name = str(item)
        item_prototype = spawner.prototype_from_object(item)
        current_affixes = item.affixes
        new_affix = item_spawner.roll_affix(
            item_prototype,
            caller.levels.level,
            exclude=current_affixes
        )
        item.affixes.append(new_affix)
        item.save()
        self.ql.at_post_use(
            caller,
            self.msg.format(
                ql=self.ql,
                orig_item_name=orig_item_name,
                new_item_name=item.get_numbered_name(1, caller)[0]
            )
        )

class ResonanceCrystal(QuantumLattice):
    """ resonance crystal converts tier 1 into tier 2 """
    def __init__(self, ql=None):
        super().__init__(ql)
        self.name = "resonance crystal"
        self.color = "|y"

    def can_use(self, item):
        """ item must be tier 1 """
        return item.tier == 1

    def use(self, caller, item):
        """ convert item to tier 2 """
        orig_item_name = str(item)
        item.tier = 2
        item.save()
        self.ql.at_post_use(
            caller,
            self.msg.format(
                ql=self.ql,
                orig_item_name=orig_item_name,
                new_item_name=item.get_numbered_name(1, caller)[0]
            )
        )

class SingularityShard(QuantumLattice):
    """ singularity shard reduces item tier by 1 level """
    def __init__(self, ql=None):
        super().__init__(ql)
        self.name = "singularity shard"
        self.color = "|[x|X"

    def can_use(self, item):
        """ item must be tier 2, 3 or 4 """
        return item.tier > 1

    def use(self, caller, item):
        """
        item goes down 1 tier. if the item has more affixes than allowed by the new tier,
        random affixes are removed until the new tier can support them
        """
        orig_item_name = str(item)
        item.tier -= 1

        while len(item.affixes) > 2*(item.tier-1):
            affix_to_remove = random.choice(item.affixes)
            item.affixes.remove(affix_to_remove)

        item.save()
        self.ql.at_post_use(
            caller,
            self.msg.format(
                ql=self.ql,
                orig_item_name=orig_item_name,
                new_item_name=item.get_numbered_name(1, caller)[0]
            )
        )

class PhasePearl(QuantumLattice):
    """ phase pearl converts tier 2 into tier 3 """
    def __init__(self, ql=None):
        super().__init__(ql)
        self.name = "phase pearl"
        self.color = "|530"

    def can_use(self, item):
        """ item must be tier 2 """
        return item.tier == 2

    def use(self, caller, item):
        """ convert item to tier 3 """
        orig_item_name = str(item)
        item.tier = 3
        item.save()
        self.ql.at_post_use(
            caller,
            self.msg.format(
                ql=self.ql,
                orig_item_name=orig_item_name,
                new_item_name=item.get_numbered_name(1, caller)[0]
            )
        )

class VoidSpark(QuantumLattice):
    """ void spark removes all affixes """
    def __init__(self, ql=None):
        super().__init__(ql)
        self.name = "void spark"
        self.color = "|M"

    def can_use(self, item):
        """ item must be tier 2, 3 or 4 and have affixes """
        return item.tier > 1 and len(item.affixes) > 0

    def use(self, caller, item):
        """ remove all item affixes """
        orig_item_name = str(item)
        item.affixes = []
        item.save()
        self.ql.at_post_use(
            caller,
            self.msg.format(
                ql=self.ql,
                orig_item_name=orig_item_name,
                new_item_name=item.get_numbered_name(1, caller)[0]
            )
        )

class ChromaticHeart(QuantumLattice):
    """ chromatic heart converts tier 3 into tier 4 """
    def __init__(self, ql=None):
        super().__init__(ql)
        self.name = "chromatic heart"

    def can_use(self, item):
        """ item must be tier 3 """
        return item.tier == 3

    def use(self, caller, item):
        """ convert item to tier 4 """
        orig_item_name = str(item)
        item.tier = 4
        item.save()
        self.ql.at_post_use(
            caller,
            self.msg.format(
                ql=self.ql,
                orig_item_name=orig_item_name,
                new_item_name=item.get_numbered_name(1, caller)[0]
            )
        )

    def get_display_name(self, custom_text=None):
        return rainbow(compress_whitespace(custom_text or self.name))

class NexusDiamond(QuantumLattice):
    """ nexus diamond converts any equipment item into tier 4 """
    def __init__(self, ql=None):
        super().__init__(ql)
        self.name = "nexus diamond"
        self.color = "|[w|x"

    def can_use(self, item):
        """ item must be tier 1, 2 or 3 """
        return item.tier > 0 and item.tier < 4

    def use(self, caller, item):
        """ convert item to tier 4 """
        orig_item_name = str(item)
        item.tier = 4
        item.save()
        self.ql.at_post_use(
            caller,
            self.msg.format(
                ql=self.ql,
                orig_item_name=orig_item_name,
                new_item_name=item.get_numbered_name(1, caller)[0]
            )
        )
