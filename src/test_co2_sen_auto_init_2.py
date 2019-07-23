'''
Created on Jul 14, 2019

@author: think

Test code for CO2 sensor via serial port.
'''

from time import sleep
import serial

def co2_chk_sum(databuf): 
    """
    Data buffer is string from serial port.
    """
    print "Checksum calculating..."
    sum = int(0)
    for i in range(1,8):
        # print repr(i)
        sum = sum + ord(databuf[i])
        # print "Sum = " + str(sum)
    cal_sum = (sum & 0xFF)
    cal_sum = ((~cal_sum) + 1) & 0xFF
    print "Calculated Sum = " + str(cal_sum)
    return cal_sum


def main():

    ports = ["COM16", "COM13"]
    port_co2 = ""
    co2_ppm = int(0)
    co2_sen_temp = int(0)

    print "\n======================================================================="
    print "Test CO2 sensor auto initialization."
    print "======================================================================="
    print "\r\n"
    print "Auto initial port of CO2 sensor."
    for port in ports:
        try:
            print "\nOpen " + port + "..."
            ser = serial.Serial(port,9600,timeout=0)
            print ser
            sleep(0.1)
            if not ser.is_open: continue
            ser.write([0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79])
            sleep(0.1)
            databuf = ser.read(20)
            ser.close()
            print "databuff => " + repr(databuf)
            print "length = " + str(len(databuf))
            
            # Validation
            if len(databuf)!=9:
                print "Wrong port response!"
                continue     
            else:
                print "Good response."           
            if co2_chk_sum(databuf) != ord(databuf[8]):
                print "Wrong checksum of " + str(ord(databuf[8])) + "!"
                continue
            else:
                print "Checksum OK."

            # Keep
            port_co2 = port
            ppm = ord(databuf[2]) * 256 + ord(databuf[3])
            temp = ord(databuf[4])
            break
                                
        except Exception as ex:
            logtext = "ERROR: initial serial port! " + repr(ex) 
            print logtext

    if port_co2!="":
        print "\nPort of CO2 sensor interfacing is " + port_co2 + "."
        print "CO2 concentration = " + str(ppm) + " ppm."
        print "Temperature = " + str(temp) + " C."
    else:
        print "\nCO2 sensor not found!"


if __name__ == '__main__':
    main()
    print "\n"
    pass