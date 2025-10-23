"""
roll tables for drops

the table is an array of 2-tuples. the first element is the thing to be rolled and the 
second element is the number of times that item appears in the pool. when the game is loaded
these tables will be mutated so that the second element is a cumulative total and hte rolls
will happen from that structure, as that is easier to roll against.

if the item rolled is also a key in _DROP_TABLES, then we roll again against that new key
until we come to a key that is not in _DROP_TABLES. at that point, we have the item we want.
"""

DROP_TABLES = {
    "generic": [
        ("base_quantum_lattice",         1),
        ("nothing",                      2),
        ("consumable",                   4),
        ("equipment",                    4),
    ],
    "tiers": [
        (4,                              1),
        (3,                              5),
        (2,                             20),
        (1,                            100),
    ],
    "affixes": [
        ("prefix_caustic",               1),
        ("prefix_nucular",               1),
        ("prefix_overclocked",           1),
        ("prefix_toxic",                 1),

        ("suffix_assembler_development", 1),

        ("prefix_atomic",                3),
        ("prefix_corrosive",             3),
        ("prefix_malignant",             3),
        ("prefix_shocking",              3),

        ("suffix_ruby_development",      3),

        ("prefix_acidic",                9),
        ("prefix_based",                 9),
        ("prefix_cringe",                9),
        ("prefix_inductive",             9),
        ("prefix_noxious",               9),
        ("prefix_radioactive",           9),
        ("prefix_reinforced",            9),

        ("suffix_enshitification",       9),
        ("suffix_python_development",    9),
        ("suffix_torrenting",            9),
    ],
    "consumable": [
        ("ration",                       1),
    ],
    "equipment": [
        ("cclass",                       1),
    ],
    "cclass": [
        ("antifa_rioter",                1),
        ("mix_maxer",                    1),
        ("hacker",                       1),
        ("gooner",                       1),
        ("pusher",                       1),
        ("gym_bro",                      1),
        ("shitposter",                   1),
        ("conspiracy",                   1),
    ],
    "base_quantum_lattice": [
        ("nexus_diamond",                1),
        ("chromatic_heart",             11),
        ("void_spark",                  37),
        ("phase_pearl",                123),
        ("singularity_shard",          412),
        ("resonance_crystal",         1372),
        ("echo_stone",                4572),
        ("static_bloom",             15242),
        ("dust_shard",               50805),
    ],
}
