"""
module for spawning random items

the item spawned will take into account the following:

    level of the mob or character causing the item to spawn
        uses poisson distribution with mean of the level

    character class of the character causing the item to spawn
        items will be slightly more likely to be usable by the character

    for mob drops, the level will be based on the level of the mob.
    any other drops / NPC shop generation, we will use the character performing the interaction
        but that logic will be handled elsewhere. in here, the level/class just get passed in
"""

import copy
import random
from bisect import bisect_left

from evennia.prototypes import spawner
from evennia.utils import logger
from evennia.utils.utils import lazy_property, make_iter

from world.drop_tables import DROP_TABLES
from world.utils import list_flatten

class PrototypeManager:
    """
    class to hold the prototypes for droppables and rollables

    droppables are base items, rollables are affixes, materials, or other qualities that can be
        applied to droppables
    """

    @lazy_property
    def _all_droppables(self):
        """ all droppable prototypes """
        return [
            spawner.flatten_prototype(droppable)
            for droppable in spawner.search_prototype(tags=["droppable"])
        ]

    def droppables(self, *args, **kwargs):
        """
        droppables with the desired tags or without excluded tags

        Args:
            each positional arg is a tag to be searched against

        Keyword Args:
            if "exclude=[str or list]" is present, these prototypes will be excluded
            useful if you want to only roll weapons, only roll quantum_lattices, etc.
            excludes will search against typeclass AND tags

            if "must_include=[str or list]" is  present, these prototypes will only
            be included if they have ALL tags in must_include. useful if you want
            to roll affixes only for Weapons, for example
        """

        droppables = self._all_droppables
        excludes = make_iter(kwargs.get("exclude", []))
        must_include = make_iter(kwargs.get("must_include", []))
        logger.log_err(f"droppables({args}, {kwargs})")

        droppables = [
            droppable
            for droppable in droppables
            if not args
            or list(filter(lambda i: i in args, droppable["prototype_tags"]))
        ]

        droppables = [
            droppable
            for droppable in droppables
            if not must_include
            or all(i in droppable["prototype_tags"] for i in must_include)
        ]

        droppables = [
            droppable
            for droppable in droppables
            if droppable["prototype_key"] not in excludes
            and droppable["typeclass"] not in excludes
            and not list(filter(lambda i: i in excludes, droppable["prototype_tags"]))
        ]

        return droppables

    @lazy_property
    def _all_rollables(self):
        """
        all rollable prototypes

        don't flatten them because then they will get typeclass=typeclasses.objects.Object
            and this will mess with the composition
        """

        return spawner.search_prototype(tags=["rollable"])

    def rollables(self, *args, **kwargs):
        """
        rollables with the desired tags or without excluded tags

        Args:
            each positional arg is a tag to be searched against

        Keyword Args:
            if "exclude=[str or list]" is present, these prototypes will be excluded
            useful if you have already rolled a given rollable and don't want to allow it again
            or to disallow combinations of rollables (e.g. cant combine `based` and `cringe`)

            if "must_include=[str or list]" is  present, these prototypes will only
            be included if they have ALL tags in must_include. useful if you want
            to roll affixes only for Weapons, for example
        """

        rollables = self._all_rollables
        excludes = make_iter(kwargs.get("exclude", []))
        must_include = make_iter(kwargs.get("must_include", []))
        logger.log_err(f"rollables({args}, {kwargs})")

        rollables = [
            rollable
            for rollable in rollables
            if not args
            or list(filter(lambda i: i in args, rollable["prototype_tags"]))
        ]

        rollables = [
            rollable
            for rollable in rollables
            if not must_include
            or all(i in rollable["prototype_tags"] for i in must_include)
        ]

        rollables = [
            rollable
            for rollable in rollables
            if rollable["prototype_key"] not in excludes
            and not list(filter(lambda i: i in excludes, rollable["prototype_tags"]))
        ]

        return rollables

    def _prototype_within_distance_of_level(self, prototype, level, distance):
        prototype_req_level = list(
            filter(lambda tup: "required_level" in tup, prototype["attrs"])
        )[0][1]
        return abs(prototype_req_level - level) <= distance

    def droppables_by_level(self, level, *args, **kwargs):
        """
        get the droppables within +-5 levels of the passed in level
        """
        return [
            droppable for droppable in self.droppables(*args, **kwargs)
            if "required_level" not in list_flatten(droppable["attrs"])
            or self._prototype_within_distance_of_level(droppable, level, 5)
        ]

    def rollables_by_level(self, level, *args, **kwargs):
        """
        get the rollables within +-5 levels of the passed in level,
            or rollables with no attrs at all
        """
        return [
            rollable for rollable in self.rollables(*args, **kwargs)
            if not rollable.get("attrs")
            or self._prototype_within_distance_of_level(rollable, level, 5)
        ]

