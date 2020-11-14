from .rrplugin import RRPlugin as RR

# The plug-in system works fine when the plugin files are loaded from a path in
# the current project, but when it's a question of bundled plugins like these,
# we can't just look for files to import. Thus they must all be individually
# imported, so we can have the plugin system just do the equivalent of
# `from path import *`
#
# User, this is not for you. Use RRPlugin to instantiate plugins (or let
# Message do it for you).

from .a import A
from .aaaa import AAAA
from .cname import CNAME
from .ns import NS
from .null import NULL
from .ptr import PTR
from .srv import SRV
from .txt import TXT
