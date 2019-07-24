'''
Created on Jul 14, 2019

@author: think

Test code for CO2 sensor via serial port.
'''

from time import sleep
import serial

def main():

    ports = ["COM1", "COM17", "COM16", "COM13", "COM17"]
    ap1701_addr = ["09","10","11"]
    ap1701_port = ""
    ap1701_sht15_temp = [float(0.0), float(0.0), float(0.0)]
    ap1701_sht15_hu = [float(0.0), float(0.0), float(0.0)]

    print "\n======================================================================="
    print "AP-1701-RS485: Test auto initialization."
    print "======================================================================="
    print "\r\n"
    print "Auto initial port of AP1701."
    print "Test for addressing of first node [" + ap1701_addr[0] + "]"
    ap1701_idx = 0
    for port in ports:
        try:
            print "\nOpen " + port + "..."
            ser = serial.Serial(port,9600,timeout=0)
            print ser
            sleep(1)
            if not ser.is_open: continue
            write_text = ":" + ap1701_addr[ap1701_idx] + "1\r"
            print write_text
            ser.write(write_text)
            sleep(0.5)
            databuf = ser.read(20)
            ser.close()
            print "databuff => " + repr(databuf)
            print "length = " + str(len(databuf))
            
            # Validation
            if len(databuf)!=14:
                print "Wrong port response!"
                sleep(1)
                continue     
            else:
                print "Good response."           

            # Keep findings
            ap1701_port = port
            ap1701_sht15_temp[ap1701_idx] = float(databuf[1:6])
            ap1701_sht15_hu[ap1701_idx] = float(databuf[8:12])
            break
                                
        except Exception as ex:
            logtext = "ERROR: initial serial port! " + repr(ex) 
            print logtext
            sleep(1)

    # Discuss auto find CO2-sensor
    if ap1701_port!="": # OK
        print "\nPort of AP-1701 interfacing is " + ap1701_port + "."
        print "Temperature = " + str(ap1701_sht15_temp[ap1701_idx]) + " C."
        print "Humidity = " + str(ap1701_sht15_hu[ap1701_idx]) + " %RH."
    else: # NG
        print "\nAP-1701 not found!"


if __name__ == '__main__':
    main()
    print "\n"
    pass