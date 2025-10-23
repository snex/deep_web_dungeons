""" Item prototypes """

from world.characters.classes import CHARACTER_CLASSES
from world.enums import(
    Ability,
    CombatRange,
    DefenseType,
    EvasiveObjectMaterial,
    NonLethalWeaponMaterial,
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
    "prototype_tags": ["droppable", "quantum_lattice", "dust_shard"],
    "key": "dust shard",
    "ql_type": QuantumLatticeType.DUST_SHARD,
    "desc": "|xDust |xshards|n can be used on a tier 2+ item to reroll a random affix. Combine 3"
            " |xdust shards|n into a |cstatic |cbloom|n."
}

QL_STATIC_BLOOM = {
    "prototype_parent": "base_quantum_lattice",
    "prototype_key": "static_bloom",
    "prototype_tags": ["droppable", "quantum_lattice", "static_bloom"],
    "key": "static bloom",
    "ql_type": QuantumLatticeType.STATIC_BLOOM,
    "desc": "|cStatic |cblooms|n can be used on a tier 2+ item to remove a random affix. Combine 3"
            " |cstatic |cblooms|n into an |Gecho |Gstone|n."
}

QL_ECHO_STONE = {
    "prototype_parent": "base_quantum_lattice",
    "prototype_key": "echo_stone",
    "prototype_tags": ["droppable", "quantum_lattice", "echo_stone"],
    "key": "echo stone",
    "ql_type": QuantumLatticeType.ECHO_STONE,
    "desc": "|GEcho |Gstones|n can be used on a tier 2+ item to add a random affix. Combine 3"
            " |Gecho |Gstones|n into a |yresonance |ycrystal|n."
}

QL_RESONANCE_CRYSTAL = {
    "prototype_parent": "base_quantum_lattice",
    "prototype_key": "resonance_crystal",
    "prototype_tags": ["droppable", "quantum_lattice", "resonance_crystal"],
    "key": "resonance crystal",
    "ql_type": QuantumLatticeType.RESONANCE_CRYSTAL,
    "desc": "|yResonance |ycrystals|n can be used on a tier 1 item to convert it into a tier 2 item"
            " with no affixes. Combine 3 |yresonance |ycrystals|n into a |[x|Xsingularity"
            " |[x|Xshard|n."
}

QL_SINGULARITY_SHARD = {
    "prototype_parent": "base_quantum_lattice",
    "prototype_key": "singularity_shard",
    "prototype_tags": ["droppable", "quantum_lattice", "singularity_shard"],
    "key": "singularity shard",
    "ql_type": QuantumLatticeType.SINGULARITY_SHARD,
    "desc": "|[x|XSingularity |[x|Xshards|n can be used on a tier 2+ item to lower its tier by 1."
            " Random affixes beyond what the new lower tier allows will be removed. Combine 3"
            " |[x|Xsingularity |[x|Xshards|n into a |530phase |530pearl|n."
}

QL_PHASE_PEARL = {
    "prototype_parent": "base_quantum_lattice",
    "prototype_key": "phase_pearl",
    "prototype_tags": ["droppable", "quantum_lattice", "phase_pearl"],
    "key": "phase pearl",
    "ql_type": QuantumLatticeType.PHASE_PEARL,
    "desc": "|530Phase |530pearls|n can be used on a tier 2 item to convert it into a tier 3 item."
            " Combine 3 |530phase |530pearls|n into a |Mvoid |Mspark|n."
}

QL_VOID_SPARK = {
    "prototype_parent": "base_quantum_lattice",
    "prototype_key": "void_spark",
    "prototype_tags": ["droppable", "quantum_lattice", "void_spark"],
    "key": "void spark",
    "ql_type": QuantumLatticeType.VOID_SPARK,
    "desc": "|MVoid |Msparks|n can be used on a tier 2+ item to wipe all of its affixes. Combine 3"
            f" |Mvoid |Msparks|n into a {rainbow('chromatic heart')}."
}

QL_CHROMATIC_HEART = {
    "prototype_parent": "base_quantum_lattice",
    "prototype_key": "chromatic_heart",
    "prototype_tags": ["droppable", "quantum_lattice", "chromatic_heart"],
    "key": "chromatic heart",
    "ql_type": QuantumLatticeType.CHROMATIC_HEART,
    "desc": f"{rainbow('Chromatic hearts')} can be used on a tier 3 item to convert it into a tier"
            f" 4 item. Combine 3 {rainbow('chromatic hearts')} into a |[w|xnexus |[w|xdiamond|n."
}

