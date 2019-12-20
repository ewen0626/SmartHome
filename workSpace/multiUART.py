from machine import UART
com1 = UART(1, 9600,tx=2,rx=15)
com2 = UART(2, 9600)

com1.init(9600)
com2.init(9600)

while True:
    data1 = com1.readline()
    data2 = com2.readline()
    if data1 and ('$GPRMC' in data1):
      print("from 1 :"+str(data1))
    if data2 and ('$GNR' in data2):
      print("from 2 :"+str(data2))
