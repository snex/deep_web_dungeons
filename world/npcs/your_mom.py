"""
Your Mom is an example ShopKeeper NPC to show how the system works.
Probably don't spawn her in the game. Or do.
"""

def node_start(_caller, raw_string, **kwargs):
    """ Base of the shop menu. """
    options = [
        {"desc": "Buy","goto": ("node_show_buyable_items", kwargs)},
        {"desc": "Leave.", "goto": ("node_end", kwargs)}
    ]
    return raw_string, options

def node_end(_caller, raw_string, **kwargs):
    """ Close the shop menu. """
    return "Thanks for your business!", None

def node_show_buyable_items(_caller, raw_string, **kwargs):
    """ Show items Your Mom has for sale. """
    text = "Buy somethin', will ya?"
    options = [
        {"desc": "Cancel.", "goto": ("node_start", kwargs)}
    ]
    return (text, ""), options
