""" generate fake ads using tracery """

import random
import tracery
from tracery.modifiers import base_english
from wonderwords import RandomWord

from .dialog_base import DialogBase

# pylint: disable=too-few-public-methods
class Advertisement(DialogBase):
    """ class for generating ads with tracery """
    def __init__(self, target):
        self.target = target
        self.rw = RandomWord()
        self.rules = {
            "product": self._load_file("products"),
            "hey_target": f"Hey, {self.target}!",
            "let_me_tell_you": "Let me tell you",
            "lets_talk": "Let's talk",
            "got_a_sec": "Got a sec to talk about #product#",

            "intro": [
                "#let_me_tell_you# about #product#",
                "#lets_talk# about #product#",
            ],
            "story_start": [
                "#hey_target# #intro#.",
                "#intro#.",
                "#hey_target# #got_a_sec#?",
                "#got_a_sec#?",
            ],
            "testimonial": self._load_file("testimonials"),
            "discount_code": self.rw.word(word_min_length=4, word_max_length=6).upper(),
            "discount_rate": f"{random.randrange(10, 26)}%",
            "discount_type": [
                "at checkout",
                "your first order",
                "their mega premium pack",
                f"and to get {random.randrange(3, 11)} free gemstones |iand|I a custom hero",
            ],
            "discount_text": "Use code #discount_code# to get #discount_rate# off #discount_type#",

            "story": "#story_start# #testimonial#! #discount_text#.",
        }

    def generate_advertisement(self):
        """ Generates an advertisement based on the tracery grammar. """
        grammar = tracery.Grammar(self.rules)
        grammar.add_modifiers(base_english)

        return grammar.flatten("#story#")
