import json
import time
import network
import ubinascii
from umqtt.simple import MQTTClient
from machine import Pin
import machine 
import os

WiFi_SSID = "SuperTang"
WiFi_PASS = "0930082454"
MQTT_Server = "192.168.1.112"
DeviceName = "主臥室燈"



machine.freq(160000000)
print(machine.freq()) #設定工作頻率

ap = network.WLAN(network.AP_IF)
ap.active(False)

sta = network.WLAN(network.STA_IF) #設定WiFi連線
sta.active(True)
sta.connect(WiFi_SSID,WiFi_PASS)

mac = ubinascii.hexlify(sta.config('mac'),':').decode()#取得MAC ADDRESS
print(mac)

while not sta.isconnected(): #等待連線完成
  print(".")
  time.sleep(0.3)
  pass
print(sta.ifconfig())


relay = Pin(4, Pin.OUT) #設定Pin為輸出模式
try:
  f=open('state.txt','r')
  relay.value(f.read())
  f.close()
  print(relay.value())
except:
  print('maybe first')

def sub_cb(topic, msg): # 收到訊息時處理
  msg_decode = msg.decode('utf8')
  msg_decode = json.loads(msg_decode) #資料前處理
  print((topic, msg))
  print(msg_decode['service_name'])
  
  if (msg_decode["service_name"] == DeviceName):
    light_state = 1 - relay.value()
    print(relay.value())
    relay.value(light_state) 
    f=open('state.txt','w')
    f.write(str(relay.value()))
    f.close()
  

def main(server=MQTT_Server):  #Connect to MQTT Server 
  print("waiting")
  
  c1 = MQTTClient("SuperTang" + mac, server)
  c1.set_callback(sub_cb)
  c1.connect()
  c1.subscribe(b"homebridge/from/set") #subscribe homebridge's Topic
  
  #c1.ping()
  
  while True:
    #c1.connect()
    #c1.subscribe(b"homebridge/from/set") #subscribe homebridge's Topic
      # Blocking wait for message
      #c1.connect()
      
      c1.wait_msg()
      # Non-blocking wait for message
      c1.check_msg()
      # Then need to sleep to avoid 100% CPU usage (in a real
      # app other useful actions would be performed instead)
      time.sleep(0.3)

  c1.disconnect()


try:
  main()
except:  
  print("ERROR....Reset...")
  machine.reset()










