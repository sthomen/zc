#!/usr/bin/env python3.7

from zc import MulticastListener
from zc.dns import Message, Query, Record, rr

# Register for listening to mDNS
listener = MulticastListener().register('224.0.0.251', 5353)

# our query, are there any chromecasts out there?
query = Query() \
	.setLabels(b'_googlecast', b'_tcp', b'local') \
	.setClass(Record.CLASS_IN) \
	.setType(rr.TYPE_PTR)

# Create a message and add our question
question = Message()
question.addRecord(Message.QUESTION, query)

listener.send(question)

# Loop while the answers flood in (or not)
while True:

	# listener is derived from socket, so we can set a timeout
	listener.settimeout(1)
	data, remote = listener.receive()

	# timed out
	if data == None:
		break

	print(f"--- START Packet from {remote}, {len(data)} bytes\n")
	message = Message(data)

	for section, records in message.records.items():
		print(f"Section: {section}")

		for record in records:
			print(record)

	print("\n--- END\n")
