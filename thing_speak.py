from machine import Pin, Timer
import urequests
import dht
import network
import time
import sys

sensor=dht.DHT11(Pin(4))

WIFI_SSID = "M1-Nautilus"
WIFI_PASSWORD = "GoMicron88"

HTTP_HEADERS = {'Content-Type': 'application/json'} 
THINGSPEAK_WRITE_API_KEY = 'W60VAR2QV8M4KUB8'  

def connect_wifi():
	wifi=network.WLAN(network.STA_IF)
	wifi.active(True)
	wifi.disconnect()
	wifi.connect(WIFI_SSID,WIFI_PASSWORD)
	if not wifi.isconnected():
		print('Connecting...Wifi')
		timeout=0
		while(not wifi.isconnected() and timeout<5):
			print(5-timeout)
			timeout=timeout+1
			time.sleep(1)
	if(wifi.isconnected()):
		print('Wifi Connected')
	else:
		print('Wifi not connected')
		sys.exit()

connect_wifi()

led=Pin("LED",Pin.OUT)

def sens_data(data):  
    sensor.measure()
    temp=sensor.temperature()
    hum=sensor.humidity()
    dht_readings = {'field1':temp,'field2':hum}
    request = urequests.post( 'http://api.thingspeak.com/update?api_key=' + THINGSPEAK_WRITE_API_KEY, json = dht_readings, headers = HTTP_HEADERS )
    request.close()
    print("Temperature: {}°C Humidity: {}". format(temp, hum))
        
    global led
    led.toggle()

tim=Timer(-1)
tim.init(mode=Timer.PERIODIC, period=10000, callback=sens_data)

    
