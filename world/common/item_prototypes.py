""" Item prototypes """

from world.enums import(
    Ability,
    CombatRange,
    DefenseType,
    PhysicalObjectMaterial,
    QuantumLatticeType,
    TechArmorMaterial,
    TechHelmetMaterial,
    TechWeaponMaterial,
    WieldLocation
)
from world.utils import rainbow

BASE_QUANTUM_LATTICE = {
    "prototype_key": "base_quantum_lattice",
    "typeclass": "typeclasses.objects.QuantumLatticeObject",
}

QL_DUST_SHARD = {
    "prototype_parent": "base_quantum_lattice",
    "prototype_key": "dust_shard",
    "key": "dust shard",
    "ql_type": QuantumLatticeType.DUST_SHARD,
    "desc": "|xDust |xshards|n can be used on a tier 2+ item to reroll a random affix. Combine 3"
            " |xdust shards|n into a |cstatic |cbloom|n."
}

QL_STATIC_BLOOM = {
    "prototype_parent": "base_quantum_lattice",
    "prototype_key": "static_bloom",
    "key": "static bloom",
    "ql_type": QuantumLatticeType.STATIC_BLOOM,
    "desc": "|cStatic |cblooms|n can be used on a tier 2+ item to remove a random affix. Combine 3"
            " |cstatic |cblooms|n into an |Gecho |Gstone|n."
}

QL_ECHO_STONE = {
    "prototype_parent": "base_quantum_lattice",
    "prototype_key": "echo_stone",
    "key": "echo stone",
    "ql_type": QuantumLatticeType.ECHO_STONE,
    "desc": "|GEcho |Gstones|n can be used on a tier 2+ item to add a random affix. Combine 3"
            " |Gecho |Gstones|n into a |yresonance |ycrystal|n."
}

QL_RESONANCE_CRYSTAL = {
    "prototype_parent": "base_quantum_lattice",
    "prototype_key": "resonance_crystal",
    "key": "resonance crystal",
    "ql_type": QuantumLatticeType.RESONANCE_CRYSTAL,
    "desc": "|yResonance |ycrystals|n can be used on a tier 1 item to convert it into a tier 2 item"
            " with no affixes. Combine 3 |yresonance |ycrystals|n into a |[x|Xsingularity"
            " |[x|Xshard|n."
}

QL_SINGULARITY_SHARD = {
    "prototype_parent": "base_quantum_lattice",
    "prototype_key": "singularity_shard",
    "key": "singularity shard",
    "ql_type": QuantumLatticeType.SINGULARITY_SHARD,
    "desc": "|[x|XSingularity |[x|Xshards|n can be used on a tier 2+ item to lower its tier by 1."
            " Random affixes beyond what the new lower tier allows will be removed. Combine 3"
            " |[x|Xsingularity |[x|Xshards|n into a |530phase |530pearl|n."
}

QL_PHASE_PEARL = {
    "prototype_parent": "base_quantum_lattice",
    "prototype_key": "phase_pearl",
    "key": "phase pearl",
    "ql_type": QuantumLatticeType.PHASE_PEARL,
    "desc": "|530Phase |530pearls|n can be used on a tier 2 item to convert it into a tier 3 item."
            " Combine 3 |530phase |530pearls|n into a |Mvoid |Mspark|n."
}

QL_VOID_SPARK = {
    "prototype_parent": "base_quantum_lattice",
    "prototype_key": "void_spark",
    "key": "void spark",
    "ql_type": QuantumLatticeType.VOID_SPARK,
    "desc": "|MVoid |Msparks|n can be used on a tier 2+ item to wipe all of its affixes. Combine 3"
            f" |Mvoid |Msparks|n into a {rainbow('chromatic heart')}."
}

QL_CHROMATIC_HEART = {
    "prototype_parent": "base_quantum_lattice",
    "prototype_key": "chromatic_heart",
    "key": "chromatic heart",
    "ql_type": QuantumLatticeType.CHROMATIC_HEART,
    "desc": f"{rainbow('Chromatic hearts')} can be used on a tier 3 item to convert it into a tier"
            f" 4 item. Combine 3 {rainbow('chromatic hearts')} into a |[w|xnexus |[w|xdiamond|n."
}

QL_NEXUS_DIAMOND = {
    "prototype_parent": "base_quantum_lattice",
    "prototype_key": "nexus_diamond",
    "key": "nexus diamond",
    "display_name": "|[w|xnexus |[w|xdiamond|n",
    "ql_type": QuantumLatticeType.NEXUS_DIAMOND,
    "desc": "|[w|xNexus |[w|xdiamonds|n can be used on any item to convert it into a tier 4 item."
}

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
