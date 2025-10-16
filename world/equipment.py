"""
Knave has a system of Slots for its inventory.

"""

from evennia import search_object, create_object
from evennia.utils.utils import inherits_from
from typeclasses.objects import Object, WeaponBareHands

from .enums import Ability, WieldLocation

class EquipmentError(TypeError):
    """ Error class to categorize errors thrown from here. """

class EquipmentHandler:
    """
    _Knave_ puts a lot of emphasis on the inventory. You have CON_DEFENSE inventory
    slots. Some things, like torches can fit multiple in one slot, other (like
    big weapons and armor) use more than one slot. The items carried and wielded has a big impact
    on character customization - even magic requires carrying a runestone per spell.

    The inventory also doubles as a measure of negative effects. Getting soaked in mud
    or slime could gunk up some of your inventory slots and make the items there unusuable
    until you clean them.

    """

    save_attribute = "inventory_slots"

    def __init__(self, obj):
        self.obj = obj
        self._load()

    def _empty_slots(self):
        return {
            WieldLocation.BACKPACK: [],
            WieldLocation.WEAPON_HAND: None,
            WieldLocation.SHIELD_HAND: None,
            WieldLocation.TWO_HANDS: None,
            WieldLocation.BODY: None,
            WieldLocation.HEAD: None,
        }

    def _load(self):
        """
        Load or create a new slot storage.

        """
        self.slots = self.obj.attributes.get(
            self.save_attribute,
            category="inventory",
            default=self._empty_slots()
        )

    def _save(self):
        """
        Save slot to storage.

        """
        self.obj.attributes.add(self.save_attribute, self.slots, category="inventory")

    def count_slots(self):
        """
        Count slot usage. This is fetched from the .size Attribute of the
        object. The size can also be partial slots.

        """
        slots = self.slots
        wield_usage = sum(
            getattr(slotobj, "size", 0) or 0
            for slot, slotobj in slots.items()
            if slot is not WieldLocation.BACKPACK
        )
        backpack_usage = sum(
            getattr(slotobj, "size", 0) or 0 for slotobj in slots[WieldLocation.BACKPACK]
        )
        return wield_usage + backpack_usage

    @property
    def max_slots(self):
        """
        The max amount of equipment slots ('carrying capacity') is based on strength.
        """
        return getattr(self.obj, Ability.STR.value, 1) + 10

    def validate_slot_usage(self, obj):
        """
        Check if obj can fit in equipment, based on its size.

        Args:
            obj (Object): The object to add.

        Raise:
            EquipmentError: If there's not enough room.

        """
        if not inherits_from(obj, Object):
            raise EquipmentError(f"{obj.key} is not something that can be equipped.")

        size = obj.size
        max_slots = self.max_slots
        current_slot_usage = self.count_slots()
        if current_slot_usage + size > max_slots:
            slots_left = max_slots - current_slot_usage
            raise EquipmentError(
                f"Equipment full ($int2str({slots_left}) slots "
                f"remaining, {obj.key} needs $int2str({size}) "
                f"$pluralize(slot, {size}))."
            )
        return True

    def get_current_slot(self, obj):
        """
        Check which slot-type the given object is in.

        Args:
            obj (Object): The object to check.

        Returns:
            WieldLocation: A location the object is in. None if the object
            is not in the inventory at all.

        """
        for equipment_item, slot in self.all():
            if obj == equipment_item:
                return slot

        return None

    @property
    def armor(self):
        """
        Armor provided by actually worn equipment/shield. For body armor
        this is a base value, like 12, for shield/helmet, it's a bonus, like +1.
        We treat values and bonuses equal and just add them up. This value
        can thus be 0, the 'unarmored' default should be handled by the calling
        method.

        Returns:
            int: Armor from equipment. Note that this is the +bonus of Armor, not the
                'defense' (to get that one adds 10).

        """
        slots = self.slots
        return sum(
            (
                # armor is listed using its defense, so we remove 10 from it
                # (11 is base no-armor value in Knave)
                getattr(slots[WieldLocation.BODY], "armor", 1),
                # shields and helmets are listed by their bonus to armor
                getattr(slots[WieldLocation.SHIELD_HAND], "armor", 0),
                getattr(slots[WieldLocation.HEAD], "armor", 0),
            )
        )

    def _get_bare_hands(self):
        """
        Get the bare hands weapon, using a universal db object.
        """

        bare_hands = search_object("Bare Hands", typeclass=WeaponBareHands).first()

        if not bare_hands:
            bare_hands = create_object(WeaponBareHands, key="Bare Hands")

        return bare_hands

    @property
    def weapon(self):
        """
        Conveniently get the currently active weapon.

        Returns:
            obj or None: The weapon. None if unarmored.

        """
        # first checks two-handed wield, then one-handed; the two
        # should never appear simultaneously anyhow (checked in `move` method).
        slots = self.slots
        weapon = slots[WieldLocation.TWO_HANDS]
        if not weapon:
            weapon = slots[WieldLocation.WEAPON_HAND]
        if not weapon:
            weapon = self._get_bare_hands()

        return weapon

    @property
    def shield(self):
        """ Return the currently active shield. """
        return self.slots[WieldLocation.SHIELD_HAND]

    @property
    def armor_item(self):
        """ Return the currently worn armor. """
        return self.slots[WieldLocation.BODY]

    @property
    def  helmet(self):
        """ Return the currently worn helmet. """
        return self.slots[WieldLocation.HEAD]

    def display_loadout(self):
        """
        Get a visual representation of your current loadout.

        Returns:
            str: The current loadout.

        """
        slots = self.slots
        weapon_str = "You are fighting with your |xbare fists|n"
        shield_str = " and have no shield."
        armor_str = "You wear no armor"
        helmet_str = " and no helmet."

        two_hands = slots[WieldLocation.TWO_HANDS]
        if two_hands:
            weapon_str = f"You wield {two_hands.get_display_name()} with both hands."
            shield_str = ""
        else:
            one_hands = slots[WieldLocation.WEAPON_HAND]
            if one_hands:
                weapon_str = f"You are wielding {one_hands.get_display_name()} in one hand."
            shield = slots[WieldLocation.SHIELD_HAND]
            if shield:
                shield_str = f" You have {shield.get_display_name()} in your off hand."

        armor = slots[WieldLocation.BODY]
        if armor:
            armor_str = f"You are wearing {armor.get_display_name()}"

        helmet = slots[WieldLocation.HEAD]
        if helmet:
            helmet_str = f" and {helmet.get_display_name()} on your head."

        return f"{weapon_str}{shield_str}\n{armor_str}{helmet_str}"

    def _obj_order(self, obj):
        """ Use the object's key to sort it in the backpack display. """
        return obj.key

    def display_backpack(self):
        """
        Get a visual representation of the backpack's contents.

        """
        backpack = sorted(self.slots[WieldLocation.BACKPACK], key=self._obj_order)
        if not backpack:
            return "Backpack is empty."
        out = []
        for item in backpack:
            out.append(f"{item.get_display_name()} [|b{item.size}|n] slot(s)")
        return "\n".join(out)

    def display_slot_usage(self):
        """
        Get a slot usage/max string for display.

        Returns:
            str: The usage string.

        """
        return f"|b{round(self.count_slots(), 2)}/{self.max_slots}|n"

    def move(self, obj):
        """
        Moves item to the place it thinks it should be in - this makes use of the object's wield
        slot to decide where it goes. The item is assumed to already be in the backpack.

        Args:
            obj (Object): Thing to use.

        Raises:
            EquipmentError: If there's no room in inventory. It will contains the details
                of the error, suitable to echo to user.

        Notes:
            This will cleanly move any 'colliding' items to the backpack to
            make the use possible (such as moving sword + shield to backpack when wielding
            a two-handed weapon). If wanting to warn the user about this, it needs to happen
            before this call.

        """
        # make sure to remove from backpack first, if it's there, since we'll be re-adding it
        self.remove(obj)

        self.validate_slot_usage(obj)
        slots = self.slots
        use_slot = getattr(obj, "inventory_use_slot", WieldLocation.BACKPACK)

        to_backpack = []
        if use_slot is WieldLocation.TWO_HANDS:
            # two-handed weapons can't co-exist with weapon/shield-hand used items
            to_backpack = [slots[WieldLocation.WEAPON_HAND], slots[WieldLocation.SHIELD_HAND]]
            slots[WieldLocation.WEAPON_HAND] = slots[WieldLocation.SHIELD_HAND] = None
            slots[use_slot] = obj
        elif use_slot in (WieldLocation.WEAPON_HAND, WieldLocation.SHIELD_HAND):
            # can't keep a two-handed weapon if adding a one-handed weapon or shield
            to_backpack = [slots[WieldLocation.TWO_HANDS]]
            slots[WieldLocation.TWO_HANDS] = None
            slots[use_slot] = obj
        elif use_slot is WieldLocation.BACKPACK:
            # it belongs in backpack, so goes back to it
            to_backpack = [obj]
        else:
            # for others (body, head), just replace whatever's there and put the old
            # thing in the backpack
            to_backpack = [slots[use_slot]]
            slots[use_slot] = obj

        for to_backpack_obj in to_backpack:
            # put stuff in backpack
            if to_backpack_obj:
                slots[WieldLocation.BACKPACK].append(to_backpack_obj)

        # store new state
        self._save()

    def add(self, obj):
        """
        Put something in the backpack specifically (even if it could be wield/worn).

        Args:
            obj (Object): The object to add.

        Notes:
            This will not change the object's `.location`, this must be done
            by the calling code.

        """
        # check if we have room
        self.validate_slot_usage(obj)
        self.slots[WieldLocation.BACKPACK].append(obj)
        self._save()

    def remove(self, obj_or_slot):
        """
        Remove specific object or objects from a slot.

        Args:
            obj_or_slot (Object or WieldLocation): The specific object or
                location to empty. If this is WieldLocation.BACKPACK, all items
                in the backpack will be emptied and returned!
        Returns:
            list: A list of 0, 1 or more objects emptied from the inventory.

        Notes:
            This will not change the object's `.location`, this must be done separately
            by the calling code.

        """
        slots = self.slots
        ret = []
        if isinstance(obj_or_slot, WieldLocation):
            if obj_or_slot is WieldLocation.BACKPACK:
                # empty entire backpack
                ret.extend(slots[obj_or_slot])
                slots[obj_or_slot] = []
            else:
                ret.append(slots[obj_or_slot])
                slots[obj_or_slot] = None
        elif obj_or_slot in self.slots.values():
            # obj in use/wear slot
            for slot, objslot in slots.items():
                if objslot is obj_or_slot:
                    slots[slot] = None
                    ret.append(objslot)
        elif obj_or_slot in slots[WieldLocation.BACKPACK]:
            # obj in backpack slot
            try:
                slots[WieldLocation.BACKPACK].remove(obj_or_slot)
                ret.append(obj_or_slot)
            except ValueError:
                pass
        if ret:
            self._save()
        return ret

    def get_wieldable_objects_from_backpack(self):
        """
        Get all wieldable weapons (or spell runes) from backpack. This is useful in order to
        have a list to select from when swapping your wielded loadout.

        Returns:
            list: A list of objects with a suitable `inventory_use_slot`. We don't check
            quality, so this may include broken items (we may want to visually show them
            in the list after all).

        """
        return [
            obj
            for obj in self.slots[WieldLocation.BACKPACK]
            if obj.inventory_use_slot
            in (WieldLocation.WEAPON_HAND, WieldLocation.TWO_HANDS, WieldLocation.SHIELD_HAND)
        ]

    def get_wearable_objects_from_backpack(self):
        """
        Get all wearable items (armor or helmets) from backpack. This is useful in order to
        have a list to select from when swapping your worn loadout.

        Returns:
            list: A list of objects with a suitable `inventory_use_slot`. We don't check
            quality, so this may include broken items (we may want to visually show them
            in the list after all).

        """
        return [
            obj
            for obj in self.slots[WieldLocation.BACKPACK]
            if obj.inventory_use_slot in (WieldLocation.BODY, WieldLocation.HEAD)
        ]

    def get_usable_objects_from_backpack(self):
        """
        Get all 'usable' items (like potions) from backpack. This is useful for getting a
        list to select from.

        Returns:
            list: A list of objects that are usable.

        """
        character = self.obj
        return [obj for obj in self.slots[WieldLocation.BACKPACK] if obj.at_pre_use(character)]

    def all(self, only_objs=False):
        """
        Get all objects in inventory, regardless of location.

        Keyword Args:
            only_objs (bool): Only return a flat list of objects, not tuples.

        Returns:
            list: A list of item tuples `[(item, WieldLocation),...]`
            starting with the wielded ones, backpack content last. If `only_objs` is set,
            this will just be a flat list of objects.

        """
        slots = self.slots
        lst = [
            (slots[WieldLocation.WEAPON_HAND], WieldLocation.WEAPON_HAND),
            (slots[WieldLocation.SHIELD_HAND], WieldLocation.SHIELD_HAND),
            (slots[WieldLocation.TWO_HANDS], WieldLocation.TWO_HANDS),
            (slots[WieldLocation.BODY], WieldLocation.BODY),
            (slots[WieldLocation.HEAD], WieldLocation.HEAD),
        ] + [(item, WieldLocation.BACKPACK) for item in slots[WieldLocation.BACKPACK]]
        if only_objs:
            # remove any None-results from empty slots
            return [tup[0] for tup in lst if tup[0]]
        # keep empty slots
        return list(lst)
