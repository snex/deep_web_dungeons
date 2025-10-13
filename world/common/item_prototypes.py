""" Item prototypes """

from world.enums import(
    Ability,
    CombatRange,
    DefenseType,
    PhysicalObjectMaterial,
    TechArmorMaterial,
    TechHelmetMaterial,
    TechWeaponMaterial,
    WieldLocation
)

BASE_WEAPON = {
    "prototype_key": "base_weapon",
    "typeclass": "typeclasses.objects.WeaponObject",
    "inventory_use_slot": WieldLocation.WEAPON_HAND,
    "quality": 3,
    "tier": 1,
}

BASE_WEAPON_NON_LETHAL = {
    "prototype_key": "base_weapon_non_lethal",
    "prototype_parent": "base_weapon",
    "inventory_use_slot": WieldLocation.WEAPON_HAND,
    "quality": 3,
}

BASE_WEAPON_PHYSICAL = {
    "prototype_key": "base_weapon_physical",
    "prototype_parent": "base_weapon",
    "material": PhysicalObjectMaterial.PLASTEEL
}

BASE_WEAPON_TECH = {
    "prototype_key": "base_weapon_tech",
    "prototype_parent": "base_weapon",
    "inventory_use_slot": WieldLocation.TWO_HANDS,
    "material": TechWeaponMaterial.QUARTZ_CORE
}

BASE_WEAPON_MELEE = {
    "prototype_parent": "base_weapon",
    "prototype_key": "base_weapon_melee",
    "attack_range": CombatRange.MELEE,
    "defense_type": DefenseType.ARMOR,
}

BASE_WEAPON_REACH = {
    "prototype_parent": "base_weapon",
    "prototype_key": "base_weapon_reach",
    "attack_range": CombatRange.REACH,
    "defense_type": DefenseType.ARMOR,
}

BASE_WEAPON_SHORT_RANGE = {
    "prototype_parent": "base_weapon",
    "prototype_key": "base_weapon_short_range",
    "attack_range": CombatRange.SHORT_RANGE,
    "defense_type": DefenseType.ARMOR,
}

BASE_WEAPON_MEDIUM_RANGE = {
    "prototype_parent": "base_weapon",
    "prototype_key": "base_weapon_medium_range",
    "attack_range": CombatRange.MEDIUM_RANGE,
    "defense_type": DefenseType.ARMOR,
}

BASE_WEAPON_LONG_RANGE = {
    "prototype_parent": "base_weapon",
    "prototype_key": "base_weapon_long_range",
    "attack_range": CombatRange.LONG_RANGE,
    "defense_type": DefenseType.ARMOR,
}

WEAPON_BIKE_LOCK = {
    "prototype_parent": ("base_weapon_melee", "base_weapon_physical"),
    "prototype_key": "weapon_bike_lock",
    "key": "bike lock",
    "attack_type": Ability.STR,
    "damage_roll": "1d6",
    # use "permissions" here
    # "allowed_classes": ["antifa_rioter"],
    "desc": "A lock attached to a chain designed to keep a bicycle secure."
}

WEAPON_BALISONG = {
    "prototype_parent": ("base_weapon_melee", "base_weapon_physical"),
    "prototype_key": "weapon_balisong",
    "key": "balisong",
    "attack_type": Ability.CUN,
    "damage_roll": "1d4",
    "desc": "A balisong, also known as a butterfly knife."
}

WEAPON_LAPTOP = {
    "prototype_parent": ("base_weapon_short_range", "base_weapon_tech"),
    "prototype_key": "weapon_laptop",
    "key": "laptop",
    "attack_type": Ability.WIL,
    "defense_type": Ability.WIL,
    "damage_roll": "2d4",
    "desc": "A cheap laptop."
}

WEAPON_DILDORANG = {
    "prototype_parent": ("base_weapon_medium_range", "base_weapon_physical"),
    "prototype_key": "weapon_dildorang",
    "key": "dildorang",
    "attack_type": Ability.CUN,
    "defense_type": DefenseType.ARMOR,
    "damage_roll": "2d4",
    "desc": "A dildo perfectly curved so that it returns to the owner when thrown."
}