QL_NEXUS_DIAMOND = {
    "prototype_parent": "base_quantum_lattice",
    "prototype_key": "nexus_diamond",
    "prototype_tags": ["droppable", "quantum_lattice", "nexus_diamond"],
    "key": "nexus diamond",
    "display_name": "|[w|xnexus |[w|xdiamond|n",
    "ql_type": QuantumLatticeType.NEXUS_DIAMOND,
    "desc": "|[w|xNexus |[w|xdiamonds|n can be used on any item to convert it into a tier 4 item."
}

MATERIAL_PHYSICAL = {
    "prototype_key": "material_physical",
    "materials": "physical",
}

MATERIAL_PHYSICAL_PLASTEEL = {
    "prototype_parent": "material_physical",
    "prototype_key": "material_physical_plasteel",
    "prototype_tags": ["rollable", "physical"],
    "material": PhysicalObjectMaterial.PLASTEEL,
    "required_level": 1,
}

MATERIAL_PHYSICAL_CHITIN = {
    "prototype_parent": "material_physical",
    "prototype_key": "material_physical_chitin",
    "prototype_tags": ["rollable", "physical"],
    "material": PhysicalObjectMaterial.CHITIN,
    "required_level": 10,
}

MATERIAL_PHYSICAL_STEEL = {
    "prototype_parent": "material_physical",
    "prototype_key": "material_physical_steel",
    "prototype_tags": ["rollable", "physical"],
    "material": PhysicalObjectMaterial.STEEL,
    "required_level": 20,
}

MATERIAL_PHYSICAL_CARBON_FIBER = {
    "prototype_parent": "material_physical",
    "prototype_key": "material_physical_carbon_fiber",
    "prototype_tags": ["rollable", "physical"],
    "material": PhysicalObjectMaterial.CARBON_FIBER,
    "required_level": 30,
}

MATERIAL_TECH_WEAPON = {
    "prototype_key": "material_tech_weapon",
    "materials": "tech_weapon",
}

MATERIAL_TECH_WEAPON_QUARTZ_CORE = {
    "prototype_parent": "material_tech_weapon",
    "prototype_key": "material_tech_weapon_quartz_core",
    "prototype_tags": ["rollable", "tech_weapon"],
    "material": TechWeaponMaterial.QUARTZ_CORE,
    "required_level": 1,
}

MATERIAL_TECH_WEAPON_SILICON_SHARD = {
    "prototype_parent": "material_tech_weapon",
    "prototype_key": "tech_weapon_silicon_shard",
    "prototype_tags": ["rollable", "tech_weapon"],
    "material": TechWeaponMaterial.SILICON_SHARD,
    "required_level": 10,
}

MATERIAL_TECH_WEAPON_BIO_SYNAPSE = {
    "prototype_parent": "material_tech_weapon",
    "prototype_key": "tech_weapon_bio_synapse",
    "prototype_tags": ["rollable", "tech_weapon"],
    "material": TechWeaponMaterial.BIO_SYNAPSE,
    "required_level": 20,
}

MATERIAL_TECH_WEAPON_FERRO_LOGIC = {
    "prototype_parent": "material_tech_weapon",
    "prototype_key": "tech_weapon_ferro_logic",
    "prototype_tags": ["rollable", "tech_weapon"],
    "material": TechWeaponMaterial.FERRO_LOGIC,
    "required_level": 30,
}

MATERIAL_TECH_ARMOR = {
    "prototype_key": "material_tech_armor",
    "materials": "tech_armor",
}

MATERIAL_TECH_ARMOR_DUST_WEAVE_CANVAS = {
    "prototype_parent": "material_tech_armor",
    "prototype_key": "material_tech_armor_dust_weave_canvas",
    "prototype_tags": ["rollable", "tech_armor"],
    "material": TechArmorMaterial.DUST_WEAVE_CANVAS,
    "required_level": 1,
}

MATERIAL_TECH_ARMOR_BIO_LUMINESCENT_MOSS_LINED = {
    "prototype_parent": "material_tech_armor",
    "prototype_key": "material_tech_armor_bio_luminescent_moss_lined",
    "prototype_tags": ["rollable", "tech_armor"],
    "material": TechArmorMaterial.BIO_LUMINESCENT_MOSS_LINED,
    "required_level": 10,
}

