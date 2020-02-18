import socket
import network
import time

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect("SuperTang","0930082454")
while not sta.isconnected():
  pass
print(sta.ifconfig())

while True:
  wifidata = sta.scan()
  aps = ""
  #print(wifidata)
  for data in wifidata:
    aps = aps + str(data) + "|"
  s = socket.socket()
  s.connect(('122.116.200.218',36009))
  s.send("+CWLAP:"+str(aps))

  time.sleep(3)
  
