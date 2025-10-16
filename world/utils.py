"""
Various utilities.

"""

import itertools

_OBJ_STATS = """
{display_name}{carried}

{desc}

Slots: |w{size}|n, Used from: |w{use_slot_name}|n
Quality: |w{quality}|n, Uses: |w{uses}|n
Attacks using |w{attack_type_name}|n against |w{defense_type_name}|n
"""


def get_obj_stats(obj, owner=None):
    """
    Get a string of stats about the object.

    Args:
        obj (EvAdventureObject): The object to get stats for.
        owner (EvAdventureCharacter, optional): If given, it allows us to
            also get information about if the item is currently worn/wielded.

    Returns:
        str: A stat string to show about the object.

    """
    carried = ""
    if owner:
        objmap = dict(owner.equipment.all())
        carried = objmap.get(obj)
        carried = f", Worn: [{carried.value}]" if carried else ""

    attack_type = getattr(obj, "attack_type", None)
    defense_type = getattr(obj, "defense_type", None)

    return _OBJ_STATS.format(
        display_name=obj.get_display_name(owner),
        value=obj.value,
        carried=carried,
        desc=obj.db.desc,
        size=obj.size,
        use_slot_name=obj.inventory_use_slot.value,
        quality=getattr(obj, "quality", "N/A"),
        uses=getattr(obj, "uses", "N/A"),
        attack_type_name=attack_type.value if attack_type else "No attack",
        defense_type_name=defense_type.value if defense_type else "No defense",
        damage_roll=getattr(obj, "damage_roll", "None"),
    )

def each_cons(iterable, n):
    """
    Returns a list of size n lists of consecutive values of the original list.

    Similar to ruby's `each_cons`
    """

    return [iterable[i:i+n] for i in range(len(iterable)-n+1)]

def each_slice(iterable, size):
    """
    Returns a list of size n lists of sub-lists of the original list.

    Similar to ruby's `each_slice`
    """

    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]

def list_flatten(iterable):
    """
    Flattens a list of lists so that it is only the original items.

    e.g. list_flatten([[1, 2], [3, 4]]) -> [1, 2, 3, 4]

    Similar to ruby's `flatten` but will only do 1 layer deep and requires all items to be lists
    """

    return [item for items in iterable for item in items]

def rainbow(text):
    """ Apply a rainbow color effect to the input text. """

    colors = ["|r", "|530", "|y", "|g", "|b", "|c", "|m"]
    return "".join(list_flatten(list(zip(itertools.cycle(colors), list(text))))) + "|n"
