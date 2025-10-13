"""
Combat Rules engine.
"""

from typing import Self, TYPE_CHECKING
from world import rules

from .enums import CombatRange, AttackType


if TYPE_CHECKING:
    from typeclasses.characters import BaseCharacter
    from typeclasses.objects import WeaponObject

_MAX_RANGE = max(en.value for en in CombatRange)

# format for combat prompt, currently unused
# health, mana, current attack cooldown
COMBAT_PROMPT = "HP {hp} - MP {mana} - SP {stamina}"

class AttackRules:
    """
    Class to determine whether or not an attacker can attack a target.
    """

    _RULES = {
        "_not_in_combat": "You are not in combat.",
        "_target_not_in_combat": "{target.get_display_name(attacker)} is not in combat with you.",
        "_no_pvp_zone": "You can't attack another player here.",
        "_player_on_cooldown": "You can't attack for"
                               "{attacker.cooldowns.time_left('attack', use_int=True)}"
                               "more seconds.",
        "_target_out_of_range": "{target} is too far away.",
        "_out_of_stamina": "You are too exhausted!",
    }

    def __init__(self, attacker, target, combat_handler):
        self.attacker = attacker
        self.target = target
        self.combat_handler = combat_handler
        self.invalid_msg = ""

    def attack_invalid(self):
        """
        Run through the attack rules and return True if any rules trigger.
        Also sets self.invalid_msg of the rule that triggered.
        """

        for rule, msg in self._RULES.items():
            if self.apply_rule(rule):
                self.invalid_msg = msg.format(
                    attacker=self.attacker,
                    target=self.target,
                )
                return True

        return False

    def apply_rule(self, rule):
        """ Apply a single rule and return whether it passes. Does not set the invalid_msg. """
        return getattr(self, rule, None)(self.attacker, self.target, self.combat_handler)

    def _not_in_combat(self, attacker, _target, _combat_handler):
        return not attacker.combat

    def _target_not_in_combat(self, attacker, target, _combat_handler):
        return not target.combat or target.combat != attacker.combat

    def _no_pvp_zone(self, _attacker, target, _combat_handler):
        return target.is_pc and not (target.location and target.location.allow_pvp)

    def _player_on_cooldown(self, attacker, _target, _combat_handler):
        return not attacker.cooldowns.ready("attack")

    def _target_out_of_range(self, attacker, target, combat_handler):
        weapon_range = attacker.weapon.attack_range
        return not combat_handler.in_range(attacker, target, weapon_range)

    def _out_of_stamina(self, attacker, _target, combat_handler):
        attack_type = attacker.weapon.attack_type
        stamina_cost = combat_handler.rules.get_attack_stamina_cost(
            attacker,
            attack_type,
            attacker.weapon.stamina_cost
        )
        return stamina_cost > attacker.stamina

class CombatRules:
    """ Class for handling combat rules. """

    __slots__ = ("handler",)

    def __init__(self, handler: 'CombatHandler'):
        self.handler = handler

    def validate_weapon_attack(self, attacker: 'BaseCharacter', target: 'BaseCharacter') -> bool:
        """ Base method for validating weapon attack. """
        attack_rules = AttackRules(attacker, target, combat_handler=self.handler)
        attack_invalid = attack_rules.attack_invalid()

        if attack_invalid:
            attacker.msg(attack_rules.invalid_msg)
            return False

        return True

    def get_initial_position(self, fighter: 'BaseCharacter') -> CombatRange:
        """ Determine the initial positions of all the combatants. """
        # TODO Ranged fighters should start further apart
        # TODO Fighters should be grouped according to alliance at the start of a fight.
        # TODO Fighters should be added at the furthest position on their alliance's side if added
        #          during the fight.

        # Temporary code until we can implement the above
        if getattr(fighter, "is_pc", False):
            return CombatRange.MELEE

        return CombatRange.MELEE

    @property
    def is_combat_finished(self) -> bool:
        """ Determine if combat is finished. """
        return len(self.handler.positions) <= 1

    def get_strike_zone(self, attack_location, defense_location):
        """
        We can expand on this to include adjacent sides/etc or weightings/corners
        """
        return attack_location == defense_location

    def get_attack_stamina_cost(self, attacker, _attack_type, base_cost):
        """ Get stamina cost for attacker. """
        if attacker.aggro == "aggressive":
            cost = int(base_cost * 1.5)
        elif attacker.aggro == "defensive":
            cost = int(base_cost / 2)
        else:
            cost = base_cost

        return cost

    def get_defense_stamina_cost(self, _attacker, _attack_type, _base_cost, _target):
        """ Get stamina cost to defender (maybe unused?). """
        return 2  # TODO FIXME update this

