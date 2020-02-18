
import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

import os
import json

"""
file = open("defaultWiFi.json",'r') #讀取預設WIFI設定檔案
wifi = file.read()
file.close()
wifi = json.loads(wifi)
print(wifi)
"""
wlan.connect("TangiPhone", "0930082454")

while not sta.isconnected(): #等待連線完成
  print(".")
  time.sleep(0.3)
  pass
print(wlan.ifconfig())