MATERIAL_TECH_ARMOR_RECYCLED_DATA_RIBBON = {
    "prototype_parent": "material_tech_armor",
    "prototype_key": "material_tech_armor_recycled_data_ribbon",
    "prototype_tags": ["rollable", "tech_armor"],
    "material": TechArmorMaterial.RECYCLED_DATA_RIBBON,
    "required_level": 20,
}

MATERIAL_TECH_ARMOR_NANOFIBER = {
    "prototype_parent": "material_tech_armor",
    "prototype_key": "material_tech_armor_nanofiber",
    "prototype_tags": ["rollable", "tech_armor"],
    "material": TechArmorMaterial.NANOFIBER,
    "required_level": 30,
}

MATERIAL_TECH_HELMET = {
    "prototype_key": "material_tech_helmet",
    "materials": "tech_helmet",
}

MATERIAL_TECH_HELMET_TINTED_POLYMER = {
    "prototype_parent": "material_tech_helmet",
    "prototype_key": "material_tech_helmet_tinted_polymer",
    "prototype_tags": ["rollable", "tech_helmet"],
    "material": TechHelmetMaterial.TINTED_POLYMER,
    "required_level": 1,
}

MATERIAL_TECH_HELMET_STATIC_FILTERING = {
    "prototype_parent": "material_tech_helmet",
    "prototype_key": "material_tech_helmet_static_filtering",
    "prototype_tags": ["rollable", "tech_helmet"],
    "material": TechHelmetMaterial.STATIC_FILTERING,
    "required_level": 10,
}

MATERIAL_TECH_HELMET_CHROMA_LAYERED = {
    "prototype_parent": "material_tech_helmet",
    "prototype_key": "material_tech_helmet_chroma_layered",
    "prototype_tags": ["rollable", "tech_helmet"],
    "material": TechHelmetMaterial.CHROMA_LAYERED,
    "required_level": 20,
}

MATERIAL_TECH_HELMET_GHOST_WEAVE = {
    "prototype_parent": "material_tech_helmet",
    "prototype_key": "material_tech_helmet_ghost_weave",
    "prototype_tags": ["rollable", "tech_helmet"],
    "material": TechHelmetMaterial.GHOST_WEAVE,
    "required_level": 30,
}

MATERIAL_EVASIVE = {
    "prototype_key": "material_evasive",
    "materials": "evasive",
}

MATERIAL_EVASIVE_WOVEN_SYNTH_FIBER = {
    "prototype_parent": "material_evasive",
    "prototype_key": "material_evasive_woven_synth_fiber",
    "prototype_tags": ["rollable", "evasive"],
    "material": EvasiveObjectMaterial.WOVEN_SYNTH_FIBER,
    "required_level": 1,
}

MATERIAL_EVASIVE_KTHARR_SHELL = {
    "prototype_parent": "material_evasive",
    "prototype_key": "material_evasive_ktharr_shell",
    "prototype_tags": ["rollable", "evasive"],
    "material": EvasiveObjectMaterial.KTHARR_SHELL,
    "required_level": 10,
}

MATERIAL_EVASIVE_BIO_LUMINESCENT_SCALE = {
    "prototype_parent": "material_evasive",
    "prototype_key": "material_evasive_bio_luminescent_scale",
    "prototype_tags": ["rollable", "evasive"],
    "material": EvasiveObjectMaterial.BIO_LUMINESCENT_SCALE,
    "required_level": 20,
}

MATERIAL_EVASIVE_BIO_PHASE_SILK = {
    "prototype_parent": "material_evasive",
    "prototype_key": "material_evasive_phase_silk",
    "prototype_tags": ["rollable", "evasive"],
    "material": EvasiveObjectMaterial.PHASE_SILK,
    "required_level": 30,
}

MATERIAL_NON_LETHAL = {
    "prototype_key": "material_non_lethal",
    "materials": "non_lethal",
}

MATERIAL_NON_LETHAL_STATIC_NUDGE = {
    "prototype_parent": "material_non_lethal",
    "prototype_key": "material_non_lethal_static_nudge",
    "prototype_tags": ["rollable", "non_lethal"],
    "material": NonLethalWeaponMaterial.STATIC_NUDGE,
    "required_level": 1,
}

