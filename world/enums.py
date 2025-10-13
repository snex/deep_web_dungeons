"""
Place for game-wide enums.
"""

from enum import IntEnum, Enum


class Criticals(Enum):
    """ Critical success and failure. """
    CRITICAL_FAILURE = "critical_failure"
    CRITICAL_SUCCESS = "critical_success"

class Ability(Enum):
    """
    Ability stats.
    """

    STR = "strength"
    CUN = "cunning"
    WIL = "will"

class WieldLocation(Enum):
    """
    Wield (or wear) locations.

    """

    # wield/wear location
    BACKPACK = "backpack"
    WEAPON_HAND = "weapon_hand"
    SHIELD_HAND = "shield_hand"
    TWO_HANDS = "two_handed_weapons"
    BODY = "body"  # armor
    HEAD = "head"  # helmets


class ObjType(Enum):
    """
    Object types

    """

    WEAPON = "weapon"
    ARMOR = "armor"
    SHIELD = "shield"
    HELMET = "helmet"
    CONSUMABLE = "consumable"
    GEAR = "gear"
    QUEST = "quest"
    TREASURE = "treasure"

class PhysicalObjectMaterial(Enum):
    """ Physical object materials. """

    PLASTEEL = "plasteel"
    CHITON = "chiton"
    STEEL = "steel"
    CARBON_FIBER = "carbon fiber"
    VIBRANIUM = "vibranium"
    TITANIUM = "titanium"
    BIO_METALLIC = "bio-metallic"
    NANO_WEAVE = "nano-weave"
    PHASE_STEEL = "phase-steel"

class EvasiveObjectMaterial(Enum):
    """ Object materials that increase evasion. """

    WOVEN_SYNTH_FIBER = "woven synth-fiber"
    KTHARR_SHELL = "k'tharr shell"
    BIO_LUMINESCENT_SCALE = "bio-luminescent scale"
    PHASE_SILK = "phase silk"
    STATIC_CHARGED_CARAPACE = "static-charged carapace"
    REFRACTIVE_PLATED = "refractive plated"
    NEURO_REACTIVE_MEMBRANE = "neuro-reactive membrane"
    QUANTUM_LACED_WEAVE = "quantum-laced weave"
    SHADOW_SKIN = "shadow skin"

class NonLethalWeaponMaterial(Enum):
    """ Non-lethal weapon materials. """

    STATIC_NUDGE = "static nudge"
    SLEEP_SPORE = "sleep spore"
    SONIC_HUM = "sonic hum"
    STICKY_WEB = "sticky web"
    NEURAL_TINGLE = "neural tingle"
    GRAV_PULL = "grav-pull"
    BIO_STATIC_FIELD_EMITTING = "bio-static field emitting"
    PHASE_SHIFT_PULSE = "phase-shift pulse"
    NEURAL_LOCKING = "neural locking"

class TechWeaponMaterial(Enum):
    """
    Tech weapon materials.

    Unlike physical weapons and armor, tech weapons and armor have different materials.
    """

    QUARTZ_CORE = "quartz core"
    SILICON_SHARD = "silicon shard"
    BIO_SYNAPSE = "bio-synapse"
    FERRO_LOGIC = "ferro-logic"
    NEURAL_LATTICE = "neural lattice"
    QUANTUM_WEAVER = "quantim weaver"
    HYPER_RESONANCE_CORE = "hyper-resonance core"
    ECHO_LOGIC_MATRIX = "echo-logic matrix"
    SINGULARITY_NODE = "singularity node"

class TechArmorMaterial(Enum):
    """ Tech body armor materials. """

    DUST_WEAVE_CANVAS = "dust-weave canvas"
    BIO_LUMINESCENT_MOSS_LINED = "bio-luminescent moss-lined"
    RECYCLED_DATA_RIBBON = "recycled data ribbon"
    NANOFIBER = "nanofiber"
    MUTANT_SCALE_MESH = "mutant scale mesh"
    SIGNAL_WIRE = "signal wire"
    POLISHED_LOGIC_NODE = "polished logic-node"
    CRYSTALIZED_MUTANT_VENOM = "crystalized mutant venom"
    QUANTUM_ENTANGLED_ARRAY = "quantum-entangled array"

class TechHelmetMaterial(Enum):
    """ Tech headgear materials. """

    TINTED_POLYMER = "tinted polymer"
    STATIC_FILTERING = "static filtering"
    CHROMA_LAYERED = "chroma-layered"
    GHOST_WEAVE = "ghost weave"
    NODE_CONNECTED = "node-connected"
    SPECTRUM_SHIFTING = "specrtrum-shifting"
    REALITY_FILTERING = "reality filtering"
    QUANTUM_WEAVING = "quantum weaving"
    VOID_GAZING = "void gazing"

class Allegiance(Enum):
    """
    Allegiance flags.
    """

    ALLEGIANCE_HOSTILE = "hostile"
    ALLEGIANCE_NEUTRAL = "neutral"
    ALLEGIANCE_FRIENDLY = "friendly"

class CombatRange(IntEnum):
    """
    Maximum combat range values
    """
    MELEE = 1
    REACH = 2
    SHORT_RANGE = 3
    MEDIUM_RANGE = 4
    LONG_RANGE = 6


class AttackType(IntEnum):
    """
    Attack types.
    """
    MELEE = 1
    RANGED = 2
    THROWN = 3
    TECH = 4


class DefenseType(Enum):
    """
    Defense types.
    """
    STR = "strength"
    CUN = "cunning"
    WIL = "will"
    ARMOR = "armor"

class CardinalDirections(Enum):
    """
    Cardinal directions on the compass.
    """

    NORTH = "north"
    NORTHEAST = "northeast"
    EAST = "east"
    SOUTHEAST = "southeast"
    SOUTH = "south"
    SOUTHWEST = "southwest"
    WEST = "west"
    NORTHWEST = "northwest"
