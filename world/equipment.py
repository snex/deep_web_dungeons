"""
Knave has a system of Slots for its inventory.

"""

import itertools

from evennia import search_object, create_object
from evennia.utils.utils import inherits_from
from typeclasses.objects import Object, NoneObject, WeaponBareHands

from .enums import Ability, WieldLocation
from .utils import obj_order

class EquipmentError(TypeError):
    """ Error class to categorize errors thrown from here. """

class BackpackHandler:
    """ class to handle all backpack operations """
    def __init__(self, backpack, equipment_handler):
        self._backpack = backpack
        self.eq = equipment_handler

    def __contains__(self, item):
        return item in self._backpack

    def __iter__(self):
        return iter(self._backpack)

    def __eq__(self, other):
        return self._backpack == other

    def append(self, item):
        """ add item to backpack """
        self._backpack.append(item)

    def remove(self, item):
        """ remove item from backpack """
        self._backpack.remove(item)

    @property
    def usage(self):
        """ return the weight of all items in the backpack """
        return sum(getattr(obj, "size", 0) or 0 for obj in self._backpack)

    def sorted_backpack(self, typeclass=Object):
        """
        returns contents of the backpack sorted by key, inheriting from typeclass, so they can be
          presented for sale

        contents is an array of the objects themselves
        """
        return [
            item
            for item in sorted(self._backpack, key=obj_order)
            if inherits_from(item, typeclass)
        ]

    def organized_backpack(self):
        """
        return contents of the backpack sorted by key and collated by quantity and weight

        contents is a dict in the following format:
            {
                "item_display_name": {
                    "capacity": TOTAL_CAPACITY_OF_THIS_ITEM,
                    "quantity": TOTAL_QUANTITY_OF_THIS_ITEM,
                }
            }
        """
        backpack = self.sorted_backpack()
        if not backpack:
            return {}

        ret = {}

        for item in backpack:
            k = str(item)

            if k in ret:
                ret[k]["capacity"] += item.size
                ret[k]["quantity"] += 1
            else:
                ret[k] = {
                    "capacity": item.size,
                    "quantity": 1,
                }

        return ret

    def paged_backpack(self, page=1, per_page=24):
        """
        get the `page` page of the sorted backpack contents,
            with a maximum of `per_page` items per page

        Args: page - which page of the backpack to return. if NaN or < 1, return page 1
                     if > total pages, return the last page
              per_page - number of items per page. defaults to 24 to fit the inventory command

        Returns a tuple containing the page, the total pages, and an array of tuples with the items
        """

        try:
            per_page = int(per_page)
        except ValueError:
            per_page = 24

        backpack = self.organized_backpack()
        total_pages = max(1, (len(backpack.keys()) -1) // per_page + 1)

        try:
            page = min(total_pages, max(1, int(page)))
        except ValueError:
            page = 1

        start_idx = (page - 1) * per_page
        return (
            page,
            total_pages,
            list(itertools.islice(backpack.items(), start_idx, start_idx + per_page))
        )

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
            for obj in self._backpack
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
            for obj in self._backpack
            if obj.inventory_use_slot in (WieldLocation.BODY, WieldLocation.HEAD)
        ]

    def get_usable_objects_from_backpack(self):
        """
        Get all 'usable' items (like potions) from backpack. This is useful for getting a
        list to select from. Requires a character to be sent in as an arg because objects
        are usable FOR characters, not just in general.

        Returns:
            list: A list of objects that are usable.

        """
        character = self.eq.obj
        return [obj for obj in self._backpack if obj.at_pre_use(character)]

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
        self._backpack = BackpackHandler(self.slots[WieldLocation.BACKPACK], self)
        self.backpack_methods = [f for f in dir(BackpackHandler) if not f.startswith('_')]

    def __getattr__(self, func):
        def method(*args, **kwargs):
            if func in self.backpack_methods:
                return getattr(self._backpack, func)(*args, **kwargs)
            raise AttributeError
        return method

    @property
    def backpack(self):
        """ return the backpack contents """
        return self._backpack

    def _empty_slots(self):
        return {
            WieldLocation.BACKPACK: [],
            WieldLocation.WEAPON_HAND: NoneObject(),
            WieldLocation.SHIELD_HAND: NoneObject(),
            WieldLocation.TWO_HANDS: NoneObject(),
            WieldLocation.BODY: NoneObject(),
            WieldLocation.HEAD: NoneObject(),
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
        return wield_usage + self.backpack.usage

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
            obj or NoneObject: The weapon. None if unarmored.

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
        return self.slots[WieldLocation.SHIELD_HAND] or NoneObject()

    @property
    def armor_item(self):
        """ Return the currently worn armor. """
        return self.slots[WieldLocation.BODY] or NoneObject()

    @property
    def helmet(self):
        """ Return the currently worn helmet. """
        return self.slots[WieldLocation.HEAD] or NoneObject()

    def display_loadout(self):
        """ displays the loadout for use with the `look` command """

        l_hand = "None"
        if self.weapon.inventory_use_slot == WieldLocation.TWO_HANDS:
            l_hand = self.weapon
        if self.shield:
            l_hand = self.shield
        return f"""
Right Hand: {self.weapon}
Left Hand: {l_hand}
Body: {self.armor_item}
Head: {self.helmet}
""".strip()

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
            slots[WieldLocation.WEAPON_HAND] = slots[WieldLocation.SHIELD_HAND] = NoneObject()
            slots[use_slot] = obj
        elif use_slot in (WieldLocation.WEAPON_HAND, WieldLocation.SHIELD_HAND):
            # can't keep a two-handed weapon if adding a one-handed weapon or shield
            to_backpack = [slots[WieldLocation.TWO_HANDS]]
            slots[WieldLocation.TWO_HANDS] = NoneObject()
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
                self.backpack.append(to_backpack_obj)

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
        self.backpack.append(obj)
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
                slots[obj_or_slot] = NoneObject()
        elif obj_or_slot in self.slots.values():
            # obj in use/wear slot
            for slot, objslot in slots.items():
                if objslot is obj_or_slot:
                    slots[slot] = NoneObject()
                    ret.append(objslot)
        elif obj_or_slot in self.backpack:
            # obj in backpack slot
            try:
                self.backpack.remove(obj_or_slot)
                ret.append(obj_or_slot)
            except ValueError:
                pass
        if ret:
            self._save()
        return ret

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
            (slots[WieldLocation.WEAPON_HAND] or NoneObject(), WieldLocation.WEAPON_HAND),
            (slots[WieldLocation.SHIELD_HAND] or NoneObject(), WieldLocation.SHIELD_HAND),
            (slots[WieldLocation.TWO_HANDS] or NoneObject(), WieldLocation.TWO_HANDS),
            (slots[WieldLocation.BODY] or NoneObject(), WieldLocation.BODY),
            (slots[WieldLocation.HEAD] or NoneObject(), WieldLocation.HEAD),
        ] + [(item, WieldLocation.BACKPACK) for item in self.backpack]
        if only_objs:
            # remove any None-results from empty slots
            return [tup[0] for tup in lst if tup[0]]
        # keep empty slots
        return list(lst)