MATERIAL_NON_LETHAL_SLEEP_SPORE = {
    "prototype_parent": "material_non_lethal",
    "prototype_key": "material_non_lethal_sleep_spore",
    "prototype_tags": ["rollable", "non_lethal"],
    "material": NonLethalWeaponMaterial.SLEEP_SPORE,
    "required_level": 10,
}

MATERIAL_NON_LETHAL_SONIC_HUM = {
    "prototype_parent": "material_non_lethal",
    "prototype_key": "material_non_lethal_sonic_hum",
    "prototype_tags": ["rollable", "non_lethal"],
    "material": NonLethalWeaponMaterial.SONIC_HUM,
    "required_level": 20,
}

MATERIAL_NON_LETHAL_STICKY_WEB = {
    "prototype_parent": "material_non_lethal",
    "prototype_key": "material_non_lethal_sticky_web",
    "prototype_tags": ["rollable", "non_lethal"],
    "material": NonLethalWeaponMaterial.STICKY_WEB,
    "required_level": 30,
}

# tags for PREFIX and SUFFIX should include the typeclasses they can be applied to as well as
# any other prefix or suffix prototype_keys they are not allowed to be combined with.

PREFIX_ACIDIC = {
    "prototype_key": "prefix_acidic",
    "prototype_tags": [
        "rollable",
        "affix",
        "typeclasses.objects.WeaponObject",
        "prefix_caustic",
        "prefix_corrosive"
    ],
}

PREFIX_ATOMIC = {
    "prototype_key": "prefix_atomic",
    "prototype_tags": [
        "rollable",
        "affix",
        "typeclasses.objects.WeaponObject",
        "prefix_nucular",
        "prefix_radioactive"
    ],
}

PREFIX_BASED = {
    "prototype_key": "prefix_based",
    "prototype_tags": [
        "rollable",
        "affix",
        "typeclasses.objects.ArmorObject",
        "typeclasses.objects.Helmet",
        "typeclasses.objects.Shield",
        "typeclasses.objects.WeaponObject",
        "prefix_cringe"
    ],
}

PREFIX_CAUSTIC = {
    "prototype_key": "prefix_caustic",
    "prototype_tags": [
        "rollable",
        "affix",
        "typeclasses.objects.WeaponObject",
        "prefix_acidic",
        "prefix_corrosive"
    ],
}

PREFIX_CORROSIVE = {
    "prototype_key": "prefix_corrosive",
    "prototype_tags": [
        "rollable",
        "affix",
        "typeclasses.objects.WeaponObject",
        "prefix_acidic",
        "prefix_caustic"
    ],
}

PREFIX_CRINGE = {
    "prototype_key": "prefix_cringe",
    "prototype_tags": [
        "rollable",
        "affix",
        "typeclasses.objects.ArmorObject",
        "typeclasses.objects.Helmet",
        "typeclasses.objects.Shield",
        "typeclasses.objects.WeaponObject",
        "prefix_based"
    ],
}

PREFIX_INDUCTIVE = {
    "prototype_key": "prefix_inductive",
    "prototype_tags": [
        "rollable",
        "affix",
        "typeclasses.objects.WeaponObject",
        "prefix_overclocked",
        "prefix_shocking"
    ],
}

PREFIX_MALIGNANT = {
    "prototype_key": "prefix_malignant",
    "prototype_tags": [
        "rollable",
        "affix",
        "typeclasses.objects.WeaponObject",
        "prefix_noxious",
        "prefix_toxic"
    ],
}

PREFIX_NOXIOUS = {
    "prototype_key": "prefix_noxious",
    "prototype_tags": [
        "rollable",
        "affix",
        "typeclasses.objects.WeaponObject",
        "prefix_malignant",
        "prefix_toxic"
    ],
}

PREFIX_NUCULAR = {
    "prototype_key": "prefix_nucular",
    "prototype_tags": [
        "rollable",
        "affix",
        "typeclasses.objects.WeaponObject",
        "prefix_atomic",
        "prefix_radioactive"
    ],
}

PREFIX_RADIOACTIVE = {
    "prototype_key": "prefix_radioactive",
    "prototype_tags": [
        "rollable",
        "affix",
        "typeclasses.objects.WeaponObject",
        "prefix_atomic",
        "prefix_nucular"
    ],
}

