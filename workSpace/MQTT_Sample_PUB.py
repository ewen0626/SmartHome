

from umqtt.simple import MQTTClient

# Test reception e.g. with:
# mosquitto_sub -t foo_topic

def main(server="192.168.0.112"):
    c = MQTTClient("umqtt_client", server)
    c.connect()
    c.publish(b"homebridge/to/set", b"中文")
    c.publish(b"homebridge/from/set", b"hello1")
    c.disconnect()

if __name__ == "__main__":
    main()



