"""
Various utilities.

"""

import itertools

import inflect

from evennia.utils import ansi, evform, evtable

from world.enums import WieldLocation

_INFLECT = inflect.engine()

def obj_order(obj):
    """ display_name to sort it. """
    return str(obj)

def get_obj_stats(obj, owner=None):
    """
    Get a string of stats about the object.

    Args:
        obj: The object to get stats for.
        owner (optional): If given, it allows us to
            also get information about if the item is currently worn/wielded.

    Returns:
        str: A stat string to show about the object.

    """
    carried = ""
    carry_locs = {
        WieldLocation.BACKPACK: "carried in your backpack",
        WieldLocation.WEAPON_HAND: "currently wielded in your right hand",
        WieldLocation.SHIELD_HAND: "currently worn on your left hand",
        WieldLocation.TWO_HANDS: "currently wielded in both hands",
        WieldLocation.BODY: "currently worn",
        WieldLocation.HEAD: "currently worn on your head",
    }
    if owner:
        objmap = dict(owner.equipment.all())
        carried = objmap.get(obj)
        carried = f", {carry_locs[carried]}" if carried else ""

    obj_stats = evform.EvForm("world.itemdisplay")

    base_stats = evtable.EvTable(border=None)
    base_stats.add_row("|cWeight|n: ", obj.size)
    base_stats.add_row("|cQuality|n: ", obj.damage_level)
    item_type_stats = evtable.EvTable(border=None)
    item_stats = obj.get_item_type_stats(owner).items()

    if not item_stats:
        item_type_stats.add_row("--")
        item_type_stats.reformat_column(0, align="c")

    for stat, value in item_stats:
        item_type_stats.add_row(f"|c{stat}|n: ", value)

    header = f"""
{obj}{carried}
{obj.db.desc}
""".strip()

    obj_stats.map(
        cells={
            "1": evtable.EvCell(f"{header}", align="c")
        },
        tables={
            "2": base_stats,
            "3": item_type_stats,
        },
    )

    return str(obj_stats)

def get_numbered_name(name, count, **kwargs):
    """
    Return the numbered (singular, plural) forms of passed in name.
    Also the singular display version, such as 'an apple', 'a tree' is determined from this method.

    Args:
        name (str): The name to inflect
        count (int): Number of objects of this type

    Keyword Args:
        return_string (bool): If `True`, return only the singular form if count is 0,1 or
            the plural form otherwise. If `False` (default), return both forms as a tuple.
        no_article (bool): If `True`, do not return an article if `count` is 1.

    Returns:
        tuple: This is a tuple `(str, str)` with the singular and plural forms of the name
        including the count.

    Examples:
    ::

        get_numbered_name("foo", 3, looker)
              -> ("a foo", "three foos")
        get_numbered_name("Foobert", 1, return_string=True)
              -> "a Foobert"
        get_numbered_name("Foobert", 1, return_string=True, no_article=True)
              -> "Foobert"
    """
    raw_name = ansi.ANSIString(name)  # this is needed to allow inflection of colored names
    try:
        plural = _INFLECT.plural(raw_name, count)
        plural = f"{_INFLECT.number_to_words(count, threshold=12)} {plural}".strip()
    except IndexError:
        # this is raised by inflect if the input is not a proper noun
        plural = raw_name
    singular = _INFLECT.an(raw_name).strip()

    if kwargs.get("no_article") and count == 1:
        if kwargs.get("return_string"):
            return raw_name
        return raw_name, raw_name

    if kwargs.get("return_string"):
        if count == 1:
            return singular

        return plural

    return singular, plural

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
