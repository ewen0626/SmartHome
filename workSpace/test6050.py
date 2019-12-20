import utime
from machine import I2C, Pin
from mpu9250 import MPU9250
from mpu6500 import MPU6500, SF_G, SF_DEG_S


from machine import UART
com1 = UART(1, 9600,tx=2,rx=15)
com2 = UART(2, 9600)

com1.init(9600)
com2.init(9600)

i2c = I2C(scl=Pin(22), sda=Pin(21))
mpu6500 = MPU6500(i2c, accel_sf=SF_G, gyro_sf=SF_DEG_S)
sensor = MPU9250(i2c, mpu6500=mpu6500)
while True:
  
  data1 = com1.readline()
  data2 = com2.readline()
  if data1 and ('$GPRMC' in data1):
    print("from 1 :"+str(data1))
  if data2 and ('$GNR' in data2):
    print("from 2 :"+str(data2))
   
  print(sensor.acceleration)
  print(sensor.gyro)
  print(sensor.magnetic)
  utime.sleep_ms(1000)
