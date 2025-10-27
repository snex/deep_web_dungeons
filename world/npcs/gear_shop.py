"""
Shop that sells equippable gear

Players can also sell their stuff for scrap
"""

import random

from evennia.prototypes.spawner import spawn
from evennia.utils.utils import make_iter

from typeclasses.objects import EquipmentObject
from world.item_spawner import item_spawner
from world.utils import get_numbered_name, obj_order

class ShoppingSession:
    """ handle a shopping session between a character and an npc shopkeeper """
    def __init__(self, npc, character):
        self.npc = npc
        self.character = character
        self._made_sale = False

    @property
    def buyable_gear(self):
        """ stock the shop if necessary then return the available stock """
        # TODO - roll new gear if character's level has changed
        gear = self.character.buyable_gear.get(self.npc, [])

        if not gear:
            for _ in range(10):
                item = item_spawner.spawn_item(
                    self.character.levels.level,
                    drop_table="gear_vendor",
                    tier_table="vendor_tiers",
                    caller=self.npc,
                    cclass=self.character.cclass.key,
                    location=self.npc
                )
                if item:
                    gear.append(item)
            self.character.ndb.buyable_gear[self.npc] = gear

        return sorted(gear, key=obj_order)

    def display_vendor_price(self, item):
        """ display the item price in a user friendly way """
        price = item.vendor_price
        price_l = []

        for currency, data in price.items():
            numbered_name = get_numbered_name(currency, data["count"], return_string=True)
            colored_name = (
                data["ql"].get_display_name(numbered_name) if data["ql"] else
                numbered_name
            )
            price_l.append(colored_name)

        if len(price_l) == 1:
            return price_l[0]

        return ", ".join(price_l[:-1]) + " and " + price_l[-1]

    def character_can_afford_item(self, item):
        """ whether or not character can afford the item """
        price = item.vendor_price

        for currency, data in price.items():
            inv = self.character.search(currency, location=self.character, quiet=True)
            if len(inv) < data["count"]:
                return False

        return True

    def buy_item(self, item):
        """ perform the buy """
        price = item.vendor_price

        if not self.character_can_afford_item(item):
            return

        for currency, data in price.items():
            inv = self.character.search(currency, location=self.character, quiet=True)
            for i in range(data["count"]):
                inv[i].delete()

        item.location = self.character
        item.save()
        self.character.buyable_gear[self.npc].remove(item)
        self.character.equipment.add(item)

    def _say(self, dialog):
        return f"{self.npc} says: {dialog}"

    def welcome_text(self):
        """ npc says this when starting the menu """
        return self._say(random.choice(make_iter(self.npc.attributes.get("welcome_text"))))

    def buy_text(self):
        """ npc says this when entering the buy menu """
        return self._say(f"""{random.choice(make_iter(self.npc.attributes.get("buy_text")))}

|g✔|n - You can afford this.
|r✘|n - You cannot afford this."""
        )

    def sell_text(self):
        """ npc says this when entering the sell menu """
        return self._say(random.choice(make_iter(self.npc.attributes.get("sell_text"))))

    def sale_made_text(self):
        """ npc says this when character leaves shop and sale was made """
        return self._say(random.choice(make_iter(self.npc.attributes.get("sale_made_text"))))

    def no_sale_text(self):
        """ npc says this when character leaves shop and no sale was made """
        return self._say(random.choice(make_iter(self.npc.attributes.get("no_sale_text"))))

    @property
    def made_sale(self):
        """ whether or not a sale was made this session """
        return self._made_sale

    @made_sale.setter
    def made_sale(self, value):
        self._made_sale = value

def node_start(caller, raw_string, **kwargs):
    """ base of the shop menu """
    shopping_session = kwargs.get("shopping_session", None)

    if not shopping_session:
        shopping_session = ShoppingSession(caller.ndb._evmenu.npc, caller)

    text = shopping_session.welcome_text()
    options = [
        {
            "desc": "Buy",
            "goto": ("node_show_buyable_items", {"shopping_session": shopping_session, **kwargs}),
        },
        {
            "desc": "Sell",
            "goto": ("node_show_sellable_items", {"shopping_session": shopping_session, **kwargs}),
        },
        {"desc": "Leave", "goto": ("node_end", {"shopping_session": shopping_session, **kwargs})},
    ]

    return (text, ""), options

def node_end(_caller, raw_string, **kwargs):
    """ close the shop menu """
    shopping_session = kwargs["shopping_session"]

    if shopping_session.made_sale:
        return shopping_session.sale_made_text()

    return shopping_session.no_sale_text()

def node_buy_item(caller, raw_string, **kwargs):
    """ buy the item """
    shopping_session = kwargs["shopping_session"]
    shopping_session.made_sale = True
    item = kwargs.pop("item")
    shopping_session.buy_item(item)
    caller.msg(f"You bought {item} for {shopping_session.display_vendor_price(item)}")

    return node_show_buyable_items(caller, "", **kwargs)

