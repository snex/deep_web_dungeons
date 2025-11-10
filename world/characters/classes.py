"""Character classes list."""

from dataclasses import dataclass
from types import MappingProxyType


@dataclass(frozen=True)
class StatDice:
    """Dataclass for StatDice"""

    health_dice: tuple[int, int]
    mana_dice: tuple[int, int]
    stamina_dice: tuple[int, int]


@dataclass(frozen=True)
class CharacterClass:
    """Dataclass for a character class."""

    key: str
    name: str
    desc: str
    primary_stat: str
    secondary_stat: str
    stat_dice: StatDice
    starting_gear: dict

    def __str__(self):
        return self.name


CHARACTER_CLASSES = MappingProxyType({
    "antifa_rioter": CharacterClass(
        key="antifa_rioter",
        name="Antifa Rioter",
        primary_stat="strength",
        secondary_stat="cunning",
        desc="Antifa Rioters love to mindlessly wade into melee combat with anything they perceive"
        " to be slightly disagreeable. They will use anything they can find as a weapon,"
        " whether that be a bicycle lock, vibranium axe, or even their bare hands. While they"
        " are impossible to have as friends - even among each other, you will be glad you"
        " joined a combat party with one when you see who all the foes target."
        """

Primary Stat:   STR
Secondary Stat: CUN

HP:              |gHigh|n
Max System Load: |rLow|n
Stamina:         |gHigh|n
""",
        stat_dice=StatDice(
            health_dice=(1, 10),
            mana_dice=(1, 6),
            stamina_dice=(1, 12),
        ),
        starting_gear={
            "weapon": "bike_lock",
            "weapon_desc": "|xplasteel bike lock|n",
            "shield": "garbage_lid",
            "shield_desc": "|xplasteel garbage lid|n",
            "helmet": "hockey_mask",
            "helmet_desc": "|xplasteel hockey mask|n",
            "armor": "chest_plate",
            "armor_desc": "|xplasteel chest plate|n",
        },
    ),
    "min_maxer": CharacterClass(
        key="min_maxer",
        name="Min-Maxer",
        primary_stat="cunning",
        secondary_stat="will",
        desc="With a Min-Maxer around, the battle is fought and won long before leaving the"
        " protective walls of Control Station 7. In fact it is fought by spending hours poring"
        " over spreadsheets finding a way to squeeze out an extra 0.05 DPS through performing"
        " an esoteric sequence of skills only found in splatbooks that had ten printings at"
        " GenCon '97. Some people boost their armor to lessen the severity of blows, but"
        ' Min-Maxers understand the path to victory - "Don\'t get hit."'
        """

Primary Stat:   CUN
Secondary Stat: WIL

HP:              |YMedium|n
Max System Load: |YMedium|n
Stamina:         |gHigh|n
""",
        stat_dice=StatDice(
            health_dice=(1, 8),
            mana_dice=(1, 8),
            stamina_dice=(1, 12),
        ),
        starting_gear={
            "weapon": "balisong",
            "weapon_desc": "|xplasteel balisong|n",
            "shield": "none",
            "shield_desc": "none",
            "helmet": "hockey_mask",
            "helmet_desc": "|xplasteel hockey mask|n",
            "armor": "chest_plate",
            "armor_desc": "|xplasteel chest plate|n",
        },
    ),
    "hacker": CharacterClass(
        key="hacker",
        name="Hacker",
        primary_stat="will",
        secondary_stat="cunning",
        desc="Hackers fancy themselves cyber samurai and keyboard cowboys while maintaining that"
        " everyone else has no idea what's going on and are just cattle. They are euphoric by"
        " being enlightened by their own intelligence. In a battle you might find one hiding"
        " in the back ranks, using their laptops to upload malware into the cybernetic"
        " implants of the enemy. They truly shine at breaking into locked terminals or"
        " decrypting salvaged data banks - after which they will gladly tell you about how you"
        " would have died out there without their efforts."
        """

Primary Stat:   WIL
Secondary Stat: CUN

HP:              |rLow|n
Max System Load: |gHigh|n
Stamina:         |rLow|n
""",
        stat_dice=StatDice(
            health_dice=(1, 6),
            mana_dice=(1, 10),
            stamina_dice=(1, 8),
        ),
        starting_gear={
            "weapon": "laptop",
            "weapon_desc": "|xquartz core laptop|n",
            "shield": "none",
            "shield_desc": "none",
            "helmet": "specs",
            "helmet_desc": "|xtinted polymer specs|n",
            "armor": "trench",
            "armor_desc": "|xdust-weave canvas trench|n",
        },
    ),
    "gooner": CharacterClass(
        key="gooner",
        name="Gooner",
        primary_stat="cunning",
        secondary_stat="strength",
        desc="Gooners are perverted freaks that feel the need to share their kinks with everyone"
        " around them, especially if nobody asked. They specialize in ranged by combat,"
        " usually by limp-wristedly throwing anything they have on hand at the enemy. If they"
        " are unable to find a foreign object to throw, they may even resort to using their"
        " own bodily fluids."
        """

Primary Stat:   CUN
Secondary Stat: STR

HP:              |YMedium|n
Max System Load: |YMedium|n
Stamina:         |YMedium|n
""",
        stat_dice=StatDice(
            health_dice=(1, 8),
            mana_dice=(1, 8),
            stamina_dice=(1, 10),
        ),
        starting_gear={
            "weapon": "dildorang",
            "weapon_desc": "|xplasteel dildorang|n",
            "shield": "none",
            "shield_desc": "none",
            "helmet": "gimp_mask",
            "helmet_desc": "|xplasteel gimp mask|n",
            "armor": "none",
            "armor_desc": "none",
        },
    ),
    "shitposter": CharacterClass(
        key="shitposter",
        name="Shitposter",
        primary_stat="cunning",
        secondary_stat="will",
        desc="Shitposters crave the attention of others, regardless of the sentiment. They will"
        " relentlessly pelt enemies with insults, distractions, and spam attacks. Once"
        " somebody decides to engage with a Shitposter, they will likely be too distracted to"
        " deal with anything else - including a knietic hammer to the face. Shitposters can"
        " also focus on benefiting allied morale through epic memes."
        """

Primary Stat:   CUN
Secondary Stat: WIL

HP:              |YMedium|n
Max System Load: |YMedium|n
Stamina:         |YMedium|n
""",
        stat_dice=StatDice(
            health_dice=(1, 8),
            mana_dice=(1, 8),
            stamina_dice=(1, 10),
        ),
        starting_gear={
            "weapon": "laptop",
            "weapon_desc": "|xquartz core laptop|n",
            "shield": "none",
            "shield_desc": "none",
            "helmet": "none",
            "helmet_desc": "none",
            "armor": "chest_plate",
            "armor_desc": "|xplasteel chest plate|n",
        },
    ),
    "conspiracy": CharacterClass(
        key="conspiracy",
        name="Conspiracy Nut",
        primary_stat="will",
        secondary_stat="strength",
        desc="Once you get a Conspiracy Nut going, it is impossible to stop them. Whether it's"
        " the claim that Control Station 7 is secretly run by pedophile cultists, the"
        " terrorist attack on Starbase Alpha was a false flag, or that post-quantum encryption"
        " is secretly backdoored and sending all your communications to the barbarians, they"
        " always have a way to confuse and distract. With a Conspiracy Nut on your team, you"
        " can be sure that the battlefield will be draped in chaos."
        """

Primary Stat:   WIL
Secondary Stat: STR

HP:              |YMedium|n
Max System Load: |gLow|n
Stamina:         |gHigh|n
""",
        stat_dice=StatDice(
            health_dice=(1, 8),
            mana_dice=(1, 6),
            stamina_dice=(1, 12),
        ),
        starting_gear={
            "weapon": "defense_spray",
            "weapon_desc": "|xstatic nudge defense spray|n",
            "shield": "garbage_lid",
            "shield_desc": "|xplasteel garbage lid|n",
            "helmet": "none",
            "helmet_desc": "none",
            "armor": "chest_plate",
            "armor_desc": "|xplasteel chest plate|n",
        },
    ),
    "pusher": CharacterClass(
        key="pusher",
        name="Pusher",
        primary_stat="will",
        secondary_stat="strength",
        desc="Need a fix? The Pusher has what you crave. They don't only deal in basic recovery"
        " drugs, but can find something for almost any effect you're looking for - and"
        " properly administer it. The more experienced Pushers can even discover new effects"
        " that are currently unknown to medical science."
        """

Primary Stat:   WIL
Secondary Stat: STR

HP:              |gHigh|n
Max System Load: |YMedium|n
Stamina:         |rLow|n
""",
        stat_dice=StatDice(
            health_dice=(1, 10),
            mana_dice=(1, 8),
            stamina_dice=(1, 8),
        ),
        starting_gear={
            "weapon": "none",
            "weapon_desc": "none",
            "shield": "garbage_lid",
            "shield_desc": "|xplasteel garbage lid|n",
            "helmet": "hockey_mask",
            "helmet_desc": "|xplasteel hockey mask|n",
            "armor": "chest_plate",
            "armor_desc": "|xplasteel chest plate|n",
        },
    ),
    "gym_bro": CharacterClass(
        key="gym_bro",
        name="Gym Bro",
        primary_stat="strength",
        secondary_stat="will",
        desc="Gym Bros can often be found in training arenas, giving keto diet advice to anyone"
        " willing to listen. They are highly effective at pumping |iothers|I up, but rarely"
        " very useful in a fight themselves. While a Gym Bro might run at the sight of any"
        " real danger, they will be able to patch you up when the scuffle is over."
        """

Primary Stat:   STR
Secondary Stat: CUN

HP:              |gHigh|n
Max System Load: |rLow|n
Stamina:         |gHigh|n
""",
        stat_dice=StatDice(
            health_dice=(1, 10),
            mana_dice=(1, 6),
            stamina_dice=(1, 12),
        ),
        starting_gear={
            "weapon": "none",
            "weapon_desc": "none",
            "shield": "none",
            "shield_desc": "none",
            "helmet": "none",
            "helmet_desc": "none",
            "armor": "none",
            "armor_desc": "none",
        },
    ),
})
