#!/usr/bin/env python3.7

from zc import MulticastListener
from zc.dns import Message

listener = MulticastListener().register('224.0.0.251', 5353)

while True:
	data, remote = listener.receive()
	print(f"--- START Packet from {remote}, {len(data)} bytes\n")
	message = Message(data)

	for section, records in message.records.items():
		print(f"Section: {section}")

		for record in records:
			print(record)

	print("\n--- END\n")

listener.unregister()
