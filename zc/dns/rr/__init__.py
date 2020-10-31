from .a import A
from .ns import NS
from .cname import CNAME
from .null import NULL
from .ptr import PTR
from .txt import TXT
from .aaaa import AAAA
from .srv import SRV

TYPE_A     = 1
TYPE_NS    = 2
TYPE_CNAME = 5
TYPE_NULL  = 10
TYPE_PTR   = 12
TYPE_TXT   = 16
TYPE_AAAA  = 28
TYPE_SRV   = 33
TYPE_ANY   = 255

mapping = {
	TYPE_A:     A,
	TYPE_NS:    NS,
	TYPE_CNAME: CNAME,
	TYPE_NULL:  NULL,
	TYPE_PTR:   PTR,
	TYPE_TXT:   TXT,
	TYPE_AAAA:  AAAA,
	TYPE_SRV:   SRV
}

def byType(type, raw, offset, length):
	rdata = None

	if type in mapping:
		rdata = mapping[type](raw, offset, length)

	return rdata
