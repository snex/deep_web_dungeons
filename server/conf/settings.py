r"""
Evennia settings file.
"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "Deep Web Dungeons"
SERVER_HOSTNAME = "deep-web-dungeons.i2p"
GAME_SLOGAN = "Dive into the Deep Web Dungeons!"
WEBCLIENT_ENABLED = False
IN_GAME_ERRORS = False
BROADCAST_SERVER_RESTART_MESSAGES = False

# Multiple characters per account, requires manual creation and login
MULTISESSION_MODE = 2
AUTO_CREATE_CHARACTER_WITH_ACCOUNT = False
AUTO_PUPPET_ON_LOGIN = False
MAX_NR_CHARACTERS = 5

FILE_HELP_ENTRY_MODULES = [ 'world.help.combat_help' ]
BASE_CHARACTER_TYPECLASS = "typeclasses.characters.Character"


######################################################################
# XYZ Grid install settings
######################################################################

# make contrib prototypes available as parents for map nodes
PROTOTYPE_MODULES += [
    'evennia.contrib.grid.xyzgrid.prototypes',
    'world.overworld.prototypes',
    'world.common.item_prototypes',
    'world.common.mob_prototypes',
    'world.common.room_prototypes',
]

# add launcher command
EXTRA_LAUNCHER_COMMANDS['xyzgrid'] = 'evennia.contrib.grid.xyzgrid.launchcmd.xyzcommand'

# add game-specific maps
XYZGRID_MAP_LIST = [
    'world.maps.riverport',
    ]

######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
