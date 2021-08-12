import hub, utime
from Backpack_Code import Backpack
from hub import port
from utime import sleep_ms

dongle = Backpack(hub.port.F, verbose = False) 
dongle.ask('\x03')

commands = '''
\x05
import network
import ESPClient
wlan = network.WLAN()
import ujson
wlan.active(True)
wlan.connect('gowifi', 'LB2005go')
wlan.isconnected()

def check():
    while(True):
        PORT = 443
        base='api.openweathermap.org'
        request='GET /data/2.5/weather?lat=42.4184&lon=-71.1062&appid=ca3fe4dbccb6541b88c49d29efa2c0e1 HTTP/1.0\\r\\nHost: api.openweathermap.org\\r\\n'
        request+= 'User-Agent:Ayan\\r\\n'
        request += 'Connection:keep-live\\r\\n\\r\\n'
        print(request)
        status, reason, reply = ESPClient.REST(base, PORT, request, False )
        

        wind = ujson.loads(reply)['wind']
        windDirection = wind['deg']

        main = ujson.loads(reply)['main']
        temp = main['temp']
        
        return windDirection, temp

\x04
'''

def configure():
    if not dongle.setup(): return False
    for cmd in commands.split('\n'):
        if not dongle.EOL(dongle.ask(cmd)) : return False
    return True
    

MotorE = port.E.motor
print(configure())


reply = dongle.ask('check()')
print(reply)

reply = dongle.ask('check()')
print(reply)
r = reply.split('\r\n') 
windDir=eval(r[-2])[0]     
tempK=eval(r[-2])[1]
tempFaren = (tempK-273.15)*9/5 + 32
        
MotorE.run_for_degrees(windDir,speed=50)

hub.led(int(tempFaren/10))