class ItemSpawner:
    """
    class to handle rolling from drop tables, then
    assembling an item from prototypes and spawning it
    """

    def __init__(self):
        self.pm = PrototypeManager()
        self.drop_tables = {}

        for key, table in DROP_TABLES.items():
            self.drop_tables[key] = []
            table_sum = 0
            for item_key, freq in table:
                table_sum += freq
                new_entry = (item_key, table_sum)
                self.drop_tables[key].append(new_entry)

    def roll_drop_table(self, table_name="generic", cclass=None):
        """ roll through the drop tables and return a leaf node """
        # we aren't iterating a dictionary, pylint!
        # pylint: disable=consider-iterating-dictionary
        while table_name in self.drop_tables.keys():
            table = self.drop_tables[table_name]
            logger.log_err(f"table: {table}")
            maximum = table[-1][1]

            if cclass and table_name == "cclass":
                table = copy.deepcopy(table)
                maximum += 2
                table.append((cclass, maximum))
                logger.log_err(f"table in cclass mod: {table}")

            roll = random.randint(1, maximum)
            logger.log_err(f"rolled a {roll} from 1-{maximum}")
            idx = bisect_left(table, roll, key=lambda t: t[1])
            logger.log_err(f"idx: {idx}")
            table_name = table[idx][0]

        return table_name

    def roll_droppable(self, level, *args, drop_table="generic", **kwargs):
        """
        roll a possible droppable from the drop table appropriate to the level.
        inject the character class so the roller can adjust the tables.
        """
        caller = kwargs.get("caller", None)
        cclass = None
        if caller and hasattr(caller, "cclass"):
            cclass = caller.cclass.key
        drop_table_tag = self.roll_drop_table(drop_table, cclass=cclass)

        droppable_keys = sorted([
            droppable["prototype_key"]
            for droppable in self.pm.droppables_by_level(
                level,
                *args,
                **kwargs,
                must_include=drop_table_tag
            )
        ])
        if not droppable_keys:
            logger.log_err("rolled nothing to drop")
            return None
        logger.log_err(f"droppable options: {droppable_keys}")
        droppable = spawner.flatten_prototype(
            spawner.search_prototype(
                random.choice(droppable_keys),
                require_single=True
            )[0]
        )
        return droppable

    def roll_material(self, droppable, level):
        """ roll a material appropriate for the item """
        material_rollable = {}

        if "materials" in list_flatten(droppable["attrs"]):
            materials = list(filter(lambda tup: "materials" in tup, droppable["attrs"]))[0][1]
            material_rollables = self.pm.rollables_by_level(level, materials)
            if not material_rollables:
                logger.log_err(
                    f"There are no material rollables for {droppable['prototype_key']},"
                     " fix your prototypes"
                )
                return {}
            material_rollable = random.choice(material_rollables)

        return material_rollable

    def roll_tier(self, droppable):
        """ roll a tier appropriate for the item """
        tier = 0

        if "tier" in list_flatten(droppable["attrs"]):
            tier = self.roll_drop_table("tiers")

        return tier

    def roll_affixes(self, droppable, level, tier):
        """ roll affixes appropriate for the item, level, and tier """
        affixes = []

        if tier > 1:
            affix_count = random.randint(2*(tier-1)-1,2*(tier-1))
            logger.log_err(f"rolled tier {tier}, rolling {affix_count} affixes...")
            for _ in range(affix_count):
                affix_rollables = self.pm.rollables_by_level(
                    level,
                    "affix",
                    must_include=droppable["typeclass"],
                    exclude=affixes
                )
                options = sorted([
                    rollable["prototype_key"]
                    for rollable in affix_rollables
                ])
                logger.log_err(f"possible affixes: {options}")
                if not affix_rollables:
                    logger.log_err(
                        f"Ran out of affixes for {droppable['prototype_key']},"
                         " fix your prototypes"
                    )
                    return affixes
                affix = ""
                while affix not in options:
                    affix = self.roll_drop_table("affixes")
                logger.log_err(f"rolled affix: {affix}")
                affixes.append(affix)

        return affixes

    def spawn_item(self, level, *args, drop_table="generic", **kwargs):
        """ assemble and spawn the item """
        droppable = self.roll_droppable(level, *args, drop_table=drop_table, **kwargs)
        if not droppable:
            return

        logger.log_err(f"rolled droppable: {droppable['prototype_key']}")
        material_rollable = self.roll_material(droppable, level)
        logger.log_err(f"rolled material: {material_rollable.get('prototype_key'), ''}")
        tier = self.roll_tier(droppable)
        affixes = self.roll_affixes(droppable, level, tier)

        item_level = max([
            (
                list(
                    filter(
                        lambda tup: "required_level" in tup, droppable.get("attrs", {})
                    )
                )
                or [('required_level', 1)]
            )[0][1],
            (
                list(
                    filter(
                        lambda tup: "required_level" in tup, material_rollable.get("attrs", {})
                    )
                )
                or [('required_level', 1)]
            )[0][1],
        ])

        material_prototype_tup = (material_rollable["prototype_key"],) if material_rollable else ()
        new_prot = {
            "prototype_parent": (droppable["prototype_key"],) + material_prototype_tup,
            "typeclass": droppable["typeclass"],
            "tier": tier,
            "required_level": item_level,
            "affixes": affixes,
        }

        logger.log_err(f"new_prot: {new_prot}")
        logger.log_err(f"new_prot_flattened: {spawner.flatten_prototype(new_prot)}")

        caller = kwargs.get("caller", None)
        obj = spawner.spawn(spawner.flatten_prototype(new_prot), caller=caller)[0]
        obj.location = caller.location
        obj.location.msg_contents(f"{obj.get_numbered_name(1, caller)[0]} dropped.")

# make a singleton so we benefit from the cached drop_tables and prototypes
item_spawner = ItemSpawner()
