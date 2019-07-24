import time
import AM2302
from time import sleep

while True:
    humidity, temperature = AM2302.DHT1()
    if humidity is not None and temperature is not None:
        print 'DHT1 -> Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
        #time.sleep(2)
    else:
        print 'Failed to get reading. Try again!'
    
    humidity, temperature = AM2302.DHT2()
    if humidity is not None and temperature is not None:
        print 'DHT2 -> Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
        #time.sleep(2)
    else:
        print 'Failed to get reading. Try again!'
    
    humidity, temperature = AM2302.DHT3()
    if humidity is not None and temperature is not None:
        print 'DHT3 -> Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
        #time.sleep(2)
    else:
        print 'Failed to get reading. Try again!'
    
    humidity, temperature = AM2302.DHT4()
    if humidity is not None and temperature is not None:
        print 'DHT4 -> Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
        #time.sleep(2)
    else:
        print 'Failed to get reading. Try again!'
    
    print "----"
    sleep(1)