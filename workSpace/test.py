import network
ap = network.WLAN(network.AP_IF)
sta = network.WLAN(network.STA_IF)

ap.config(essid='TangSmartHome', authmode=network.AUTH_WPA_WPA2_PSK, password="12345678")

import socket

s = socket.socket()
HOST = '0.0.0.0'
PORT = 80
httpHeader = b"""\
HTTP/1.0 200 OK

Welcome to MicroPython"!
"""

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)
print("Server running on port ", PORT)

while True:
    client, addr = s.accept()
    print("Client address:", addr)
    
    req = client.recv(1024)
    print("Request:")
    print(req)
    client.send(httpHeader)
    client.close()
    print('-----------------------')
