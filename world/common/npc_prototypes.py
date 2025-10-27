""" NPC prototypes """

BASE_NPC = {
    "prototype_key": "base_npc",
    "typeclass": "typeclasses.npcs.NPC"
}

BASE_TALKATIVE_NPC = {
    "prototype_parent": "base_npc",
    "prototype_key": "base_talkative_npc",
    "typeclass": "typeclasses.npcs.TalkativeNPC"
}

BASE_SHOPKEEPER = {
    "prototype_parent": "base_talkative_npc",
    "prototype_key": "base_shopkeeper",
    "typeclass": "typeclasses.npcs.ShopKeeper"
}

YOUR_MOM = {
    "prototype_parent": "base_shopkeeper",
    "prototype_key": "your_mom",
    "key": "Your Mom",
    "desc": "Your Mom is pretty hot, dude.",
    "hi_text": "Welcome to Your Mom's shop. Please browse my wares!",
    "menudata": "world.npcs.your_mom"
}

RIKA_VOLKOV = {
    "prototype_parent": "base_shopkeeper",
    "prototype_key": "rika_volkov",
    "key": "Rika Volkov",
    "aliases": ["razor"],
    "desc": "A description of \"Razor\" Rika Volkov goes here.",
    "welcome_text": ["Welcome to The Razor's Edge!", "Razor's Edge only sells the best!"],
    "buy_text": ["What'll it be?", "What'cha need?", "Got all yer barb smashing needs!"],
    "sell_text": ["Whatcha got for me?", "Got anything good?", "Anything I can use in there?"],
    "sale_made_text": ["Stop by any time!", "See ya next time!", "Go crack some skulls!"],
    "no_sale_text": ["Stop wasting my time!", "Buy or get out!", "No loitering!"],
    "menudata": "world.npcs.gear_shop",
}