PREFIX_REINFORCED = {
    "prototype_key": "prefix_reinforced",
    "prototype_tags": [
        "rollable",
        "affix",
        "typeclasses.objects.ArmorObject",
        "typeclasses.objects.Helmet",
        "typeclasses.objects.Shield",
    ],
}

PREFIX_OVERCLOCKED = {
    "prototype_key": "prefix_overclocked",
    "prototype_tags": [
        "rollable",
        "affix",
        "typeclasses.objects.WeaponObject",
        "prefix_inductive",
        "prefix_shocking"
    ],
}

PREFIX_SHOCKING = {
    "prototype_key": "prefix_shocking",
    "prototype_tags": [
        "rollable",
        "affix",
        "typeclasses.objects.WeaponObject",
        "prefix_inductive",
        "prefix_overclocked"
    ],
}

PREFIX_TOXIC = {
    "prototype_key": "prefix_toxic",
    "prototype_tags": [
        "rollable",
        "affix",
        "typeclasses.objects.WeaponObject",
        "prefix_malignant",
        "prefix_noxious"
    ],
}

SUFFIX_ASSEMBLER_DEVELOPMENT = {
    "prototype_key": "suffix_assembler_development",
    "prototype_tags": [
        "rollable",
        "affix",
        "typeclasses.objects.Helmet",
        "suffix_python_development",
        "suffix_ruby_development",
    ],
}

SUFFIX_ENSHITIFICATION = {
    "prototype_key": "suffix_enshitification",
    "prototype_tags": [
        "rollable",
        "affix",
        "typeclasses.objects.ArmorObject",
        "typeclasses.objects.Helmet",
        "typeclasses.objects.Shield",
        "typeclasses.objects.WeaponObject",
    ],
}

SUFFIX_PYTHON_DEVELOPMENT = {
    "prototype_key": "suffix_python_development",
    "prototype_tags": [
        "rollable",
        "affix",
        "typeclasses.objects.Helmet",
        "suffix_assembler_development",
        "suffix_ruby_development",
    ],
}

SUFFIX_RUBY_DEVELOPMENT = {
    "prototype_key": "suffix_ruby_development",
    "prototype_tags": [
        "rollable",
        "affix",
        "typeclasses.objects.Helmet",
        "suffix_assembler_development",
        "suffix_python_development",
    ],
}

SUFFIX_TORRENTING = {
    "prototype_key": "suffix_torrenting",
    "prototype_tags": [
        "rollable",
        "affix",
        "typeclasses.objects.ArmorObject",
        "typeclasses.objects.Helmet",
        "typeclasses.objects.Shield",
        "typeclasses.objects.WeaponObject",
    ],
}

BASE_WEAPON = {
    "prototype_key": "base_weapon",
    "typeclass": "typeclasses.objects.WeaponObject",
    "inventory_use_slot": WieldLocation.WEAPON_HAND,
    "quality": 60,
    "tier": 1,
}

BASE_WEAPON_NON_LETHAL = {
    "prototype_parent": ("material_non_lethal_static_nudge", "base_weapon"),
    "prototype_key": "base_weapon_non_lethal",
}

BASE_WEAPON_PHYSICAL = {
    "prototype_parent": ("material_physical_plasteel", "base_weapon"),
    "prototype_key": "base_weapon_physical",
}

BASE_WEAPON_TECH = {
    "prototype_parent": ("material_tech_weapon_quartz_core", "base_weapon"),
    "prototype_key": "base_weapon_tech",
    "inventory_use_slot": WieldLocation.TWO_HANDS,
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
    "prototype_tags": ["droppable", "weapon", "antifa_rioter"],
    "key": "bike lock",
    "attack_type": Ability.STR,
    "damage_roll": "1d6",
    "allowed_classes": [CHARACTER_CLASSES["antifa_rioter"]],
    "desc": "A lock attached to a chain designed to keep a bicycle secure."
}

WEAPON_PARKING_METER = {
    "prototype_parent": ("base_weapon_reach", "base_weapon_physical"),
    "prototype_key": "weapon_parking_meter",
    "prototype_tags": ["droppable", "weapon", "antifa_rioter"],
    "key": "parking meter",
    "attack_type": Ability.STR,
    "damage_roll": "1d8",
    "allowed_classes": [CHARACTER_CLASSES["antifa_rioter"]],
    "required_level": 5,
    "desc": "A cut off parking meter and attached pole can make a decent warhammer."
}

