 
import time
from umqtt.simple import MQTTClient
from machine import Pin

relay = Pin(2, Pin.OUT)
# Publish test messages e.g. with:
# mosquitto_pub -t foo_topic -m hello

# Received messages from subscriptions will be delivered to this callback
def sub_cb(topic, msg):
  print((topic, msg))
  light_state = 1 - relay.value()
  relay.value(light_state)
  

def main(server="test.mosquitto.org"):
  c1 = MQTTClient("umqtt_client", server)
  c1.set_callback(sub_cb)
  c1.connect()
  c1.subscribe(b"homebridge/from/set")
  c1.subscribe(b"3211111")
  
  while True:
    if True:
      # Blocking wait for message
      c1.wait_msg()

    else:
      # Non-blocking wait for message
      c1.check_msg()
      # Then need to sleep to avoid 100% CPU usage (in a real
      # app other useful actions would be performed instead)
      time.sleep(1)

  c1.disconnect()

if __name__ == "__main__":
  main()