class CombatHandler:
    """
    Main class for handling combat.
    """

    __slots__ = ('positions', 'rules')

    rules_class = CombatRules

    def __init__(self, attacker, target, custom_rules=None):
        self.rules = custom_rules(self) if custom_rules else self.rules_class(self)
        self.positions: dict['BaseCharacter', CombatRange] = {}
        self.add(attacker)
        self.add(target)

    @classmethod
    def get_or_create(cls, attacker, target) -> Self:
        """
        This function will create the CombatHandler or merge existing ones, then return it.
        """
        attacker_combat: Self = attacker.combat
        target_combat: Self = target.combat

        if attacker_combat and target_combat and attacker_combat != target_combat:
            attacker_combat.merge(target.combat)
            return attacker_combat

        if attacker_combat:
            attacker_combat.add(target)
            return attacker_combat

        if target_combat:
            target_combat.add(attacker)
            return target_combat

        return CombatHandler(attacker, target)

    def add(self, fighter: 'BaseCharacter') -> None:
        """
        Add a new combatant to the combat instance.
        """
        assert fighter not in self.positions, f"Fighter {fighter} was already added to the fight!"

        self.positions[fighter] = self.rules.get_initial_position(fighter)
        fighter.combat = self

    def remove(self, fighter: 'BaseCharacter') -> None:
        """
        Removes a fighter from the combat instance.
        """
        assert fighter in self.positions, f"Fighter {fighter} was already removed from the fight!"


        del self.positions[fighter]
        if fighter.combat == self:
            fighter.combat = None

        if self.is_finished:
            self.end_combat()


    def merge(self, other):
        """
        Merge another combat instance into this one
        """
        self.positions.update(other.positions)
        for obj in other.positions.keys():
            obj.combat = self

        other.positions = {}

    def update(self):
        """ Check to see if we need to end combat. """

        if self.is_finished:
            self.end_combat()

    def end_combat(self) -> None:
        """ End the combat. """

        for fighter in self.positions:
            if fighter.combat == self:
                fighter.combat = None

            if fighter.is_pc:
                # Temporary message for debugging
                # fighter.msg("You are victorious!")
                pass

        self.positions = {}

    @property
    def is_finished(self) -> bool:
        """ Is Combat finished? """
        return self.rules.is_combat_finished

    def get_range(self, attacker: 'BaseCharacter', target: 'BaseCharacter') -> CombatRange:
        """
        Get the distance from target in terms of weapon range.
        """
        assert attacker in self.positions, f"Attacker {attacker} is not in combat!"
        assert target in self.positions, f"Target {target} is not in combat!"

        distance = abs(self.positions[attacker] - self.positions[target])
        for range_enum in CombatRange:
            if range_enum.value >= distance:
                return range_enum

        return CombatRange.LONG_RANGE

    def in_range(self, attacker, target, combat_range):
        """Check if target is within the specified range of attacker."""
        assert attacker in self.positions, f"Attacker {attacker} is not in combat!"
        assert target in self.positions, f"Target {target} is not in combat!"

        distance = abs(self.positions[attacker] - self.positions[target])

        return distance <= combat_range

    def any_in_range(self, attacker: 'BaseCharacter', combat_range: CombatRange) -> bool:
        """
        Determine if any opponents are in range to be attacked by `attacker`.
        """

        assert attacker in self.positions, f"Attacker {attacker} is not in combat!"

        a_pos = self.positions[attacker]

        return any(
            p
            for c, p in self.positions.items()
            if abs(a_pos - p) <= combat_range and c != attacker
        )

    def approach(self, mover: 'BaseCharacter', target: 'BaseCharacter') -> bool:
        """
        Move a combatant towards the target.
        Returns True if the distance changed, or False if it didn't.
        """
        assert mover in self.positions, f"Mover {mover} is not in combat!"
        assert target in self.positions, f"Target {target} is not in combat!"

        start = self.positions[mover]
        end = self.positions[target]

        if start == end:
            # already as close as you can get
            return False

        change = 1 if start < end else -1
        self.positions[mover] += change

        return True

    def retreat(self, mover: 'BaseCharacter', target: 'BaseCharacter') -> bool:
        """
        Move a combatant away from the target.
        Returns True if the distance changed, or False if it didn't.
        """
        assert mover in self.positions, f"Mover {mover} is not in combat!"
        assert target in self.positions, f"Target {target} is not in combat!"

        start = self.positions[mover]
        end = self.positions[target]

        # can't move beyond maximum weapon range
        if abs(start - end) >= _MAX_RANGE:
            return False

        change = -1 if start < end else 1
        self.positions[mover] += change

        return True

    def _is_attack_blocked_or_parried(self, attacker, target, attack_type):
        """
        Handle attack being blocked or parried.
        """

        blocked = False
        parried = False
        range_to_target = self.get_range(attacker, target)
        # Check to see if the target is using a shield
        #   their Block zone matches the Attacker's target zone
        if target.shield is not None:
            blocked = True

        # Check if target is wielding something that can parry,
        #    and if their Parry zone matches the Attacker's target zone.
        if target.weapon is not None and target.weapon.can_parry():
            parried = True

        if blocked or parried:
            # See if target can defend
            target_defense_stamina_cost = self.rules.get_defense_stamina_cost(
                attacker,
                attack_type,
                attacker.weapon.stamina_cost,
                target
            )
            if target_defense_stamina_cost < target.stamina:
                target.spend_stamina(target_defense_stamina_cost)
                if range_to_target == CombatRange.MELEE:
                    attacker.cooldowns.add("attack", attacker.weapon.cooldown + 1)
                    target.buffs.add_buff("attack", 2, versus=attacker, duration=1)

                if blocked:
                    blocking_item = target.shield
                else:
                    blocking_item = target.weapon

                target.location.msg_contents(
                    "$You() $conj(block) the attack with $pron(your) {blocking_item}.",
                    mapping={"blocking_item": blocking_item},
                    from_obj=target,
                )
                return True
        return False


    def at_melee_attack(self, attacker, target):
        """
        Proceed with a melee attack.
        All validations should be done before this method.
        """
        weapon = attacker.weapon

        attacker_stamina_cost = self.rules.get_attack_stamina_cost(
            attacker,
            AttackType.MELEE,
            weapon.stamina_cost
        )
        attacker.spend_stamina(attacker_stamina_cost)
        attacker.cooldowns.add("attack", weapon.cooldown)

        if self._is_attack_blocked_or_parried(attacker, target, AttackType.MELEE):
            return 0

        attack_roll = rules.dice.roll("1d20") + attacker.get_ability(weapon.attack_type)
        if attack_roll >= target.armor + 10:
            damage = rules.dice.roll(weapon.damage_roll) + attacker.get_ability(weapon.attack_type)

            # multiply the result by the Attackers Aggression factor (round up)
            if attacker.aggro == "defensive":
                damage = int(damage / 2)
            elif attacker.aggro == "aggressive":
                damage = int(damage * 1.5)

            # Subtract off the Target's armor, if any.
            if target.armor:
                damage = damage - target.armor
                if damage <= 0:
                    attacker.location.msg_contents(
                        "$pron(your) attack fails to pierce {target}'s {armor}.",
                        mapping={"target": target, "armor": target.armor},
                        from_obj=attacker,
                    )
                    return 0

            # apply the remainder to the Targets Health
            attacker.location.msg_contents(
                "$You() $conj(hit) {target} with $pron(your) {weapon}.",
                mapping={"target": target, "weapon": weapon or "fists"},
                from_obj=attacker,
            )
            target.at_damage(damage, attacker)

            return damage

        target.location.msg_contents(
            "$You() $conj(dodge) the attack.",
            from_obj=target,
        )

        return 0

    def at_ranged_attack(self, attacker, target):
        """
        Proceed with a ranged attack.
        All validations should be done before this method.
        """

        weapon = attacker.weapon
        damage_roll = weapon.damage_roll
        stamina_cost = weapon.stamina_cost
        cooldown = weapon.cooldown

        attacker_stamina_cost = self.rules.get_attack_stamina_cost(
            attacker,
            AttackType.RANGED,
            stamina_cost
        )
        attacker.spend_stamina(attacker_stamina_cost)
        attacker.cooldowns.add("attack", cooldown)

        if self._is_attack_blocked_or_parried(attacker, target, AttackType.RANGED):
            return 0

        attack_roll = rules.dice.roll("1d20") + attacker.get_ability(weapon.attack_type)
        target_size_penalty = 0
        if self.in_range(attacker, target, CombatRange.SHORT_RANGE):
            range_penalty = 0
        else:
            # TODO Determine penalty
            range_penalty = 2

        defense_roll = 5 + target_size_penalty + range_penalty
        if attack_roll >= defense_roll:
            damage = rules.dice.roll(damage_roll)
            damage += attacker.strength

            # multiply the result by the Attackers Aggression factor (round up)
            if attacker.aggro == "defensive":
                damage = int(damage / 2)
            elif attacker.aggro == "aggressive":
                damage = int(damage * 1.5)

            # Subtract off the Target's armor, if any.
            if target.armor:
                damage = damage - target.armor
                if damage <= 0:
                    attacker.location.msg_contents(
                        "$pron(your) attack fails to pierce {target}'s {armor}.",
                        mapping={"target": target, "armor": target.armor},
                        from_obj=attacker,
                    )
                    return 0

            # apply the remainder to the Targets Health
            attacker.location.msg_contents(
                "$You() $conj(shoot) {target} with $pron(your) {weapon}.",
                mapping={"target": target, "weapon": weapon},
                from_obj=attacker,
            )
            target.at_damage(damage, attacker)

            return damage

        target.location.msg_contents(
            "$You() $conj(dodge) the attack.",
            from_obj=target,
        )

        return 0

    def at_thrown_attack(self, attacker, target):
        """
        Proceed with a thrown attack.
        All validations should be done before this method.
        """

        weapon = attacker.weapon
        damage_roll = weapon.damage_roll

        if attacker.weapon.is_throwable is not None:
            # set the Base Physical Damage Range to 1-2 and the Base Stamina Cost to 4.
            stamina_cost = 4
            cooldown = 4
        else:
            stamina_cost = weapon.stamina_cost
            cooldown = weapon.cooldown

        attacker_stamina_cost = self.rules.get_attack_stamina_cost(
            attacker,
            AttackType.THROWN,
            stamina_cost
        )
        attacker.spend_stamina(attacker_stamina_cost)
        attacker.cooldowns.add("attack", cooldown)

        if self._is_attack_blocked_or_parried(attacker, target, AttackType.THROWN):
            return 0

        attack_roll = rules.dice.roll("1d20") + attacker.get_ability(weapon.attack_type)
        target_size_penalty = 0
        if self.in_range(attacker, target, CombatRange.SHORT_RANGE):
            range_penalty = 0
        else:
            # TODO Determine penalty
            range_penalty = 2

        defense_roll = 5 + target_size_penalty + range_penalty
        if attack_roll >= defense_roll:
            damage = rules.dice.roll(damage_roll)
            damage += attacker.cunning

            # multiply the result by the Attackers Aggression factor (round up)
            if attacker.aggro == "defensive":
                damage = int(damage / 2)
            elif attacker.aggro == "aggressive":
                damage = int(damage * 1.5)

            # Subtract off the Target's armor, if any.
            if target.armor:
                damage = damage - target.armor
                if damage <= 0:
                    attacker.location.msg_contents(
                        "$pron(your) attack fails to pierce {target}'s {armor}.",
                        mapping={"target": target, "armor": target.armor},
                        from_obj=attacker,
                    )
                    return 0

            # apply the remainder to the Targets Health
            attacker.location.msg_contents(
                "$You() $conj(hit) {target} with $pron(your) thrown {weapon}.",
                mapping={"target": target, "weapon": weapon},
                from_obj=attacker,
            )
            target.at_damage(damage, attacker)

            return damage

        target.location.msg_contents(
            "$You() $conj(dodge) the attack.",
            from_obj=target,
        )
        return 0
