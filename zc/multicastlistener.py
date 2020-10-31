import socket

class MulticastListener(socket.socket):
	"""
	Multicast listener
	"""
	def __init__(self, reuse = True):
		socket.socket.__init__(self, socket.AF_INET, socket.SOCK_DGRAM)

		if (reuse):
			self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			if hasattr(socket, "SO_REUSEPORT"):
				self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

		self.mcast_addr = None

	def guessmyip(self):
		"""
		Guess the local address to use for receiving multicast packets

		"""
		return socket.gethostbyname(socket.gethostname())

	def register(self, addr, port, local = None):
		"""
		Register to listen for multicast packets

		Addresses are in dotted quad
		The maximum packet length comes from socket.recvfrom() needing a length

		:param addr str: Address of the multicast group to join
		:param port int: Multicast port
		:param local str: Local address
		"""
		if not local:
			local = self.guessmyip()

		self.bind(('', port))

		self.setsockopt(
			socket.SOL_IP,
			socket.IP_ADD_MEMBERSHIP,
			socket.inet_aton(addr) + socket.inet_aton(local)
		)

		# Linux doesn't require this to be set, but BSD systems seem
		# to need to know the interface (address) to use to send packets
		# from
		self.setsockopt(
			socket.IPPROTO_IP,
			socket.IP_MULTICAST_IF,
			socket.inet_aton(local)
		)

		# Store this for later
		self.mcast_addr = (addr, port)

		return self

	def receive(self, length = 9000):
		"""
		Receive a single multicast packet, this method blocks until a packet
		has been received.

		:param length int: Maximum packet length to listen for
		"""
		if not self.mcast_addr:
			raise IllegalState("Attempted to listen before registering")

		data, remote_addr = self.recvfrom(length)
		return (data, remote_addr)

	def send(self, message):
		"""
		Send a multicast packet

		:param message bytes: The packet to send
		"""
		if not self.mcast_addr:
			raise IllegalState("Attempted to send before registering")

		self.sendto(message, self.mcast_addr)

	def unregister(self):
		"""
		Unregister from the current multicast group
		"""

		if not self.mcast_addr:
			raise IllegalState("Attempted to unregister before registering")

		self.setsockopt(
			socket.SOL_IP,
			socket.IP_ADD_MEMBERSHIP,
			socket.inet_aton(self.addr) + socket.inet_aton('0.0.0.0')
		)

		self.mcast_addr = None

		return self

class IllegalState(RuntimeError):
	pass