WEAPON_BALISONG = {
    "prototype_parent": ("base_weapon_melee", "base_weapon_physical"),
    "prototype_key": "weapon_balisong",
    "prototype_tags": ["droppable", "weapon", "min_maxer"],
    "key": "balisong",
    "attack_type": Ability.CUN,
    "damage_roll": "1d4",
    "allowed_classes": [CHARACTER_CLASSES["min_maxer"]],
    "desc": "A balisong, also known as a butterfly knife."
}

WEAPON_SAI = {
    "prototype_parent": ("base_weapon_melee", "base_weapon_physical"),
    "prototype_key": "weapon_sai",
    "prototype_tags": ["droppable", "weapon", "min_maxer"],
    "key": "sai",
    "attack_type": Ability.CUN,
    "damage_roll": "1d6",
    "allowed_classes": [CHARACTER_CLASSES["min_maxer"]],
    "required_level": 5,
    "parry": True,
    "desc": "A small 3-pronged weapon that can be used to deflect incoming attacks."
}

WEAPON_LAPTOP = {
    "prototype_parent": ("base_weapon_short_range", "base_weapon_tech"),
    "prototype_key": "weapon_laptop",
    "prototype_tags": ["droppable", "weapon", "hacker", "shitposter"],
    "key": "laptop",
    "attack_type": Ability.WIL,
    "defense_type": Ability.STR,
    "damage_roll": "2d4",
    "allowed_classes": [CHARACTER_CLASSES["hacker"], CHARACTER_CLASSES["shitposter"]],
    "desc": "A cheap laptop."
}

WEAPON_SMART_PHONE = {
    "prototype_parent": ("base_weapon_short_range", "base_weapon_tech"),
    "prototype_key": "weapon_smart_phone",
    "prototype_tags": ["droppable", "weapon", "hacker", "shitposter"],
    "key": "smart phone",
    "attack_type": Ability.WIL,
    "defense_type": Ability.STR,
    "damage_roll": "2d6",
    "allowed_classes": [CHARACTER_CLASSES["hacker"], CHARACTER_CLASSES["shitposter"]],
    "required_level": 5,
    "desc": "An older model smart phone."
}

WEAPON_DILDORANG = {
    "prototype_parent": ("base_weapon_medium_range", "base_weapon_physical"),
    "prototype_key": "weapon_dildorang",
    "prototype_tags": ["droppable", "weapon", "gooner"],
    "key": "dildorang",
    "attack_type": Ability.CUN,
    "defense_type": DefenseType.ARMOR,
    "damage_roll": "2d4",
    "allowed_classes": [CHARACTER_CLASSES["gooner"]],
    "desc": "A dildo perfectly curved so that it returns to the owner when thrown."
}

WEAPON_BALL_GAG_SLING = {
    "prototype_parent": ("base_weapon_medium_range", "base_weapon_physical"),
    "prototype_key": "weapon_ball_gag_sling",
    "prototype_tags": ["droppable", "weapon", "gooner"],
    "key": "ball gag sling",
    "attack_type": Ability.CUN,
    "defense_type": DefenseType.ARMOR,
    "damage_roll": "2d6",
    "allowed_classes": [CHARACTER_CLASSES["gooner"]],
    "desc": "A ball gag rigged into a sling",
    "required_level": 5,
}

WEAPON_DEFENSE_SPRAY = {
    "prototype_parent": ("base_weapon_medium_range", "base_weapon_non_lethal"),
    "prototype_key": "weapon_defense_spray",
    "prototype_tags": ["droppable", "weapon", "conspiracy", "pusher"],
    "key": "defense spray",
    "attack_type": Ability.WIL,
    "defense_type": DefenseType.STR,
    "damage_roll": "1d1",
    "allowed_classes": [CHARACTER_CLASSES["conspiracy"], CHARACTER_CLASSES["pusher"]],
    "desc": "Non lethal defense spray."
}

