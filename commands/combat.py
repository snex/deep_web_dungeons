"""
Combat commands.
"""

from random import choice

from world.combat import CombatHandler
from world.enums import CombatRange
from .command import Command


class CombatCommand(Command):
    """ Commands for use during combat. """
    cooldown_key = ""
    cooldown_message = "You can't do that for another {delay} seconds."

    in_combat_only = True
    requires_target = True

    def __init__(self, **kwargs):
        self.target = None  # This line is to avoid the IDE complaints
        super().__init__(**kwargs)

    def parse(self):
        super().parse()
        target = self.get_target()
        self.target = target

    def get_target(self):
        """ Get default target if none specified. """
        if not self.args:
            # TODO Use the last hit enemy OR
            # TODO Find the closest enemy in combat.
            return None

        return self.caller.search(self.args)

    def validate_target(self) -> bool:
        """ Validates whether target is valid. """
        target = self.target
        if not target or not target.dbid or not hasattr(target, "combat"):
            self.caller.msg("Invalid target.")
            return False

        if target.is_pc and not (target.location and target.location.allow_pvp):
            self.caller.msg("You can't attack another player here.")
            return False

        return True

    def at_post_cmd(self):
        if self.caller.combat:
            self.caller.combat.update()


class CmdInitiateCombat(CombatCommand):
    """Engage an opponent in combat."""

    key = "attack"
    aliases = ("engage", "kill")

    in_combat_only = False

    def func(self):
        caller = self.caller
        target = self.target
        if not self.validate_target():
            return

        combat = CombatHandler.get_or_create(caller, target)
        combat_range = combat.get_range(caller, target)
        caller.msg(
            f"You prepare for combat! {target}"
            f" is at {combat_range.name.lower()} range."
        )

        # TODO: trigger combat prompt


class CmdAdvance(CombatCommand):
    """Advance towards a target."""

    key = "advance"
    aliases = ("approach",)
    locks = "cmd:in_combat()"

    cooldown_key = "combat_move"
    cooldown_message = "You can't move for another {delay} seconds."

    def func(self):
        caller = self.caller
        target = self.target
        if not self.validate_target():
            return

        combat: CombatHandler = caller.combat
        if combat.approach(caller, target):
            # TODO: base movement cooldown on character stats
            caller.cooldowns.add(self.cooldown_key, 3)
            combat_range = combat.get_range(caller, target)
            caller.location.msg_contents(
                "{attacker} advances towards {target}.",
                exclude=caller,
                mapping={"attacker": caller, "target": target},
            )
            caller.msg(
                f"You advance towards {target}"
                f" and are now at {combat_range.lower()} range."
            )
        else:
            caller.msg(
                f"You can't advance any further towards {target}."
            )

        # TODO: trigger combat prompt


class CmdRetreat(CombatCommand):
    """Move away from a target."""

    key = "retreat"
    locks = "cmd:in_combat()"

    cooldown_key = "combat_move"
    cooldown_message = "You can't move for another {delay} seconds."

    def func(self):
        caller = self.caller
        target = self.target
        if not self.validate_target():
            return

        combat = caller.combat
        if combat.retreat(caller, target):
            # TODO: base movement cooldown on character stats
            caller.cooldowns.add(self.cooldown_key, 3)
            combat_range = combat.get_range(caller, target)
            caller.location.msg_contents(
                "{attacker} retreats from {target}.",
                exclude=caller,
                mapping={"attacker": caller, "target": target},
            )
            caller.msg(
                f"You retreat from {target}"
                f" and are now at {combat_range.lower()} range."
            )
        else:
            caller.msg(
                f"You can't retreat any further from {target}."
            )

        # TODO: trigger combat prompt


class CmdHit(CombatCommand):
    """
    Basic melee combat attack.

    hit <target>
    """

    key = "hit"
    locks = "cmd:in_combat() and melee_equipped()"

    def func(self):
        caller = self.caller
        target = self.target
        if not self.validate_target():
            return

        combat = caller.combat
        if not combat:
            caller.msg("You are not in combat!")
            return

        if not combat.rules.validate_weapon_attack(caller, target):
            return

        hittable = combat.in_range(caller, target, CombatRange.MELEE)
        if hittable is None:
            caller.msg("You can't fight that.")
            return
        if not hittable:
            caller.msg(f"{target} is too far away.")
            return

        combat.at_melee_attack(caller, target)

class CmdShoot(CombatCommand):
    """Basic ranged combat attack."""

    key = "shoot"
    locks = "cmd:in_combat() and ranged_equipped()"

    cooldown_key = "attack"
    cooldown_message = "You can't attack for {delay} more seconds."

    def func(self):
        caller = self.caller
        target = self.target
        if not self.validate_target():
            return

        combat = caller.combat
        if not combat:
            caller.msg("You are not in combat!")
            return

        if not combat.rules.validate_weapon_attack(caller, target):
            return

        combat.at_ranged_attack(caller, target)


class CmdFlee(CombatCommand):
    """Command to disengage and escape from combat."""

    key = "flee"
    aliases = ("escape",)
    locks = "cmd:in_combat()"

    cooldown_key = "combat_move"
    cooldown_message = "You can't move for another {delay} seconds."
    requires_target = False

    def func(self):
        caller = self.caller
        exits = [ex for ex in caller.location.contents if ex.destination]
        if not exits:
            caller.msg("There's nowhere to run!")
            return

        # TODO: add checks for flight success, e.g. `caller.at_pre_flee`

        # this is the actual fleeing bit
        caller.msg("You flee!")
        caller.combat.remove(caller)
        target = choice(exits)
        # using execute_cmd instead of duplicating all the checks in ExitCommand
        caller.execute_cmd(target.key)

    def get_target(self):
        return None
