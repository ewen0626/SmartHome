"""
{"name":"測試溫度","characteristic":"CurrentTemperature","value":18}

"""
from machine import Pin
from umqtt.simple import MQTTClient
import dht
import json
import time
import machine
import network
import ubinascii

WiFi_SSID = "5678"
WiFi_PASS = ""
MQTT_Server = "192.168.0.199"
DeviceName = "Temp"
data = {}

sta = network.WLAN(network.STA_IF) #設定WiFi連線
sta.active(True)
sta.connect(WiFi_SSID,WiFi_PASS)
mac = ubinascii.hexlify(sta.config('mac'),':').decode()#取得ADDRESS
print(mac)
while not sta.isconnected():
  pass
print(sta.ifconfig())


d = dht.DHT22(Pin(2))

rtc = machine.RTC()
rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
rtc.alarm(rtc.ALARM0, 30000)

time.sleep(2)



d.measure()
temp = d.temperature()
hum = d.humidity()
data['name'] = DeviceName
data['characteristic'] = 'CurrentTemperature'
data['value'] = temp
data = json.dumps(data)
print(data)
print("----------------------------")
print('Humidity: {}%'.format(hum))
print('Temperature: {}{}C'.format(temp, '\u00b0'))
print("GO TO SLEEP")
print("----------------------------")


c = MQTTClient("SuperTang" + mac, MQTT_Server)

c.connect()

c.publish(b"homebridge/to/set", data)


c.disconnect()
print("published!")
time.sleep(1)
machine.deepsleep()