WEAPON_STUN_BATON = {
    "prototype_parent": ("base_weapon_melee", "base_weapon_non_lethal"),
    "prototype_key": "weapon_stun_baton",
    "prototype_tags": ["droppable", "conspiracy", "pusher"],
    "key": "stun baton",
    "attack_type": Ability.CUN,
    "defense_type": DefenseType.STR,
    "damage_roll": "1d1",
    "allowed_classes": [CHARACTER_CLASSES["conspiracy"], CHARACTER_CLASSES["pusher"]],
    "required_level": 5,
    "desc": "A non lethal stun baton."
}

BASE_ARMOR = {
    "prototype_key": "base_armor",
    "typeclass": "typeclasses.objects.ArmorObject",
    "inventory_use_slot": WieldLocation.BODY,
    "quality": 60,
    "tier": 1,
}

BASE_ARMOR_PHYSICAL = {
    "prototype_parent": ("material_physical_plasteel", "base_armor"),
    "prototype_key": "base_armor_physical",
}

BASE_ARMOR_TECH = {
    "prototype_parent": ("material_tech_armor_dust_weave_canvas", "base_armor"),
    "prototype_key": "base_armor_tech",
}

BASE_ARMOR_EVASIVE = {
    "prototype_parent": ("material_evasive_woven_synth_fiber", "base_armor"),
    "prototype_key": "base_armor_tech",
}

ARMOR_CHEST_PLATE = {
    "prototype_parent": "base_armor_physical",
    "prototype_key": "armor_chest_plate",
    "prototype_tags": ["droppable", "armor", "antifa_rioter", "conspiracy", "min_maxer", "pusher"],
    "key": "chest plate",
    "armor": 1,
    "allowed_classes": [
        CHARACTER_CLASSES["antifa_rioter"],
        CHARACTER_CLASSES["conspiracy"],
        CHARACTER_CLASSES["min_maxer"],
        CHARACTER_CLASSES["pusher"]
    ],
    "desc": "Basic chest plate that gives a minimal amount of protection in combat.",
}

ARMOR_SPORTSBALL_GEAR = {
    "prototype_parent": "base_armor_physical",
    "prototype_key": "armor_sportsball_gear",
    "prototype_tags": ["droppable", "armor", "antifa_rioter", "conspiracy", "min_maxer", "pusher"],
    "key": "sportsball gear",
    "display_name": "set of sportsball gear",
    "armor": 2,
    "allowed_classes": [
        CHARACTER_CLASSES["antifa_rioter"],
        CHARACTER_CLASSES["conspiracy"],
        CHARACTER_CLASSES["min_maxer"],
        CHARACTER_CLASSES["pusher"]
    ],
    "required_level": 5,
    "desc": "Some sportsball gear.",
}

ARMOR_TRENCH = {
    "prototype_parent": "base_armor_tech",
    "prototype_key": "armor_trench",
    "prototype_tags": ["droppable", "armor", "hacker", "shitposter"],
    "key": "trench",
    "max_system_load": 3,
    "allowed_classes": [CHARACTER_CLASSES["hacker"], CHARACTER_CLASSES["shitposter"]],
    "desc": "A basic full length trench coat."
}

ARMOR_HOODIE = {
    "prototype_parent": "base_armor_tech",
    "prototype_key": "armor_hoodie",
    "prototype_tags": ["droppable", "armor", "hacker", "shitposter"],
    "key": "hoodie",
    "max_system_load": 5,
    "allowed_classes": [CHARACTER_CLASSES["hacker"], CHARACTER_CLASSES["shitposter"]],
    "required_level": 5,
    "desc": "A dark hoodie with plenty of pockets.",
}

BASE_SHIELD = {
    "prototype_key": "base_shield",
    "typeclass": "typeclasses.objects.Shield",
    "inventory_use_slot": WieldLocation.SHIELD_HAND,
    "quality": 60,
    "materials": "physical",
    "tier": 1,
}

SHIELD_GARBAGE_LID = {
    "prototype_parent": "base_shield",
    "prototype_key": "shield_garbage_lid",
    "prototype_tags": ["droppable", "shield", "antifa_rioter", "conspiracy", "pusher"],
    "key": "garbage lid",
    "block": 10.0,
    "allowed_classes": [
        CHARACTER_CLASSES["antifa_rioter"],
        CHARACTER_CLASSES["conspiracy"],
        CHARACTER_CLASSES["pusher"]
    ],
    "desc": "The lid from a garbage can."
}

