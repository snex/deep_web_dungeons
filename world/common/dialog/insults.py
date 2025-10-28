""" Generate insults using tracery. """

from random import randrange

import tracery
from tracery.modifiers import base_english

from .dialog_base import DialogBase

# pylint: disable=too-few-public-methods
class Insult(DialogBase):
    """ Class for generating insults using tracery. """
    def __init__(self, target):
        self.target = target
        self.rules = {
            "unsourced_start": self._load_file("unsourced_starts"),
            "sourced_start": self._load_file("sourced_starts"),
            "reputable_source": self._load_file("reputable_sources"),

            "unsourced_story_start": [
                "#unsourced_start#",
                "#unsourced_start# that",
            ],
            "story_start": [
                "#unsourced_story_start#",
                "#sourced_start# #reputable_source# that"
            ],

            "collection": self._load_file("collections"),
            "pathetic_adjective": self._load_file("pathetic_adjectives"),

            "definite_bad_guy": self._load_file("definite_bad_guys"),
            "indefinite_bad_guy": self._load_file("indefinite_bad_guys"),
            "bad_guy": [
                "#definite_bad_guy#",
                "#indefinite_bad_guy.a#",
            ],
            "friendly_verb": self._load_file("friendly_verbs", self.target.gender, "sub"),

            "bad_thing": self._load_file("bad_things"),

            "indefinite_victim": self._load_file("indefinite_victims"),
            "definite_victim": self._load_file("definite_victims", self.target.gender, "pos"),

            "victim": [
                "#definite_victim#",
                "#indefinite_victim.a#",
                "#pathetic_adjective.a# #indefinite_victim#"
            ],
            "victim_collection": [
                "#collection.a# full of #indefinite_victim.s#",
                "#collection.a# full of #pathetic_adjective# #indefinite_victim.s#"
            ],
            "indifferent_victim": [
                "#victim#",
                "#victim_collection#"
            ],

            "modifiable_victim_verb": self._load_file("modifiable_victim_verbs"),
            "unmodifiable_victim_verb": self._load_file("unmodifiable_victim_verbs"),
            "victim_verb_modifier": self._load_file("victim_verb_modifiers"),

            "intransitive_action": [
                "#modifiable_victim_verb# #indifferent_victim# #victim_verb_modifier#",
                "#modifiable_victim_verb# #indifferent_victim#",
                "#unmodifiable_victim_verb# #indifferent_victim#",
                "made #indifferent_victim# cry",
            ],

            "verb_phys": self._load_file("physical_verbs"),
            "verb_nonphys": self._load_file("non_physical_verbs"),

            "object_phys": self._load_file("physical_objects"),
            "object_nonphys": self._load_file("non_physical_objects"),

            "singular_transitive_action": [
                "#verb_phys# #victim.pos# #object_phys#",
                "#verb_nonphys# #victim.pos# #object_nonphys#"
            ],
            "plural_transitive_action": [
                "#verb_phys# #indifferent_victim.pos# #object_phys.s#",
                "#verb_nonphys# #indifferent_victim.pos# #object_nonphys.s#"
            ],
            "transitive_action": [
                "#singular_transitive_action#",
                "#plural_transitive_action#"
            ],

            "borrowed_action": [
                "borrowed #victim.pos# #object_phys# and never gave it back",
                "borrowed #victim_collection.pos# #object_phys.s# and never gave them back"
            ],

            "celebratory_verb": self._load_file("celebratory_verbs", self.target.gender, "sub"),
            "bad_event": self._load_file("bad_events"),

            "artwork": self._load_file("stories"),

            "bad_ingredient": self._load_file("bad_ingredients"),
            "good_food": self._load_file("good_foods"),

            "action": [
                "#intransitive_action#",
                "#transitive_action#",
                "#borrowed_action#",
                f"promised to buy {randrange(10,100)} #object_phys.s# from #indifferent_victim#"
                    " but then never paid",
                "#friendly_verb# #bad_guy#",
                "tried to sell #bad_thing# to #indifferent_victim#",
                "#celebratory_verb# #bad_event#",
                "spoiled the ending to #artwork#",
                "puts #bad_ingredient# on #good_food#"
            ],

            "story": "#story_start#"
        }

    def generate_insult(self):
        """ Generates an insult based on the tracery grammar. """
        grammar = tracery.Grammar(self.rules)
        grammar.add_modifiers(base_english)
        grammar.add_modifiers(self._possessive_modifiers())
        grammar.add_modifiers(self._pronoun_modifiers())

        return grammar.flatten(f"#story# {self.target} #action#!")
