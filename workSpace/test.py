
import json
file = open("config.json",'r') #讀取預設WIFI設定檔案
data = file.read()
file.close()
data = json.loads(data)
print(data)
file = open("config.json",'w')
data = json.dumps(data)
file.write(data) 
file.close()
print(data)

from urllib import unquote
#from urllib import unquote
#unquote('%C4%A7%CA%DE')

#print (urllib.unquote('%C4%A7%CA%DE'))

