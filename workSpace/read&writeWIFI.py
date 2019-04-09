import os
import json


file = open("defaultWiFi.json",'r') #讀取預設WIFI設定檔案
wifi = file.read()
file.close()
wifi = json.loads(wifi)
print(wifi)


wifi["ssid"] = "5678" #更改WIFI設定檔
file = open("defaultWiFi.json",'w')
wifi = json.dumps(wifi)
file.write(wifi) 
file.close()
print(wifi)

