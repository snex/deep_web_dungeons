def node_start(caller, raw_string, **kwargs):
    options = [
        {"desc": "Buy","goto": ("node_show_buyable_items", kwargs)},
        {"desc": "Leave.", "goto": ("node_end", kwargs)}
    ]
    return raw_string, options

def node_end(caller, raw_string, **kwargs):
    return "Thanks for your business!", None

def node_show_buyable_items(caller, raw_string, **kwargs):
    text = "Buy somethin', will ya?"
    options = [
        {"desc": "Cancel.", "goto": ("node_start", kwargs)}
    ]
    return (text, ""), options
