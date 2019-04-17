# -*- coding: utf-8 -*-

"""
  程式說明請參閱18-33頁
"""
from umqtt.robust import MQTTClient
import time
import network
WiFi_SSID = "5678"
WiFi_PASS = ""
MQTT_Server = "192.168.0.199"
DeviceName = "測試開關"
sta = network.WLAN(network.STA_IF) #設定WiFi連線
sta.active(True)
sta.connect(WiFi_SSID,WiFi_PASS)
while not sta.isconnected(): #等待連線完成
  pass
print(sta.ifconfig())
def sub_cb(topic, msg):
  print((topic, msg))
  
c = MQTTClient("umqtt_client", MQTT_Server)
c.DEBUG = True
c.set_callback(sub_cb)


if not c.connect(clean_session=False):
  print("New session being set up")
  c.subscribe(b"homebridge/from/set")

while 1:
  c.wait_msg()

c.disconnect()
