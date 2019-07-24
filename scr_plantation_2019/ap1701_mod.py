'''
Created on Jul 14, 2019

@author: think

'''

from time import sleep
import serial

class ap1701:

    def __init__(self):
        self.os = "PI"
        pass

    def auto_init(self, ports, address):
        # Find AP-1701 port automatically.
        # port = auto_init(ports, "09")
        # For example.
        # ports = ["COM1", "COM17", "COM16", "COM13", "COM17"]
        # ap1701_addr = ["09","10","11"]
        
        ap1701_port = ""
        ap1701_sht15_temp = float(0.0)
        ap1701_sht15_hu = float(0.0)

        print "\n======================================================================="
        print "AP-1701-RS485: Test auto initialization."
        print "======================================================================="
        print "\r\n"
        print "Auto initial port of AP1701."
        print "Test for addressing of [" + address + "]"
        for port in ports:
            try:
                print "\nOpen " + port + "..."
                ser = serial.Serial(port,9600,timeout=5.0)
                print ser
                sleep(1)
                if self.os=="PI":
                    if not ser.isOpen(): continue
                else:
                    if not ser.is_open: continue
                write_text = ":" + address + "1\r\n"
                print "AP-1701 << " + repr(write_text)
                ser.write(write_text)
                sleep(0.7)
                databuf = ser.read(20)
                ser.close()
                print "AP-1701 >> " + repr(databuf)
                print "length = " + str(len(databuf))
                
                # Validation
                if not ("T" in databuf and "H" in databuf):
                    print "Wrong port response!"
                    sleep(1)
                    continue     
                else:
                    print "Good response."           

                # Keep findings
                T_idx = databuf.find("T")
                self.serial_port = ser
                self.port = port
                ap1701_port = port
                # print databuf[T_idx+1:T_idx+6]
                ap1701_sht15_temp = float(databuf[T_idx+1:T_idx+6])
                ap1701_sht15_hu = float(databuf[T_idx+8:T_idx+12])
                break
                                    
            except Exception as ex:
                logtext = "ERROR: initial serial port! " + repr(ex) 
                print logtext
                sleep(1)

        # Discuss auto find CO2-sensor
        if ap1701_port!="": # OK
            print "\nPort of AP-1701 interfacing is " + ap1701_port + "."
            print "Temperature = " + str(ap1701_sht15_temp) + " C."
            print "Humidity = " + str(ap1701_sht15_hu) + " %RH.\n"
        else: # NG
            print "\nAP-1701 not found!\n"

        return ap1701_port

    def read_once(self, address):
        try:            
            print "AP-1701 read once..."
            if self.os=="PI":
                if not self.serial_port.isOpen(): 
                    self.serial_port.open()
            else:
                if not self.serial_port.is_open: 
                    self.serial_port.open()

            write_text = ":" + address + "1\r\n"
            print "AP-1701 << " + repr(write_text)
            self.serial_port.write(write_text)
            sleep(0.5)
            databuf = self.serial_port.read(20)        
            print "AP-1701 >> " + repr(databuf)
            print "length = " + str(len(databuf))
            
            # Validation
            if not ("T" in databuf and "H" in databuf):
                print "Wrong port response!\n"
                sleep(1)
            else:
                print "Good response.\n"           

            # Keep findings
            T_idx = databuf.find("T")
            ap1701_sht15_temp = float(databuf[T_idx+1:T_idx+6])
            ap1701_sht15_hu = float(databuf[T_idx+8:T_idx+12])
        
            return [ap1701_sht15_temp, ap1701_sht15_hu]

        except Exception as ex:            
            print repr(ex) + "\n"
            return [0.0, 0.0]

    def read_once2(self, serial_port, address):
        try:
            print "AP-1701 read once (2)..."
            if self.os=="PI":
                if not serial_port.isOpen(): serial_port.open()
            else:
                if not serial_port.is_open: serial_port.open()
            write_text = ":" + address + "1\r\n"
            print "AP-1701 << " + repr(write_text)
            serial_port.write(write_text)
            sleep(0.5)
            databuf = serial_port.read(20)        
            print "AP-1701 >> " + repr(databuf)
            print "length = " + str(len(databuf))
            
            # Validation
            if not ("T" in databuf and "H" in databuf):
                print "Wrong port response!"
                sleep(1)
            else:
                print "Good response."           

            # Keep findings
            T_idx = databuf.find("T")
            ap1701_sht15_temp = float(databuf[T_idx+1:T_idx+6])
            ap1701_sht15_hu = float(databuf[T_idx+8:T_idx+12])
        
            return [ap1701_sht15_temp, ap1701_sht15_hu]

        except Exception as ex:
            logtext = "ERROR: initial serial port! " + repr(ex) 
            print logtext
            return [0.0, 0.0]
