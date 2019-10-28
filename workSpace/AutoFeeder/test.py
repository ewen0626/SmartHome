#91~102 涓嶅嫊
#90 鎱㈣綁
import time
from machine import PWM
from machine import Pin
servo = PWM(Pin(5), freq=50)

period = 20000
minDuty = int(500/period * 1024)
maxDuty = int(2400/period * 1024)
unit = (maxDuty - minDuty)/180

def rotate(servo, degree=91):
  _duty = round(unit * degree) + minDuty
  _duty = min(maxDuty, max(minDuty, _duty))
  servo.duty(_duty)

rotate(servo, 90)
time.sleep(0.7)
rotate(servo, 91)

