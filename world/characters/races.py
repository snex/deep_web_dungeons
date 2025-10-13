""" Races list. """

from dataclasses import dataclass

@dataclass(frozen=True)
class Race:
    """ Dataclass for a race. """
    key: str
    name: str
    desc: str
    strength_mod: int = 0
    cunning_mod: int = 0
    will_mod: int = 0

    def __str__(self):
        return self.name

RACES = {
    "human": Race(
        key="human",
        name="Human",
        desc="Humans are versatile and can choose which attributes to modify at creation."
             """

+2 Player Choice
-2 Player Choice
"""
    ),
    "furry": Race(
        key="furry",
        name="Furry",
        strength_mod=-1,
        cunning_mod=2,
        will_mod=-1,
        desc="Furries are anthropomorphic mammals with lightning reflexes and deceptive"
             " personalities. They loathe physical and intellectual exercise."
             """

-1 STR
+2 CUN
-1 WIL
"""
    ),
    "robot_llm":  Race(
        key="robot_llm",
        name="Robot LLM",
        cunning_mod=-2,
        will_mod=2,
        desc="A specialty CPU running LLM software inside of a Robot body. Robot LLMs are"
             " intelligent but find it almost impossible to be deceptive (at least on purpose)."
             """

-2 CUN
+2 WIL
"""
    ),
    "android": Race(
        key="android",
        name="Android",
        strength_mod=-1,
        will_mod=1,
        desc="Androids are Humans or Furries that have so many implants that they are effectively"
        " hybrids. The excessive surgery required has taken its toll on the user's body."
        """

-1 STR
+1 WIL
"""
    ),
    "mutant": Race(
        key="mutant",
        name="Toxic Mutant",
        strength_mod=2,
        will_mod=-2,
        desc="Toxic Mutants are Humans or Furries who have fallen into one of the many toxic"
             " waterways throughout the land. They have developed superhuman strength but their"
             " brains have been damaged."
             """

+2 STR
-2 WIL
"""
    ),
}
