
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

#import urllib 
#from urllib import unquote
#unquote('%C4%A7%CA%DE')
print("123")
#print(unquote_plus('%E6%88%BF%E9%96%93%E7%87%88'))


# -*- coding: utf-8 -*-

"""
   程式說明請參閱17-23頁
"""

import urequests as req

apiURL='{url}?pin={temp}'.format(
    url   = 'http://192.168.0.199:8080/123',
    temp  = "%E6%88%BF%E9%96%93%E7%87%88"
    
)

r = req.get(apiURL)

print('content:', r.content)
print('text:', r.text)
