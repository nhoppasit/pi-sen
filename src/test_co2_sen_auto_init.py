'''
Created on Jul 14, 2019

@author: think
'''

from time import sleep
import serial

def co2_chk_sum(databuf):
    print "CO2 sensor check sum."
    sum = int(0)
    for i in range(1,8):
        print repr(i)
        sum = sum + databuf[i]
        #print "Sum = " + str(sum)
    cal_sum = (sum & 0xFF)
    cal_sum = ((~cal_sum) + 1) & 0xFF
    print "Sum = " + str(cal_sum)
    return cal_sum


def main():

    ports = ["COM3", "COM13"]

    print "\n======================================================================="
    print "Test CO2 sensor auto initialization."
    print "======================================================================="
    print "\r\n"
    print "Auto initial port of CO2 sensor."
    for port in ports:
        port_co2 = ""
        try:
            print "\nOpen " + port + "..."
            ser = serial.Serial(port,9600,timeout=0)
            print ser
            sleep(0.1)
            if ser.is_open:
                ser.write([0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79])
                sleep(0.1)
                databuf = ser.read(20)
                ser.close()
                print "databuff => " + repr(databuf)
                print "length = " + str(len(databuf))
                if len(databuf)!=9:
                    print "Wrong port response!"
                    continue                
                port_co2 = port                    
        except Exception as ex:
            logtext = "ERROR: initial serial port! " + repr(ex) 
            print logtext

        print "\nPort of CO2 sensor interfacing is " + port_co2 + "."

if __name__ == '__main__':
    main()
    print "\n"
    pass