def node_ask_buy_item(caller, raw_string, **kwargs):
    """ confirm the user wants to buy an item """
    shopping_session = kwargs["shopping_session"]
    item = kwargs.pop("item")

    text = f"""{item.return_appearance(shopping_session.character)}"
Buy {item} for {shopping_session.display_vendor_price(item)}?"""


    if shopping_session.character_can_afford_item(item):
        options = [
            {"desc": "Yes, buy it.", "goto": ("node_buy_item", {"item": item, **kwargs})},
            {
                "desc": "No, look for something else to buy.",
                "goto": ("node_show_buyable_items", kwargs),
            },
            {"desc": "No, go back to the main menu.", "goto": ("node_start", kwargs)},
        ]

        return (text, ""), options

    caller.msg(f"""{item.return_appearance(shopping_session.character)}

Item price: {shopping_session.display_vendor_price(item)}
You can't afford it.""")

    return node_show_buyable_items(caller, "", **kwargs)

def node_show_buyable_items(_caller, raw_string, **kwargs):
    """ show items the shopkeeper is selling """
    shopping_session = kwargs["shopping_session"]
    text = shopping_session.buy_text()
    options = []
    for item in shopping_session.buyable_gear:
        afford = "[|g✔|n]" if shopping_session.character_can_afford_item(item) else "[|r✘|n]"
        options.append({
            "desc": f"{afford} {item}", "goto": ("node_ask_buy_item", {"item": item, **kwargs})
        })

    options += [
        {"desc": "Cancel", "goto": ("node_start", kwargs)},
    ]

    return (text, ""), options

def node_sell_item(caller, raw_string, **kwargs):
    """ sell the item """
    shopping_session = kwargs["shopping_session"]
    shopping_session.made_sale = True
    item = kwargs.pop("item")
    scraps = spawn(*item.scrap_value * ["scrap"])
    for scrap in scraps:
        scrap.location = caller
        caller.equipment.move(scrap)
    item.delete()

    return node_show_sellable_items(caller, "", **kwargs)

def node_sell_all(caller, raw_string, **kwargs):
    """ sell everything """
    shopping_session = kwargs["shopping_session"]
    shopping_session.made_sale = True
    gear = caller.equipment.sorted_backpack(EquipmentObject)
    scrap_value = 0

    for item in gear:
        scrap_value += item.scrap_value
        item.delete()

    scraps = spawn(*scrap_value * ["scrap"])
    for scrap in scraps:
        scrap.location = caller
        caller.equipment.move(scrap)

    return node_start(caller, "", **kwargs)

def node_ask_sell_item(caller, raw_string, **kwargs):
    """ confirm the user wants to sell an item """
    item = kwargs.pop("item")
    text = f"Sell {item} for {item.scrap_value} scrap?"
    options = [
        {"desc": "Yes, sell it.", "goto": ("node_sell_item", {"item": item, **kwargs})},
        {
            "desc": "No, look for something else to sell.",
            "goto": ("node_show_sellable_items", kwargs),
        },
        {"desc": "No, go back to the main menu.", "goto": ("node_start", kwargs)},
    ]

    return (text, ""), options

def node_ask_sell_all(caller, raw_string, **kwargs):
    """ confirm the user wants to sell everything """
    gear = caller.equipment.sorted_backpack(EquipmentObject)
    scrap_value = sum(
        item.scrap_value
        for item in gear
    )
    text = (
        f"Are you |w|iabsolutely sure|I|n you want to sell everything in your backpack for"
        f" {scrap_value} scrap?"
    )
    options = [
        {"desc": "Yes, I'm sure. Sell it.", "goto": ("node_sell_all", kwargs)},
        {
            "desc": "No, look for something else to sell.",
            "goto": ("node_show_sellable_items", kwargs),
        },
        {"desc": "No, go back to the main menu.", "goto": ("node_start", kwargs)},
    ]

    return (text, ""), options

def node_show_sellable_items(caller, raw_string, **kwargs):
    """ show items the player can sell to the shopkeeper """
    shopping_session = kwargs["shopping_session"]
    text = shopping_session.sell_text()
    gear = caller.equipment.sorted_backpack(EquipmentObject)

    if not gear:
        caller.msg("You have nothing to sell.")
        return node_start(caller, "", **kwargs)

    options = []
    for item in gear:
        options.append(
            {"desc": str(item), "goto": ("node_ask_sell_item", {"item": item, **kwargs})}
        )
    options += [
        {"desc": "Sell it all!", "goto": ("node_ask_sell_all", kwargs)},
        {"desc": "Cancel", "goto": ("node_start", kwargs)},
    ]

    return (text, ""), options
