"""
module for all quantum lattice behaviors when used
"""

import random

from evennia.prototypes import spawner
from evennia.utils.evmenu import EvMenu

from world.affixes import AFFIXES
from world.item_spawner import item_spawner

class QuantumLattice:
    """ base QL class with common init """
    def __init__(self, ql, item):
        self.ql = ql
        self.item = item
        self.orig_item_name = item.get_display_name()
        self.msg = ("The {ql_name} crumbles away and transforms the"
                   " {orig_item_name} into {new_item_name}.")

    def can_use(self):
        """ only implemented in subclasses """
        raise NotImplementedError

    def use(self, caller):
        """ only implemented in subclasses """
        raise NotImplementedError

class DustShard(QuantumLattice):
    """ dust shard rerolls a random affix """
    def can_use(self):
        """ item must be tier 2, 3 or 4 """
        return self.item.tier > 1 and len(self.item.affixes) > 0

    def use(self, caller):
        """
        choose a random affix on the item, remove it, add a new random allowed affix but not the one
          that was removed
        """
        item_prototype = spawner.prototype_from_object(self.item)
        current_affixes = self.item.affixes
        affix_to_remove = random.choice(current_affixes)
        new_affix = item_spawner.roll_affix(
            item_prototype,
            caller.levels.level,
            exclude=current_affixes + [affix_to_remove]
        )
        self.item.affixes.remove(affix_to_remove)
        self.item.affixes.append(new_affix)
        self.item.save()
        self.ql.at_post_use(
            caller,
            self.msg.format(
                ql_name=self.ql.get_display_name(),
                orig_item_name=self.orig_item_name,
                new_item_name=self.item.get_numbered_name(1, caller)[0]
            )
        )

class StaticBloom(QuantumLattice):
    """ static bloom removes a user-selected affix """
    def __init__(self, ql, item):
        super().__init__(ql, item)
        self.menu_tree = {
            "node_select_affix": self._node_select_affix,
            "node_end_menu": self._node_end_menu,
        }

    def _node_select_affix(self, caller, raw_string, **kwargs):
        """ present the user with the affixes they can remove """
        current_affixes = self.item.affixes
        text = "Select a property to remove."
        options = []
        for affix in current_affixes:
            options.append({
                "desc": AFFIXES[affix]["desc"],
                "goto": ("node_end_menu", {"affix_to_remove": affix}),
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
        affix_to_remove = kwargs.get("affix_to_remove", None)

        if affix_to_remove:
            self.item.affixes.remove(affix_to_remove)
            self.item.save()
            self.ql.at_post_use(
                caller,
                self.msg.format(
                    ql_name=self.ql.get_display_name(),
                    orig_item_name=self.orig_item_name,
                    new_item_name=self.item.get_numbered_name(1, caller)[0]
                )
            )

        return "", None

    def can_use(self):
        """ item must be tier 2, 3 or 4 and have at least 1 affix """
        return self.item.tier > 1 and len(self.item.affixes) > 0

    def use(self, caller):
        """ present the user with a menu asking them which affix to remove """
        EvMenu(
            caller,
            self.menu_tree,
            startnode="node_select_affix",
            cmd_on_exit=None,
        )

class EchoStone(QuantumLattice):
    """ echo stone adds a random affix """
    def can_use(self):
        """ item must be tier 2, 3 or 4 and have less affixes than maximum allowed by the tier """
        return self.item.tier > 1 and len(self.item.affixes) < 2*(self.item.tier-1)

    def use(self, caller):
        """ add a random allowed affix to the item """
        item_prototype = spawner.prototype_from_object(self.item)
        current_affixes = self.item.affixes
        new_affix = item_spawner.roll_affix(
            item_prototype,
            caller.levels.level,
            exclude=current_affixes
        )
        self.item.affixes.append(new_affix)
        self.item.save()
        self.ql.at_post_use(
            caller,
            self.msg.format(
                ql_name=self.ql.get_display_name(),
                orig_item_name=self.orig_item_name,
                new_item_name=self.item.get_numbered_name(1, caller)[0]
            )
        )

class ResonanceCrystal(QuantumLattice):
    """ resonance crystal converts tier 1 into tier 2 """
    def can_use(self):
        """ item must be tier 1 """
        return self.item.tier == 1

    def use(self, caller):
        """ convert item to tier 2 """
        self.item.tier = 2
        self.item.save()
        self.ql.at_post_use(
            caller,
            self.msg.format(
                ql_name=self.ql.get_display_name(),
                orig_item_name=self.orig_item_name,
                new_item_name=self.item.get_numbered_name(1, caller)[0]
            )
        )

class SingularityShard(QuantumLattice):
    """ singularity shard reduces item tier by 1 level """
    def can_use(self):
        """ item must be tier 2, 3 or 4 """
        return self.item.tier > 1

    def use(self, caller):
        """
        item goes down 1 tier. if the item has more affixes than allowed by the new tier,
        random affixes are removed until the new tier can support them
        """
        self.item.tier -= 1

        while len(self.item.affixes) > 2*(self.item.tier-1):
            affix_to_remove = random.choice(self.item.affixes)
            self.item.affixes.remove(affix_to_remove)

        self.item.save()
        self.ql.at_post_use(
            caller,
            self.msg.format(
                ql_name=self.ql.get_display_name(),
                orig_item_name=self.orig_item_name,
                new_item_name=self.item.get_numbered_name(1, caller)[0]
            )
        )

class PhasePearl(QuantumLattice):
    """ phase pearl converts tier 2 into tier 3 """
    def can_use(self):
        """ item must be tier 2 """
        return self.item.tier == 2

    def use(self, caller):
        """ convert item to tier 3 """
        self.item.tier = 3
        self.item.save()
        self.ql.at_post_use(
            caller,
            self.msg.format(
                ql_name=self.ql.get_display_name(),
                orig_item_name=self.orig_item_name,
                new_item_name=self.item.get_numbered_name(1, caller)[0]
            )
        )

class VoidSpark(QuantumLattice):
    """ void spark removes all affixes """
    def can_use(self):
        """ item must be tier 2, 3 or 4 and have affixes """
        return self.item.tier > 1 and len(self.item.affixes) > 0

    def use(self, caller):
        """ remove all item affixes """
        self.item.affixes = []
        self.item.save()
        self.ql.at_post_use(
            caller,
            self.msg.format(
                ql_name=self.ql.get_display_name(),
                orig_item_name=self.orig_item_name,
                new_item_name=self.item.get_numbered_name(1, caller)[0]
            )
        )

class ChromaticHeart(QuantumLattice):
    """ chromatic heart converts tier 3 into tier 4 """
    def can_use(self):
        """ item must be tier 3 """
        return self.item.tier == 3

    def use(self, caller):
        """ convert item to tier 4 """
        self.item.tier = 4
        self.item.save()
        self.ql.at_post_use(
            caller,
            self.msg.format(
                ql_name=self.ql.get_display_name(),
                orig_item_name=self.orig_item_name,
                new_item_name=self.item.get_numbered_name(1, caller)[0]
            )
        )

class NexusDiamond(QuantumLattice):
    """ nexus diamond converts any equipment item into tier 4 """
    def can_use(self):
        """ item must be tier 1, 2 or 3 """
        return self.item.tier > 0 and self.item.tier < 4

    def use(self, caller):
        """ convert item to tier 4 """
        self.item.tier = 4
        self.item.save()
        self.ql.at_post_use(
            caller,
            self.msg.format(
                ql_name=self.ql.get_display_name(),
                orig_item_name=self.orig_item_name,
                new_item_name=self.item.get_numbered_name(1, caller)[0]
            )
        )