BASE_ARMOR = {
    "prototype_key": "base_armor",
    "typeclass": "typeclasses.objects.ArmorObject",
    "inventory_use_slot": WieldLocation.BODY,
    "quality": 3,
    "tier": 1,
}

BASE_ARMOR_PHYSICAL = {
    "prototype_key": "base_armor_physical",
    "prototype_parent": "base_armor",
    "material": PhysicalObjectMaterial.PLASTEEL
}

BASE_ARMOR_TECH = {
    "prototype_key": "base_armor_tech",
    "prototype_parent": "base_armor",
    "material": TechArmorMaterial.DUST_WEAVE_CANVAS
}

ARMOR_CHEST_PLATE = {
    "prototype_parent": "base_armor_physical",
    "prototype_key": "armor_chest_plate",
    "key": "chest plate",
    "armor": 1,
    "desc": "Basic chest plate that gives a minimal amount of protection in combat.",
}

ARMOR_TRENCH = {
    "prototype_parent": "base_armor_tech",
    "prototype_key": "armor_trench",
    "key": "trench",
    "max_system_load": 3,
    "desc": "A basic full length trench coat."
}

BASE_SHIELD = {
    "prototype_key": "base_shield",
    "typeclass": "typeclasses.objects.Shield",
    "inventory_use_slot": WieldLocation.SHIELD_HAND,
    "quality": 3,
    "material": PhysicalObjectMaterial.PLASTEEL,
    "tier": 1,
}

SHIELD_GARBAGE_LID = {
    "prototype_parent": "base_shield",
    "prototype_key": "shield_garbage_lid",
    "key": "garbage lid",
    "block": 20.0,
    "desc": "The lid from a garbage can."
}

BASE_HELMET = {
    "prototype_key": "base_helmet",
    "typeclass": "typeclasses.objects.Helmet",
    "inventory_use_slot": WieldLocation.HEAD,
    "quality": 3,
    "tier": 1,
}

BASE_HELMET_PHYSICAL = {
    "prototype_key": "base_helmet_physical",
    "prototype_parent": "base_helmet",
    "material": PhysicalObjectMaterial.PLASTEEL
}

BASE_HELMET_TECH = {
    "prototype_key": "base_helmet_tech",
    "prototype_parent": "base_helmet",
    "material": TechHelmetMaterial.TINTED_POLYMER
}

HELMET_HOCKEY_MASK = {
    "prototype_parent": "base_helmet_physical",
    "prototype_key": "hockey_mask",
    "key": "hockey mask",
    "desc": "Hockey masks are good for a slight amount of defense and scaring kids at summer camp."
}

HELMET_SPECS = {
    "prototype_parent": "base_helmet_tech",
    "prototype_key": "specs",
    "key": "specs",
    "display_name": "pair of specs",
    "desc": "A pair of specs worn over the eyes."
}

HELMET_GIMP_MASK = {
    "prototype_parent": "base_helmet_physical",
    "prototype_key": "gimp_mask",
    "key": "gimp mask",
    "desc": "A gimp mask is useless for defense but also not good for much else."
}

BASE_CONSUMABLE = {
    "prototype_key": "base_consumable",
    "typeclass": "typeclasses.objects.ConsumableObject",
    "inventory_use_slot": WieldLocation.BACKPACK
}

BASE_HEALING_CONSUMABLE = {
    "prototype_parent": "base_consumable",
    "prototype_key": "base_healing_consumable",
    "typeclass": "typeclasses.objects.ConsumableHealingObject"
}

RATION = {
    "prototype_parent": "base_healing_consumable",
    "prototype_key": "ration",
    "key": "ration",
    "desc": "A grey protein block covered in pale-green nutrient paste.",
    "uses": 1,
    "heal_value": 3,
    "consume_method": "eat"
}
