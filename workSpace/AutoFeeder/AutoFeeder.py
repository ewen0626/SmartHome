#91~102 涓嶅嫊
#90 鎱㈣綁
import time
from machine import PWM,ADC
from machine import Pin
import json
import time
import network
import ubinascii
from umqtt.simple import MQTTClient

WiFi_SSID = "SuperTang"
WiFi_PASS = "0930082454"
MQTT_Server = "192.168.1.112"
#DeviceName = "主臥室燈"



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
led=Pin(2,Pin.OUT)
led.value(0)
print(sta.ifconfig())


servo = PWM(Pin(5), freq=50)
IR=Pin(14,Pin.IN)           

period = 20000
minDuty = int(500/period * 1024)
maxDuty = int(2400/period * 1024)
unit = (maxDuty - minDuty)/180

def rotate(servo, degree=91):
  _duty = round(unit * degree) + minDuty
  _duty = min(maxDuty, max(minDuty, _duty))
  servo.duty(_duty)
  
  
def sub_cb(topic, msg): # 收到訊息時處理
  msg_decode = msg.decode('utf8')
  #msg_decode = json.loads(msg_decode) #資料前處理
  print((topic, msg))
  #print(msg_decode['service_name'])
  
  if msg_decode == "feed":
    rotate(servo, 90)
    time.sleep(0.5)
    while IR.value()==1:
      rotate(servo, 90)

    rotate(servo, 91)


def main(server=MQTT_Server):  #Connect to MQTT Server 
  c1 = MQTTClient("SuperTang" + mac, server)
  c1.set_callback(sub_cb)
  c1.connect()
  c1.subscribe(b"CatFeeder") #subscribe homebridge's Topic
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

if __name__ == "__main__":

  main()
  
  print("ERROR....Reset...")
  #machine.reset()




