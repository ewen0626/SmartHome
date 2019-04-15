# -*- coding: utf-8 -*-



from machine import UART
com = UART(0, 115200)
com.init(115200)

while True:
  data = com.readline()
  if data:
    print(data)
    com.write(data)


