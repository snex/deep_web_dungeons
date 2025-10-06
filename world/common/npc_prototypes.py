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
