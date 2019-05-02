# -*- coding: utf-8 -*-

"""
   程式說明請參閱18-38頁
"""

from umqtt.simple import MQTTClient
from machine import Pin
import dht
import machine
import network
import time
import ubinascii

rtc = machine.RTC()
rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
rtc.alarm(rtc.ALARM0, 30000)

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('dlink-731', '1223334444')

while not sta_if.isconnected():
  time.sleep(0.3)
  print(".")
  pass
print(sta_if.ifconfig())
config = {
	'broker' : 'mqtt.thingspeak.com',
	'user' : 'cubie',
	'key' : '5MD1U33J3DO9TEXG',
	'id' : 'room/' + ubinascii.hexlify(machine.unique_id()).decode(),
	'topic' : b'channels/772089/publish/I2AEIIER4RWMW0RT'
}

client = MQTTClient(client_id=config['id'],
		 server=config['broker'],
	 	 user=config['user'],
		 password=config['key'])

d = dht.DHT22(Pin(2))

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
	print('Publish data to ThingSpeak.')
	
	d.measure()
	data = 'field1={}&field2={}'.format(
		d.temperature(), 
		d.humidity())
	
	client.connect()
	client.publish(config['topic'],data.encode())
	time.sleep(2)
	client.disconnect()

print('Going to sleep...')
machine.deepsleep()

