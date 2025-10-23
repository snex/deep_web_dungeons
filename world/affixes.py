""" list of all affixes """

AFFIXES = {
    "prefix_acidic": {
        # TODO: instead of damage type and damage roll etc,
        #   supply a callable that applies the affix effects when called
        "damage_type": "acid",
        "damage_roll": "1d6",
        "desc": "acidic",
    },
    "prefix_atomic": {
        "damage_type": "radioactive",
        "damage_roll": "2d6",
        "desc": "atomic",
    },
    "prefix_based": {
        "desc": "based",
    },
    "prefix_caustic": {
        "damage_type": "acid",
        "damage_roll": "3d6",
        "desc": "caustic",
    },
    "prefix_corrosive": {
        "damage_type": "acid",
        "damage_roll": "2d6",
        "desc": "corrosive",
    },
    "prefix_cringe": {
        "desc": "cringe",
    },
    "prefix_inductive": {
        "damage_type": "shock",
        "damage_roll": "1d6",
        "desc": "inductive",
    },
    "prefix_malignant": {
        "damage_type": "toxic",
        "damage_roll": "2d6",
        "desc": "malignant",
    },
    "prefix_noxious": {
        "damage_type": "toxic",
        "damage_roll": "1d6",
        "desc": "noxious",
    },
    "prefix_nucular": {
        "damage_type": "radioactive",
        "damage_roll": "3d6",
        "desc": "nucular",
    },
    "prefix_radioactive": {
        "damage_type": "radioactive",
        "damage_roll": "1d6",
        "desc": "radioactive",
    },
    "prefix_reinforced": {
        "desc": "reinforced",
    },
    "prefix_overclocked": {
        "damage_type": "shock",
        "damage_roll": "3d6",
        "desc": "overclocked",
    },
    "prefix_shocking": {
        "damage_type": "shock",
        "damage_roll": "2d6",
        "desc": "shocking",
    },
    "prefix_toxic": {
        "damage_type": "toxic",
        "damage_roll": "3d6",
        "desc": "toxic",
    },
    "suffix_assembler_development": {
        "desc": "assembly development",
    },
    "suffix_enshitification": {
        "desc": "enshitification",
    },
    "suffix_python_development": {
        "desc": "python development",
    },
    "suffix_ruby_development": {
        "desc": "ruby development",
    },
    "suffix_torrenting": {
        "desc": "torrenting",
    },
}
