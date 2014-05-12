import socket
import getnifs

nifs = getnifs.get_network_interfaces()
for ni in nifs:
	if ni.name == "lo":
		continue
	else:
		print ni.name
		print ni.addresses.get(socket.AF_INET) 

