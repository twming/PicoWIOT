from machine import Pin, Timer
from simple import MQTTClient
import dht
import network
import time
import sys

sensor=dht.DHT11(Pin(4))

WIFI_SSID = "xxxx"
WIFI_PASSWORD = "xxxx"

mqtt_client_id = bytes('client_'+'12322','utf-8')
ADAFRUIT_IO_URL = 'io.adafruit.com'
ADAFRUIT_USERNAME = "xxxx"
ADAFRUIT_IO_KEY = "xxxx"

TEMP_FEED_ID = 'temperature'
HUM_FEED_ID = 'humidity'
temp_feed=bytes("{:s}/feeds/{:s}".format(ADAFRUIT_USERNAME,TEMP_FEED_ID),'utf-8')
hum_feed=bytes("{:s}/feeds/{:s}".format(ADAFRUIT_USERNAME,HUM_FEED_ID),'utf-8')


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

client=MQTTClient(client_id=mqtt_client_id,
		server=ADAFRUIT_IO_URL,
		user=ADAFRUIT_USERNAME,
		password=ADAFRUIT_IO_KEY,
		ssl=False)

try:
	status=client.connect()
	print("Connected to MQQT server")
except Exception as e:
	print('Could not connect to MQTT server {}{}'.format(type(e).__name__,e))
	sys.exit()


led=Pin("LED",Pin.OUT)
counter=0

def sens_data(data):
	sensor.measure()
	temp=sensor.temperature()
	hum=sensor.humidity()
	client.publish(temp_feed,bytes(str(temp),'utf-8'),qos=0)
	client.publish(hum_feed,bytes(str(hum),'utf-8'),qos=0)
	print("Temperature: {}°C Humidity: {}". format(temp, hum))
	global led
	led.toggle()

tim=Timer(-1)
tim.init(mode=Timer.PERIODIC, period=10000, callback=sens_data)
