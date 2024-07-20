from machine import Pin, Timer
import urequests
import dht
import network
import time
import sys
import utime

trigger = Pin(15, Pin.OUT)
echo = Pin(14, Pin.IN)


WIFI_SSID = "xxxxxxx"
WIFI_PASSWORD = "xxxxxxx"

HTTP_HEADERS = {'Content-Type': 'application/json'} 
THINGSPEAK_WRITE_API_KEY = 'xxxxxxx'  

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

def ultra(data):
   trigger.low()
   utime.sleep_us(2)
   trigger.high()
   utime.sleep_us(5)
   trigger.low()
   while echo.value() == 0:
       signaloff = utime.ticks_us()
   while echo.value() == 1:
       signalon = utime.ticks_us()
   timepassed = signalon - signaloff
   distance = (timepassed * 0.0343) / 2
   print("The distance from object is ",distance,"cm")
   
   distance_readings = {'field3':distance}
   request = urequests.post( 'http://api.thingspeak.com/update?api_key=' + THINGSPEAK_WRITE_API_KEY, json = distance_readings, headers = HTTP_HEADERS )
   request.close()

   # TODO: Write a code to turn on the LED if distance less than 8cm
   # global led

tim=Timer(-1)
tim.init(mode=Timer.PERIODIC, period=10000, callback=ultra)

    
