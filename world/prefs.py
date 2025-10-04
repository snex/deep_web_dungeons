"""
Preferences menu.
"""

from evennia.utils.evmenu import EvMenu

_PREFS = {
    "look_on_enter": {
        "desc": "Whether or not to show the flavor text of a room upon entering.",
        "default": True
    }
}

def node_change_look_on_enter(caller, raw_string, **kwargs):
    """
    Change the user's preference for look_on_enter
    """

    caller.preferences["look_on_enter"] = not kwargs["current_val"]

    return node_display_prefs(caller, "")

def node_display_prefs(caller, raw_string, **kwargs):
    """
    Display user preferences as well as their values. Let the user select one
    if they want to change its value.
    """

    options = []

    for pref, details in _PREFS.items():
        val = details["default"]
        desc = details["desc"]

        if pref in caller.preferences:
            val = caller.preferences[pref]

        options.append(
            {
                "desc": f"{pref}: |w{val}|n\n {desc}\n",
                "goto": (f"node_change_{pref}", {"current_val": val, **kwargs})
            }
        )

        return (
            "Select a preference by number to change it, or type `quit` to go back.",
            ""
        ), options

def start_prefs(caller, _session=None):
    """
    This is a start point for running the user preferences menu.
    """
    menu_tree = {
        "node_display_prefs": node_display_prefs,
        "node_change_look_on_enter": node_change_look_on_enter
    }

    EvMenu(
        caller,
        menu_tree,
        startnode="node_display_prefs"
    )
