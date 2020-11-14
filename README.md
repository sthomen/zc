# zc

This is a library for interfacing with mDNS. It's intent is to be much simpler
than the only other one I found, zeroconf, which spins off its own listening
threads and is fairly cryptic.

I mainly wrote this as a fun project exploring mDNS, but it might be useful
to someone. If you wish to use it, feel free! I would appreciate credits if
you do, or perhaps send me a line telling me about your project. Patches are
also welcome, but keep in mind that I have a day job and can't always respond
quickly.

## Usage

The library has two major components, the increasinly misnamed MulticastListener
class directly available `from zc` and the dns message component. The former is
for doing the actual sending of messages as it is derived from the socket class
and the second is for decoding and encoding messages that you want to send.

In general I tend to favor builder-style classes, so a fair number of the 
constructing" methods return self so that they can be used in this fashion.

### Multicast

To listen for multicast messages, all you need is a listener

```
from zc import MulticastListener

listener = MulticastListener()
```

and then use `register` to listen to the right group and port

```
listener.register('224.0.0.251', 5353)
```

You can now tell the listener to listen for a packet:

```
data, remote = listener.receive()
```

The receive method will block until a message is received and then continue.
If you don't want to wait forever, you can set the listener to time out after
a second by doing this before calling `receive`.

```
listener.settimeout(1)
```

If no packet was receive within the time you set, the first element of the
returned tuple will be set to `None`. Note that the settimeout here is
inherited from socket. The MulticastListener is a socket.

### DNS

DNS is a very old protocol and has a lot of features, this module is not
intended to be a complete implementation, but instead be basic and extensible.

Multicast DNS uses the same wire format as the regular DNS, and here it starts
with the `zc.dns.Message` class.

The Message class represent the entire DNS message, it contains:

 - a query ID (16 bit integer)
 - some flags (`zc.dns.Flags`)

...and any number of records, grouped by sections (the count of items in each
section are in the header, but Message abstracts that away when decoding and
encoding). The various sections have differing names in the RFC:s, but I call
them (in order):

 - Question (Message.QUESTION)
 - Answer (Message.ANSWER)
 - NS (Message.NS)
 - Additional (Message.ADDITIONAL)

Each record in these sections is either a Query or a Resource Record. Normally
Query type records are in the Question section. When Message parses the header
however, it will only look at the QR flag (indicating that it is a response)
wheter or not to read the payload as Query or Record objects, regardless of
section.

#### Query records

`zc.dns.Query` records are fairly simple, they only have a label (sometime
refered to as a name in the documentation) a type indicating what is being
asked for and a class which invariably is 1 (indicating Internet, "IN", names).

#### Resouce Records

`.zc.dns.Record` items are more complex, they are like Query records in that
they too contain a label (name), type and class but also have a TTL, rdlength
and a variable length rdata field (record data, the length indicated by
rdlength) which holds the actual resource information, and is indicated by the
type value.

Record will automatically decode this field into the right rdata type, if it's
known, otherwise it will just store the raw data there.

##### Plugins

The module uses a plugin system for locating and instantiating rdata objects,
and can be extended dynamically by instantiating `zc.dns.rr.RRPlugin` and adding
your custom plugin search path to it with `addPath()` as a python class
prefix (my.module.path.here). The plugin system expects to find these plugins
in the path ./my/module/path/here and will import all the .py files there.

Added plugins can be loaded by calling `refresh()` on the RRPlugin instance,
this will be done automatically when addPath is called.

Plugin classes are discovered by decorating them with `@RRPlugin.register(type=N)`.
where N is the type number found in the resource record header. You can also
name them by adding the name="name" parameter to the decorator, otherwise the
class name is used.

This bit is still very experimental and may not work reliably.
