
    
from umqtt.simple import MQTTClient

# Test reception e.g. with:
# mosquitto_sub -t foo_topic

def main(server="test.mosquitto.org"):
    c = MQTTClient("umqtt_client", server)
    c.connect()
    c.publish(b"homebridge/from/set", b"hello")
    c.publish(b"homebridge/from/set", b"hello1")
    c.disconnect()

if __name__ == "__main__":
    main()

