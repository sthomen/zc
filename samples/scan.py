#!/usr/bin/env python3.7

from zc import MulticastListener
from zc.dns import Message, Query, Record
from zc.dns.rr import RR
from zc.dns.util import b2address, b2ip, b2name

# Initializes RR plugins
rr = RR()
# Load the typemap, so we can easily get name -> number
typemap = rr.getTypeMap()

# Register for listening to mDNS
listener = MulticastListener().register('224.0.0.251', 5353)

# our query, are there any chromecasts out there?
query = Query() \
	.setLabels('_googlecast', '_tcp', 'local') \
	.setType(typemap.PTR)

# Create a message and add our question
question = Message()
question.addRecord(Message.QUESTION, query)

print("Sending query...")
listener.send(question)

print("Listening for replies...")
# Loop while the answers flood in (or not)
while True:

	# listener is derived from socket, so we can set a timeout
	listener.settimeout(1)

	data, remote = listener.receive()

	# timed out
	if data == None:
		break

	message = Message(data)

	# We're only looking for replies (this would otherwise try to parse our
	# question as well)
	if message.flags.qr:

		# load answer 0, this should match our query (PTR)
		answer = message.answer()

		if answer.type == typemap.PTR:
			print("Chromecast found at the address:")
			print(f"  {b2address(answer.rdata.target)}")
			print()
		else:
			print(f"Unexpected answer type {answer.type}")
			break

		if message.records[Message.ADDITIONAL]:
			print("Additionally, they tell us that:")

			for record in message.records[Message.ADDITIONAL]:
				if record.type == typemap.A:
					print("  The address is:")
					print(f"   {b2ip(record.rdata.address)}")
					print()

				elif record.type == typemap.TXT:
					print("  They have these properties:")
					for k,v in record.rdata.data.items():
						print(f'   {b2name(k)}: {b2name(v)}')
					print()

				elif record.type == typemap.SRV:
					print("  The service can be found here:")
					print(f"   {b2address(record.rdata.target)} port {record.rdata.port}")
					print(f"   weight: {record.rdata.weight}, priority: {record.rdata.priority}")
					print()
