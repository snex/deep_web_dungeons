"""
MUD ruleset based on the _Knave_ OSR tabletop RPG by Ben Milton (modified for MUD use).

The rules are divided into a set of classes. While each class (except chargen) could
also have been stand-alone functions, having them as classes makes it a little easier
to use them as the base for your own variation (tweaking values etc).

- Roll-engine: Class with methods for making all dice rolls needed by the rules. Knave only
  has a few resolution rolls, but we define helper methods for different actions the
  character will be able to do in-code.
- Character generation - this is a container used for holding, tweaking and setting
  all character data during character generation. At the end it will save itself
  onto the Character for permanent storage.
- Improvement - this container holds rules used with experience to improve the
  character over time.
- Charsheet - a container with tools for visually displaying the character sheet in-game.

This module is designed to use by importing the `dice` singleton provided.

"""
from random import randint
from .random_tables import death_and_dismemberment as death_table

# Basic rolls


class DiceRollEngine:
    """
    This groups all dice rolls for game mechanics. These could all have been normal functions,
    but we are group them in a class to make them easier to partially override and replace later.

    """

    def roll(self, roll_string, max_number=10):
        """
        NOTE: Implement this with the dice roller contrib instead!

        """
        max_diesize = 1000
        roll_string = roll_string.lower()
        if "d" not in roll_string:
            raise TypeError(
                f"Dice roll '{roll_string}' was not recognized. Must be `<number>d<dicesize>`."
            )
        number, diesize = roll_string.split("d", 1)
        try:
            number = int(number)
            diesize = int(diesize)
        except Exception as exc:
            raise TypeError(
                f"The number and dice-size of '{roll_string}' must be numerical."
            ) from exc
        if 0 < number > max_number:
            raise TypeError(f"Invalid number of dice rolled (must be between 1 and {max_number})")
        if 0 < diesize > max_diesize:
            raise TypeError(f"Invalid die-size used (must be between 1 and {max_diesize} sides)")

        # At this point we know we have valid input - roll and add dice together
        return sum(randint(1, diesize) for _ in range(number))

    def roll_random_table(self, dieroll, table_choices):
        """
        Make a roll on a random table.

        Args:
            dieroll (str): The dice to roll, like 1d6, 1d20, 3d6 etc).
            table_choices (iterable): If a list of single elements, the die roll
                should fully encompass the table, like a 1d20 roll for a table
                with 20 elements. If each element is a tuple, the first element
                of the tuple is assumed to be a string 'X-Y' indicating the
                range of values that should match the roll.

        Returns:
            Any: The result of the random roll.

        Example:
            `roll table_choices = [('1-5', "Blue"), ('6-9': "Red"), ('10', "Purple")]`

        Notes:
            If the roll is outside of the listing, the closest edge value is used.

        """
        roll_result = self.roll(dieroll)
        if not table_choices:
            return None

        if isinstance(table_choices[0], (tuple, list)):
            # tuple with range conditional, like ('1-5', "Blue") or ('10', "Purple")
            max_range = -1
            min_range = 10**6
            for (valrange, choice) in table_choices:

                minval, *maxval = valrange.split("-", 1)
                minval = abs(int(minval))
                maxval = abs(int(maxval[0]) if maxval else minval)

                # we store the largest/smallest values so far in case we need to use them
                max_range = max(max_range, maxval)
                min_range = min(min_range, minval)

                if minval <= roll_result <= maxval:
                    return choice

            # if we have no result, we are outside of the range, we pick the edge values. It is also
            # possible the range contains 'gaps', but that'd be an error in the random table itself.
            if roll_result > max_range:
                return table_choices[-1][1]

            return table_choices[0][1]

        # regular list - one line per value.
        roll_result = max(1, min(len(table_choices), roll_result))
        return table_choices[roll_result - 1]

    death_map = {
        "weakened": "strength",
        "unsteady": "dexterity",
        "sickly": "constitution",
        "addled": "intelligence",
        "rattled": "wisdom",
        "disfigured": "charisma",
    }

    def roll_death(self, character):
        """
        Happens when hitting <= 0 hp. unless dead,

        """

        result = self.roll_random_table("1d8", death_table)
        if result == "dead":
            character.at_death()
        else:
            # survives with degraded abilities (1d4 roll)
            abi = self.death_map[result]

            current_abi = getattr(character, abi)
            loss = self.roll("1d4")

            current_abi -= loss

            if current_abi < -10:
                # can't lose more - die
                character.at_death()
            else:
                # refresh health, but get permanent ability loss
                new_hp = self.roll("1d4")
                character.heal(new_hp)
                setattr(character, abi, current_abi)

                character.msg(
                    "~" * 78 + "\n|yYou survive your brush with death, "
                    f"but are |r{result.upper()}|y and permanently |rlose {loss} {abi}|y.|n\n"
                    f"|GYou recover |g{new_hp}|G health|.\n" + "~" * 78
                )


# singletons

# access rolls e.g. with world.rules.dice.roll(...)
dice = DiceRollEngine()