SHIELD_WOK = {
    "prototype_parent": "base_shield",
    "prototype_key": "shield_wok",
    "prototype_tags": ["droppable", "shield", "antifa_rioter", "conspiracy", "pusher"],
    "key": "wok",
    "block": 13.0,
    "allowed_classes": [
        CHARACTER_CLASSES["antifa_rioter"],
        CHARACTER_CLASSES["conspiracy"],
        CHARACTER_CLASSES["pusher"]
    ],
    "required_level": 5,
    "desc": "A used wok with one of the handles moved to the inside to me it suitable as a shield."
            " Smells like General Tso's Chicken."
}

BASE_HELMET = {
    "prototype_key": "base_helmet",
    "typeclass": "typeclasses.objects.Helmet",
    "inventory_use_slot": WieldLocation.HEAD,
    "quality": 60,
    "tier": 1,
}

BASE_HELMET_PHYSICAL = {
    "prototype_parent": ("material_physical_plasteel", "base_helmet"),
    "prototype_key": "base_helmet_physical",
    "materials": "physical",
}

BASE_HELMET_TECH = {
    "prototype_parent": ("material_tech_helmet_tinted_polymer", "base_helmet"),
    "prototype_key": "base_helmet_tech",
    "materials": "tech_helmet",
}

BASE_HELMET_EVASIVE = {
    "prototype_parent": ("material_evasive_woven_synth_fiber", "base_helmet"),
    "prototype_key": "base_helmet_evasive",
    "materials": "evasive",
}

HELMET_HOCKEY_MASK = {
    "prototype_parent": "base_helmet_physical",
    "prototype_key": "helmet_hockey_mask",
    "prototype_tags": ["droppable", "helmet", "antifa_rioter", "conspiracy", "min_maxer", "pusher"],
    "key": "hockey mask",
    "allowed_classes": [
        CHARACTER_CLASSES["antifa_rioter"],
        CHARACTER_CLASSES["conspiracy"],
        CHARACTER_CLASSES["min_maxer"],
        CHARACTER_CLASSES["pusher"]
    ],
    "desc": "Hockey masks are good for a slight amount of defense and scaring kids at summer camp."
}

HELMET_SPORTSBALL_HELMET = {
    "prototype_parent": "base_helmet_physical",
    "prototype_key": "helmet_sportsball_helmet",
    "prototype_tags": ["droppable", "helmet", "antifa_rioter", "conspiracy", "min_maxer", "pusher"],
    "key": "sportsball helmet",
    "allowed_classes": [
        CHARACTER_CLASSES["antifa_rioter"],
        CHARACTER_CLASSES["conspiracy"],
        CHARACTER_CLASSES["min_maxer"],
        CHARACTER_CLASSES["pusher"]
    ],
    "required_level": 5,
    "desc": "A sportsball helmet covers the entire head and has a face guard."
}

HELMET_SPECS = {
    "prototype_parent": "base_helmet_tech",
    "prototype_key": "specs",
    "prototype_tags": ["droppable", "helmet", "hacker", "shitposter"],
    "key": "specs",
    "display_name": "pair of specs",
    "allowed_classes": [CHARACTER_CLASSES["hacker"], CHARACTER_CLASSES["shitposter"]],
    "desc": "A pair of specs worn over the eyes."
}

HELMET_FEDORA = {
    "prototype_parent": "base_helmet_evasive",
    "prototype_key": "helmet_fedora",
    "prototype_tags": ["droppable", "helmet", "hacker", "shitposter"],
    "key": "fedora",
    "allowed_classes": [CHARACTER_CLASSES["hacker"], CHARACTER_CLASSES["shitposter"]],
    "required_level": 5,
    "desc": "A stylish fedora, tipped towards m'ladies."
}

HELMET_GIMP_MASK = {
    "prototype_parent": "base_helmet_physical",
    "prototype_key": "gimp_mask",
    "prototype_tags": ["droppable", "helmet", "gooner"],
    "key": "gimp mask",
    "allowed_classes": [CHARACTER_CLASSES["gooner"]],
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
    "prototype_tags": ["droppable", "consumable", "ration"],
    "key": "ration",
    "desc": "A grey protein block covered in pale-green nutrient paste. Recovers some health when"
            " eaten.",
    "uses": 1,
    "heal_value": 3,
    "consume_method": "eat"
}
