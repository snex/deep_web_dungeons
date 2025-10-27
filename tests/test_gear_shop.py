"""
test the gear shop
"""

from unittest.mock import patch, PropertyMock

from evennia.prototypes.spawner import spawn
from evennia.utils.create import create_object

from typeclasses.npcs import ShopKeeper
from world.npcs.gear_shop import ShoppingSession
from world.quantum_lattices import DustShard, StaticBloom, EchoStone

from .mixins import AinneveTestMixin

class TestShoppingSession(AinneveTestMixin):
    """ test the shopping session class to connect a character with an npc while shopping """
    def setUp(self):
        super().setUp()
        self.shopkeeper = create_object(
            ShopKeeper,
            key="shopkeeper"
        )
        self.shopping_session = ShoppingSession(self.shopkeeper, self.char1)
        self.char1.buyable_gear = {self.shopkeeper: [self.weapon]}
        self.vendor_price_patcher = patch(
            "typeclasses.objects.EquipmentObject.vendor_price",
            new_callable=PropertyMock
        )
        self.mock_vendor_price = self.vendor_price_patcher.start()

    def tearDown(self):
        self.vendor_price_patcher.stop()
        super().tearDown()

    @patch("world.item_spawner.item_spawner.spawn_item")
    def test_buyable_gear(self, mock_item_spawner):
        """ test getting and creating buyable gear """
        self.char1.buyable_gear = {self.shopkeeper: ["b", "a"]}
        self.assertEqual(self.shopping_session.buyable_gear, ["a", "b"])
        mock_item_spawner.side_effect = [9, 8, 7, 6, 5, 5, 4, 3, 2, 1]
        self.char1.buyable_gear = {"different shopkeeper": ["b", "a"]}
        self.assertEqual(self.shopping_session.buyable_gear, [1, 2, 3, 4, 5, 5, 6, 7, 8, 9])

    def test_display_vendor_price(self):
        """ test displaying vendor price in a user friendly manner """
        self.mock_vendor_price.return_value = {
            "scrap": {"count": 4, "ql": None},
        }
        self.assertEqual(self.shopping_session.display_vendor_price(self.weapon), "four scraps")
        self.mock_vendor_price.return_value = {
            "scrap": {"count": 4, "ql": None},
            "dust shard": {"count": 2, "ql": DustShard()},
            "static bloom": {"count": 1, "ql": StaticBloom()},
            "echo stone": {"count": 20, "ql": EchoStone()},
        }
        self.assertEqual(
            self.shopping_session.display_vendor_price(self.weapon),
            "four scraps, |xtwo dust shards|n, |ca static bloom|n and |G20 echo stones|n"
        )

    def test_character_can_afford_item(self):
        """ test determination of character being able to afford an item """
        self.mock_vendor_price.return_value = {
            "scrap": {"count": 4, "ql": None},
            "dust shard": {"count": 2, "ql": DustShard()},
        }
        self.assertFalse(self.shopping_session.character_can_afford_item(self.weapon), False)
        scrap = spawn("scrap")[0]
        scrap.location = self.char1
        self.char1.equipment.move(scrap)
        self.assertFalse(self.shopping_session.character_can_afford_item(self.weapon), False)
        scrap = spawn("scrap")[0]
        scrap.location = self.char1
        self.char1.equipment.move(scrap)
        self.assertFalse(self.shopping_session.character_can_afford_item(self.weapon), False)
        scrap = spawn("scrap")[0]
        scrap.location = self.char1
        self.char1.equipment.move(scrap)
        self.assertFalse(self.shopping_session.character_can_afford_item(self.weapon), False)
        scrap = spawn("scrap")[0]
        scrap.location = self.char1
        self.char1.equipment.move(scrap)
        self.assertFalse(self.shopping_session.character_can_afford_item(self.weapon), False)
        dust = spawn("dust_shard")[0]
        dust.location = self.char1
        self.char1.equipment.move(dust)
        self.assertFalse(self.shopping_session.character_can_afford_item(self.weapon), False)
        dust = spawn("dust_shard")[0]
        dust.location = self.char1
        self.char1.equipment.move(dust)
        self.assertTrue(self.shopping_session.character_can_afford_item(self.weapon), False)

    def test_buy_item(self):
        """ test that you can buy an item """
        self.mock_vendor_price.return_value = {
            "scrap": {"count": 4, "ql": None},
            "dust shard": {"count": 2, "ql": DustShard()},
        }
        self.shopping_session.buy_item(self.weapon)
        self.assertNotEqual(self.weapon.location, self.char1)
        scraps = spawn(*(4 * ["scrap"]))
        for scrap in scraps:
            scrap.location = self.char1
            self.char1.equipment.move(scrap)
        dusts = spawn(*(2 * ["dust_shard"]))
        for dust in dusts:
            dust.location = self.char1
            self.char1.equipment.move(dust)
        self.shopping_session.buy_item(self.weapon)
        self.assertEqual(self.weapon.location, self.char1)
