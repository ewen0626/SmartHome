import json
import time
import network
import ubinascii
from umqtt.simple import MQTTClient
from machine import Pin
import machine 

WiFi_SSID = "5678"
WiFi_PASS = ""
MQTT_Server = "192.168.0.192"
DeviceName = "測試開關1"



machine.freq(160000000)
print(machine.freq()) #設定工作頻率


sta = network.WLAN(network.STA_IF) #設定WiFi連線
mac = ubinascii.hexlify(sta.config('mac'),':').decode()#取得MAC ADDRESS
sta.active(True)
sta.connect(WiFi_SSID,WiFi_PASS)
print(mac)

while not sta.isconnected(): #等待連線完成
  pass
print(sta.ifconfig())


relay = Pin(2, Pin.OUT) #設定Pin為輸出模式

def sub_cb(topic, msg): # 收到訊息時處理
  msg_decode = msg.decode('utf8')
  msg_decode = json.loads(msg_decode) #資料前處理
  print((topic, msg))
  print(msg_decode['service_name'])
  
  if msg_decode["service_name"] == DeviceName:
    light_state = 1 - relay.value()
    relay.value(light_state)
  
  

def main(server=MQTT_Server):  #Connect to MQTT Server 
  c1 = MQTTClient("SuperTang" + mac, server)
  c1.set_callback(sub_cb)
  c1.connect()
  c1.subscribe(b"homebridge/from/set") #subscribe homebridge's Topic
  
  
  while True:
    if True:
      # Blocking wait for message
      c1.wait_msg()

    else:
      # Non-blocking wait for message
      c1.check_msg()
      # Then need to sleep to avoid 100% CPU usage (in a real
      # app other useful actions would be performed instead)
      time.sleep(0.1)

  c1.disconnect()

if __name__ == "__main__":
  main()








