import json
import time
from umqtt.simple import MQTTClient
from machine import Pin
machine.freq(160000000)
print(machine.freq())
relay = Pin(2, Pin.OUT)
# Publish test messages e.g. with:
# mosquitto_pub -t foo_topic -m hello

# Received messages from subscriptions will be delivered to this callback
def sub_cb(topic, msg):
  msg_decode = msg.decode('utf8')
  msg_decode = json.loads(msg_decode)
  print((topic, msg))
  print(msg_decode['service_name'])
  
  if msg_decode["service_name"] =="開關":
    light_state = 1 - relay.value()
    relay.value(light_state)
  

def main(server="192.168.0.100"):
  c1 = MQTTClient("umqtt_client", server)
  c1.set_callback(sub_cb)
  c1.connect()
  c1.subscribe(b"homebridge/from/set")
  
  
  while True:
    if True:
      # Blocking wait for message
      c1.wait_msg()

    else:
      # Non-blocking wait for message
      c1.check_msg()
      # Then need to sleep to avoid 100% CPU usage (in a real
      # app other useful actions would be performed instead)
      time.sleep(0.5)

  c1.disconnect()

if __name__ == "__main__":
  main()




