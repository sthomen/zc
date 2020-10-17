#!/usr/bin/env python

from zc import MulticastListener
from zc.dns import Message

listener = MulticastListener().register('224.0.0.251', 5353)

while True:
	data, remote = listener.receive()
	print(f"Received packet from {remote}")
	print(Message(data))

listener.unregister()
