"""
Helpers for testing evadventure modules.

"""

from evennia.utils import create
from evennia.utils.test_resources import EvenniaTest

from typeclasses.objects import (
    ArmorObject,
    Helmet,
    Object,
    Shield,
    WeaponObject,
)
from world.enums import WieldLocation


class AinneveTestMixin(EvenniaTest):
    """
    Provides a set of pre-made characters.

    """

    def setUp(self):
        super().setUp()
        # remove default dev permissions from first test account so test chars have equivalent perms
        self.account.permissions.remove('Developer')

        self.helmet = create.create_object(
            Helmet,
            key="helmet",
            attributes=[("inventory_use_slot", WieldLocation.HEAD)]
        )
        self.shield = create.create_object(
            Shield,
            key="shield",
            attributes=[("inventory_use_slot", WieldLocation.SHIELD_HAND)]
        )
        self.armor = create.create_object(
            ArmorObject,
            key="armor",
            attributes=[("inventory_use_slot", WieldLocation.BODY)]
        )
        self.weapon = create.create_object(
            WeaponObject,
            key="weapon",
            attributes=[("inventory_use_slot", WieldLocation.WEAPON_HAND)]
        )
        self.big_weapon = create.create_object(
            WeaponObject,
            key="big_weapon",
            attributes=[("inventory_use_slot", WieldLocation.TWO_HANDS)],
        )
        self.item = create.create_object(
            Object,
            key="backpack item",
        )
        self.item2 = create.create_object(
            Object,
            key="backpack item 2",
            attributes=[("size", 5)]
        )
