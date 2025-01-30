from scapy.all import * 

# INTERFACE="en0"
# packets = sniff(iface=INTERFACE, count=20)
# print(packets[0].show())



DOMAIN="google-gruyere.appspot.com"
INSTANCE_ID="472666335020487989751201647380414278590"
PATH=f"/{INSTANCE_ID}"

syn = IP(dst=DOMAIN) / TCP(dport=443, flags="S")
syn_ack = sr1(syn)
get_str = f"GET {PATH} HTTP/1.1\r\nHost: {DOMAIN}\r\n\r\n"
request = IP(dst=DOMAIN) /  TCP(dport=443,
                            sport=syn_ack[TCP].dport,
                            seq=syn_ack[TCP].ack,
                            ack=syn_ack[TCP].seq + 1,
                            flags="A") / get_str
reply = sr1(request)

print(reply.show())
