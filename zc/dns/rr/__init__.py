from .ptr import PTR
from .a import A
from .null import NULL
from .txt import TXT
from .aaaa import AAAA
from .srv import SRV

RTYPE_A     = 1
RTYPE_NS    = 2
RTYPE_CNAME = 5
RTYPE_NULL  = 10
RTYPE_PTR   = 12
RTYPE_TXT   = 16
RTYPE_AAAA  = 28
RTYPE_SRV   = 33

# NULL just reads the data of the RR into self.raw
mapping = {
	RTYPE_A:    A,
	RTYPE_NULL: NULL,
	RTYPE_AAAA: AAAA,
	RTYPE_PTR:  PTR,
	RTYPE_TXT:  TXT,
	RTYPE_SRV:  SRV
}

def getInstance(type, raw, offset, length):
	rdata = None

	if type in mapping:
		rdata = mapping[type](raw, offset, length)

	return rdata
