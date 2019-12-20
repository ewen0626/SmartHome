# -*- coding: utf-8 -*-
from machine import UART
import time
import network
import ubinascii
wlan=network.WLAN(network.STA_IF)
wlan.active(True)       #掃描附近無線基地台
i =0

com = UART(1, 115200,tx=2,rx=15)
com.init(115200)

while i<5:
  com.write("AT\r\n")
  time.sleep(1)
  com.write("AT+CIPMODE=1\r\n")
  time.sleep(1)
  com.write("AT+NETOPEN\r\n")
  time.sleep(1)
  com.write('AT+CIPOPEN=0,"TCP","122.116.200.218",36021\r\n')
  time.sleep(1)
  i = i+1

while True:
  wifidata = ""
  mac = ""
  aps=wlan.scan() 
  #掃描附近無線基地台
  for data in aps:
    mac=ubinascii.hexlify(data[1], ':').decode()
    data = list(data)
    data[1] = mac
    data[2] = data[3]
    wifidata = wifidata + "+CWLAP:" + str(data)
  print(wifidata)
  com.write(wifidata)
  #com.write("\r\n")
  time.sleep(3)
  


