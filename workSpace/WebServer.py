import time
import network
import json
from machine import Pin
#from urllib import unquote

relay = Pin(2, Pin.OUT)
ap = network.WLAN(network.AP_IF)
sta = network.WLAN(network.STA_IF)

#ap.config(essid='TangSmartHome', authmode=network.AUTH_WPA_WPA2_PSK, password="12345678")
#ap.config(essid='TangSmartHome')
#ap.active(True)
sta.active(True)
sta.connect("5678","")
while not sta.isconnected():
  pass
print(sta.ifconfig())



file = open("config.json",'r') #讀取預設WIFI設定檔案
data = file.read()
file.close()
data = json.loads(data)
"""
file = open("config.json",'w')
data = json.dumps(data)
file.write(data) 
file.close()
print(data)
"""





import socket, os, gc
#machine.freq(160000000)
#print(machine.freq())
HOST = '0.0.0.0'
PORT = 80

httpHeader = '''HTTP/1.0 200 OK
Content-type: {}
Content-length: {}

'''

mimeTypes = {
	'.txt'  : 'text/plain',
  '.htm'  : 'text/html',
  '.html' : 'text/html',
  '.css'  : 'text/css',
  '.js'   : 'application/javascript',
  '.xml'  : 'application/xml',
  '.json' : 'application/json',
  '.jpg'  : 'image/jpeg',
  '.png'  : 'image/png',
  '.gif'  : 'image/gif',
  '.svg'  : 'image/svg+xml',
  '.ico'  : 'image/x-icon'
}

def checkFileSize(path):
  try:
    s = os.stat(path)
    
    if s[0] != 16384:
      fileSize = s[6]
    else:
      fileSize = None
    return fileSize
  except:
    return None

def checkMimeType(fileName):
  fileName = fileName.lower()

  for ext in mimeTypes:
    if fileName.endswith(ext):
      return mimeTypes[ext]
  return None

def err(socket, code, msg):
  socket.write("HTTP/1.1 "+code+" "+msg+"\r\n\r\n")
  socket.write(msg)
  
def parse(str):
  arr = str.split('&')
  args = {}

  for item in arr:
    data = item.split('=')
    args[data[0]] = data[1]
    
  return args


def query(client, path):
  cmd, str = path.split('?')
  if cmd == 'setwifi':
    
    args = parse(str)
    ssid = args['ssid']
    password = args['pass']
    
    
    deviceName = args['deviceName']
    sta.connect(ssid,password)
    while not sta.isconnected():
      pass
    
    ap.active(False)
    
    import urequests as req

    apiURL='{url}?pin={temp}'.format(
      url   = 'http://192.168.0.199:8080/123',
      temp  = deviceName
    
    )

    r = req.get(apiURL)
    deviceName = r.text
    print('content:', r.content)
    print('text:', deviceName)
    
    file = open("config.json",'r') #讀取預設WIFI設定檔案
    data = file.read()
    file.close()
    data = json.loads(data)
    data['deviceName'] = deviceName
    file = open("config.json",'w')
    data = json.dumps(data)
    file.write(data) 
    file.close()
    print(data)
    
    err(client, "200", "SetWiFiOK" )
  




def handleRequest(client):
  req = client.recv(1024).decode('utf8')
  #print('------------------------')
  #print(req)
  #print('------------------------')
  firstLine = req.split('\r\n')[0]
  #print(firstLine)
    
  httpMethod = ''
  path = ''

  try:
    httpMethod, path, httpVersion = firstLine.split()
    del httpVersion
  except:
    pass

  del firstLine
  del req

  if httpMethod == 'GET':
    fileName = path.strip('/')
    #print("path : "+fileName)
    if fileName == '':
      fileName = 'index.html'
      sendFile(client, fileName)
      
    
    elif fileName == "light":
      light_state = 1 - relay.value()
      relay.value(light_state)
      err(client, "200", "OK")
    
    elif '?' in fileName:
      query(client, fileName)
      #print("go to query")
      #err(client, "200", "hey")
    else:
      sendFile(client, fileName)
      #print("go to sendFile")

  else:
    
    err(client, "501", "Not Implemented")

  



def sendFile(client, fileName):
  contentType = checkMimeType(fileName)
  if contentType :
    fileSize = checkFileSize(fileName)
    if fileSize != None:
      f = open(fileName, 'r')
      httpHeader.format(contentType, fileSize)
      
      client.write(httpHeader.encode('utf-8'))
      while True:
        chunk = f.read(64)
        if len(chunk) == 0:
          break
        client.write(chunk)

      f.close()
    else:
      err(client, "404", "Not Found")
  else:
    err(client, "415", "Unsupported Media Type")

def main():
  s = socket.socket()
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind((HOST, PORT))
  s.listen(5)
  print('Web server running on port', PORT)
  while True:
    time.sleep(0.1)
    client = s.accept()[0]   
    handleRequest(client)
    client.close()

    print('Free RAM before GC:', gc.mem_free())
    gc.collect()
    print('Free RAM after GC:', gc.mem_free())
    print('--------------------------------------------')

main()










