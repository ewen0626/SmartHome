import network
import ubinascii
wlan=network.WLAN(network.STA_IF)
wlan.active(True)
wlan.config('mac')    #查詢 ESP8266 本身 MAC 位址
#b'`\x01\x94<\xcb\xab'
aps=wlan.scan()        #掃描附近無線基地台
#aps_decode = ubinascii.hexlify(aps,':').decode()
wifidata = ""
#print(aps)
for data in aps:
  wifidata = wifidata + "+CWLAP:" + str(data)
  
print(wifidata)
