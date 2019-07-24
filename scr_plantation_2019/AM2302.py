import Adafruit_DHT

sensor = Adafruit_DHT.AM2302
pin = [5,6,12,13]

def DHT1():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin[0])
    #if humidity is not None and temperature is not None:
    #print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
    return humidity, temperature

def DHT2():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin[1])
    #if humidity is not None and temperature is not None:
    #print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
    return humidity, temperature

def DHT3():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin[2])
    #if humidity is not None and temperature is not None:
    #print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
    return humidity, temperature

def DHT4():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin[3])
    #if humidity is not None and temperature is not None:
    #print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
    return humidity, temperature
