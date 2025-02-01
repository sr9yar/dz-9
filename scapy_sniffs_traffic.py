from scapy.all import * 

INTERFACE="en0"
packets = sniff(iface=INTERFACE, count=10)


for pac in packets:
  print(pac[0].show())


