"""
{"name":"測試溫度","characteristic":"CurrentTemperature","value":18}
{"name": "客廳濕度", "service_name": "客廳濕度", "characteristic": "CurrentRelativeHumidity", "value": 85}
"""
from machine import Pin
from umqtt.simple import MQTTClient
import dht
import json
import time
import machine
import network
import ubinascii

WiFi_SSID = "SuperTang"
WiFi_PASS = ""
MQTT_Server = "192.168.1.112"
DeviceName_temp = "客廳溫度"
DeviceName_hum = "客廳濕度"
data = {}
ap = network.WLAN(network.AP_IF)
ap.active(False)
sta = network.WLAN(network.STA_IF) #設定WiFi連線
sta.active(True)
sta.connect(WiFi_SSID,WiFi_PASS)
mac = ubinascii.hexlify(sta.config('mac'),':').decode()#取得ADDRESS
print(mac)
while not sta.isconnected():
  time.sleep(0.3)
  print(".")
  pass
print(sta.ifconfig())


d = dht.DHT22(Pin(5))

rtc = machine.RTC()
rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
rtc.alarm(rtc.ALARM0, 20000)

time.sleep(2)


try:
  d.measure()
  time.sleep_ms(50)
  temp = d.temperature()
  hum = d.humidity()
  data_temp['name'] = DeviceName_temp
  data_temp['characteristic'] = 'CurrentTemperature'
  data_temp['value'] = temp
  data_temp = json.dumps(data_temp)
  
  data_hum['name'] = DeviceName_hum
  data_hum['characteristic'] = 'CurrentRelativeHumidity'
  data_hum['value'] = hum
  data_hum = json.dumps(data_hum) 
  
  print(data)
  print("----------------------------")
  print('Humidity: {}%'.format(hum))
  print('Temperature: {}{}C'.format(temp, '\u00b0'))
  print("----------------------------")


  c = MQTTClient("SuperTang" + mac, MQTT_Server)
  c.connect()
  c.publish(b"homebridge/to/set", data_hum)
  c.publish(b"homebridge/to/set", data_temp)

  c.disconnect()
  print("published!")
except:
  
  print("ERROR")

time.sleep(1)
print("GO TO SLEEP")
machine.deepsleep()







