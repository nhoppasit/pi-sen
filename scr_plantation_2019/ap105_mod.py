'''
Created on Jul 14, 2019

@author: think

'''

from time import sleep
import serial

class ap105:

    def __init__(self):
        self.os = "PI"
        pass

    def auto_init(self, ports):
        # Find AP-105 port automatically.
        # port = auto_init(ports, "09")
        # For example.
        # ports = ["COM1", "COM17", "COM16", "COM13", "COM17"]
        # ap105_addr = ["09","10","11"]
        
        ap105_port = ""
        ap105_sht15_temp = float(0.0)
        ap105_sht15_hu = float(0.0)

        print "\n======================================================================="
        print "AP-105-RS232: Test auto initialization."
        print "======================================================================="
        print "\r\n"
        print "Auto initial port of AP-105."
        port_idx = 0
        for port in ports:
            try:
                port_idx = port_idx+1
                print "\nOpen " + port + "..."
                ser = serial.Serial(port,19200,timeout=5.0)
                print ser
                sleep(1)
                if self.os=="PI":
                    if not ser.isOpen(): continue
                else:
                    if not ser.is_open: continue
                write_text = ":0\r"
                print "AP-105 << " + repr(write_text)
                ser.write(write_text)
                sleep(0.7)
                databuf = ser.read(ser.inWaiting())
                print "AP-105 >> " + repr(databuf)
                print "length = " + str(len(databuf))
                                
                # Validation
                if len(databuf)<=0 or 20<len(databuf):
                    ser.close()
                    print "Wrong port response!"
                    sleep(1)
                    continue
                # print  databuf[:2]   
                if databuf[:2]!='AP':
                    ser.close()
                    print "Wrong port response!"
                    sleep(1)
                    continue     
                
                print "Good response."           

                # Keep findings
                self.serial_port = ser
                self.port = port
                ap105_port = port
                write_text = ":1\r"
                print "AP-105 << " + repr(write_text)
                ser.write(write_text)
                sleep(0.7)
                databuf = ser.read(ser.inWaiting())
                print "AP-105 >> " + repr(databuf)
                print "length = " + str(len(databuf))
                ser.close()
                t5 = databuf[3:8]
                h5 = databuf[9:11]  
                ap105_sht15_temp = float(t5)
                ap105_sht15_hu = float(h5)
                break
                                    
            except Exception as ex:
                logtext = "ERROR: initial serial port! " + repr(ex) 
                print logtext
                sleep(1)

        # Discuss auto find CO2-sensor
        if ap105_port!="": # OK
            print "\nPort of AP-105 interfacing is " + ap105_port + "."
            print "Temperature = " + str(ap105_sht15_temp) + " C."
            print "Humidity = " + str(ap105_sht15_hu) + " %RH.\n"
        else: # NG
            print "\nAP-105 not found!\n"

        return [port_idx, ap105_port]

    def read_once(self):
        try:            
            print "AP-105 read once..."
            if self.os=="PI":
                if not self.serial_port.isOpen(): 
                    self.serial_port.open()
                    print "PI-Open port..."
            else:
                if not self.serial_port.is_open: 
                    self.serial_port.open()
                    print "Open port..."

            print self.serial_port
            write_text = ":1\r"
            print "AP-105 << " + repr(write_text)
            self.serial_port.write(write_text)
            sleep(0.5)
            databuf = self.serial_port.read(self.serial_port.inWaiting())        
            print "AP-105 >> " + repr(databuf)
            print "length = " + str(len(databuf))
            
            # Validation
            if not ("T" in databuf and "H" in databuf):
                print "Wrong port response!\n"
                sleep(1)
            else:
                print "Good response.\n"           

            # Keep findings
            t5 = databuf[3:8]
            h5 = databuf[9:11]  
            ap105_sht15_temp = float(t5)
            ap105_sht15_hu = float(h5)
        
            return [ap105_sht15_temp, ap105_sht15_hu]

        except Exception as ex:            
            print repr(ex) + "\n"
            return [0.0, 0.0]
