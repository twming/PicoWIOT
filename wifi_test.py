from time import sleep
import network

wifi = network.WLAN(network.STA_IF)
wifi.active(True)

counter=0
print('Network connecting ...')

if (not wifi.isconnected()):
    while(not wifi.isconnected() and counter<=5):
        wifi.connect('M1-Nautilus', 'GoMicron88')
        counter=counter+1
        sleep(1)    
    
print(wifi)
wifi.disconnect()