from machine import Pin, Timer
from simple import MQTTClient
import dht
import network
import time
import sys

sensor=dht.DHT11(Pin(4))

WIFI_SSID = "xxxx"
WIFI_PASSWORD = "xxxxx"

mqtt_client_id = bytes('client_'+'12322','utf-8')
ADAFRUIT_IO_URL = 'io.adafruit.com'
ADAFRUIT_USERNAME = "xxxxx"
ADAFRUIT_IO_KEY = "xxxxxx"

LED_FEED_ID = 'led'
led_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME,LED_FEED_ID),'utf-8')

led=Pin("LED",Pin.OUT)
remote_led=Pin(5,Pin.OUT)


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

def led_check(topic,msg):
    print('Received Data: Topic = {}, Msg = {}'.format(topic,msg))
    received_data=str(msg,'utf=8')
    if received_data=='1':
        remote_led.value(1)
        print("remote_led : ON")
    if received_data=='0':
        remote_led.value(0)
        print("remote_led : OFF")


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

client.set_callback(led_check)
client.subscribe(led_feed)

def sens_data(data):
	client.check_msg()
	global led
	led.toggle()
	

    
tim=Timer(-1)
tim.init(mode=Timer.PERIODIC, period=10000, callback=sens_data)

