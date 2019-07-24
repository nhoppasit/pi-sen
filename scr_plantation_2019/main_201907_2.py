import json
import datetime
from time import *
import serial  # <----Rpi
import memo
import uart
import RPi_I2C_driver
import temp_ctrl_lib
import lux_lib
import thegpio
import data_store
import _dropbox
import TSL2561
import AM2302
from suds.client import Client

import ap105_mod
import ap1701_mod

#--------------------------------------------------------------
# Check logging...
# Start new log file a day.
#--------------------------------------------------------------

memo.checkSystemNote()
memo.checkNoteFolder()
memo.checkMemoFolder[1]()

data_store.checkSystemNote()
data_store.checkNoteFolder()

#---------------------------------------------
# Program header
#---------------------------------------------

print "\n\n\n"
print "***************************************************************"
print " ME FARM"
print " (c)2017, Designed by RED FILE"
print "***************************************************************"
memo.appendNote("***************************************************************\n")
memo.appendNote(" ME FARM\n")
memo.appendNote("***************************************************************\n")

serviceState = -2;
try:
    cl = Client('http://farmboxwebhop.dyndns.org:8080/api/Control.asmx?WSDL', timeout=10)
    print 'Service success\n'
    memo.appendNote('Service success\n');
    serviceState = 0;
    
except Exception as ex:
    print 'Service failed\n'
    memo.appendNote('Service failed\n');    

#---------------------------------------------
# port detection
#---------------------------------------------
port_def = "/dev/ttyAMA0"  # <----Rpi
port_ap105v2_2 = '/dev/ttyUSB0'
port_air1 = '/dev/ttyUSB1'
port_air2 = '/dev/ttyUSB2'

ap105 = serial.Serial(port_ap105v2_2);
ap105.baudrate = 19200;
sleep(5);
ap105.write(':0\r');
sleep(0.2);
aptext = ap105.read(ap105.inWaiting());
print aptext;
print aptext[:2]

# try:

#     if aptext[:2]!='AP':
#         print 'Next port...\r'
#         sleep(1);
#         ap105.close();
#         sleep(1);
#         port_ap105v2_2 = '/dev/ttyUSB1'
#         port_air1 = '/dev/ttyUSB0'
#         port_air2 = '/dev/ttyUSB2'
#         ap105 = serial.Serial(port_ap105v2_2);
#         ap105.baudrate = 19200;
#         sleep(5);
#         ap105.write(':0\r');
#         sleep(0.2);
#         aptext = ap105.read(ap105.inWaiting());
#         print aptext;
#         print aptext[:2]
        
#         if aptext[:2]!='AP':
#             print 'Next port...\r'
#             sleep(1);
#             ap105.close();
#             sleep(1);
#             port_ap105v2_2 = '/dev/ttyUSB2'
#             port_air1 = '/dev/ttyUSB0'
#             port_air2 = '/dev/ttyUSB1'
#             ap105 = serial.Serial(port_ap105v2_2);
#             ap105.baudrate = 19200;
#             sleep(5);
#             ap105.write(':0\r');
#             sleep(0.2);
#             aptext = ap105.read(ap105.inWaiting());
#             print aptext;
#             print aptext[:2]

#     print '\r\nPORT of AP-105:'
#     print port_ap105v2_2;
#     print "\r\n"
#     memo.appendNote('PORT of AP-105:' + port_ap105v2_2)


# except Exception as ex:
#     print '\r\nPort of AP-105 failed\n'
#     memo.appendNote('Port of AP-105 failed');

#===============================================================================
# AP-105
#===============================================================================
ports = ["/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/ttyUSB2", "/dev/ttyUSB3", "/dev/ttyUSB4"]
ap105 = ap105_mod.ap105()
try:
    [idx_ap105_port, p] = ap105.auto_init(ports)
    print repr(p) + "\n"
    print ports[idx_ap105_port-1] + "\n"
    memo.appendNote('PORT of AP-105:' + ports[idx_ap105_port-1] + "\n")

    [a,b] = ap105.read_once()
    print "[%f C, %f %sRH]\r\n" % (a, b, "%")

except Exception as ex:
    print repr(ex) + "\n"
    memo.appendNote(repr(ex) + "\n")

#===============================================================================
# AP-1701
#===============================================================================
ap1701_addr = ["09","10","11"]
ap1701 = ap1701_mod.ap1701()
try:
    [idx_ap1701_port, p] = ap1701.auto_init(ports, ap1701_addr[0])
    print repr(p) + "\n"
    print ports[idx_ap1701_port-1] + "\n"
    memo.appendNote('PORT of AP-1701:' + ports[idx_ap1701_port-1] + "\n")

    for addr in ap1701_addr:
        [a,b] = ap1701.read_once(addr)
        print "[%f C, %f %sRH]\r\n" % (a, b, "%")

except Exception as ex:
    print repr(ex) + "\n"
    memo.appendNote(repr(ex) + "\n")

dt5 = 0.0
dh5 = 0.0
dt6 = 0.0
dh6 = 0.0
dt7 = 0.0
dh7 = 0.0
dt8 = 0.0
dh8 = 0.0

#===============================================================================
# AIR CONDITIONS
#===============================================================================
air1 = serial.Serial(port_air1);
air1.baudrate = 9600;
sleep(5);

air2 = serial.Serial(port_air2);
air2.baudrate = 9600;
sleep(5);


#===============================================================================
# MAIN SETUP
#===============================================================================

# LCD
#mylcd = RPi_I2C_driver.lcd(0x3F)
mylcd = RPi_I2C_driver.lcd(0x27)
mylcd.lcd_display_string_pos(datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S.%f [OPEN]"), 1, 0)

#---------------------------------------------
# Setup GPIO
#---------------------------------------------
thegpio.setupGPIO()
ryPin = [4,17,18,27,22,23,24,25]
for idx in range(8):
    thegpio.setAsOutput(ryPin[idx])
    thegpio.offPin(ryPin[idx])
    
# ------------------------------------------------
# Test host and open station
# ------------------------------------------------
loop = 1
Running = True

# ------------------------------------------------------------------------
# Loop  
# ------------------------------------------------------------------------
        
while Running:
    try:
        #--------------------------------------------------------------
        # Check logging...
        # Start new log file a day.
        #--------------------------------------------------------------
        
        memo.checkSystemNote()
        memo.checkNoteFolder()
        memo.checkMemoFolder[1]()
        
        data_store.checkSystemNote()
        data_store.checkNoteFolder()

        # ------------------------------------------------------------------------
        # Current loop
        # ------------------------------------------------------------------------
        
        if loop>100: 
            loop = 0;
        memo.appendNote("LOOP: %d\n" % loop)
        print "\nLOOP: " + str(loop)               
        if loop > 100:
            Running = False

        # ------------------------------------------------------------------------
        # Clear LCD
        # ------------------------------------------------------------------------
        # mylcd.lcd_clear()
        # sleep(0.5)

        # ------------------------------------------------------------------------
        # Read DHT
        # ------------------------------------------------------------------------
        h1, t1 = AM2302.DHT1()
        if h1 is not None and t1 is not None:
            print 'DHT1 -> Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t1, h1)
            #time.sleep(2)
        else:
            print 'Failed to get reading. Try again!'
        
        h2, t2 = AM2302.DHT2()
        if h2 is not None and t2 is not None:
            print 'DHT2 -> Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t2, h2)
            #time.sleep(2)
        else:
            print 'Failed to get reading. Try again!'
        
        h3, t3 = AM2302.DHT3()
        if h3 is not None and t3 is not None:
            print 'DHT3 -> Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t3, h3)
            #time.sleep(2)
        else:
            print 'Failed to get reading. Try again!'
        
        h4, t4 = AM2302.DHT4()
        if h4 is not None and t4 is not None:
            print 'DHT4 -> Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t4, h4)
            #time.sleep(2)
        else:
            print 'Failed to get reading. Try again!'
        
        dh1 = float(h1)
        dh2 = float(h2)
        dh3 = float(h3)
        dh4 = float(h4)
        dt1 = float(t1)
        dt2 = float(t2)
        dt3 = float(t3)
        dt4 = float(t4)              
        
        # AP-105
        try:
            [pdt5, pdh5] = ap105.read_once()
            print "[%f C, %f %sRH]\r\n" % (pdt5, pdh5, "%")
        except Exception as exap105:
            print repr(exap105) + "\n"
            pdt5 = 0
            pdh5 = 0

        # AP-1701        
        try:
            [pdt6, pdh6] = ap1701.read_once(ap1701_addr[0])
            print "[%f C, %f %sRH]\r\n" % (pdt6, pdh6, "%")
        except Exception as exap1701:
            print repr(exap1701) + "\n"
            pdt6 = 0
            pdh6 = 0

        try:
            [pdt7, pdh7] = ap1701.read_once(ap1701_addr[1])
            print "[%f C, %f %sRH]\r\n" % (pdt7, pdh7, "%")
        except Exception as exap1701:
            print repr(exap1701) + "\n"
            pdt7 = 0
            pdh7 = 0

        try:
            [pdt8, pdh8] = ap1701.read_once(ap1701_addr[2])
            print "[%f C, %f %sRH]\r\n" % (pdt8, pdh8, "%")
        except Exception as exap1701:
            print repr(exap1701) + "\n"
            pdt8 = 0
            pdh8 = 0

        # Keep
        if pdh5>0 and pdt5>0: 
            dh5 = pdh5
            dt5 = pdt5
        if pdh6>0 and pdt6>0: 
            dh6 = pdh6
            dt6 = pdt6
        if pdh7>0 and pdt7>0: 
            dh7 = pdh7
            dt7 = pdt7
        if pdh8>0 and pdt8>0: 
            dh8 = pdh8
            dt8 = pdt8

        # CO2
        dCO2 = 2500

        # LCD TEXT        
        strLCDMsg1 = "%2.1f,%2.1f|%2.1f,%2.1f " % (dh5,dt5,dh6,dt6)
        strLCDMsg2 = "%2.1f,%2.1f|%2.1f,%2.1f " % (dh7,dt7,dh8,dt8)

        # ------------------------------------------------------------------------
        # Update LCD by TIMERY
        # ------------------------------------------------------------------------
        mylcd.lcd_display_string_pos(strLCDMsg1, 1, 0)
        mylcd.lcd_display_string_pos(strLCDMsg2, 2, 0)
        #memo.appendNote("Update DHT on LCD\n")
        #memo.appendNote(strLCDMsg1)
        #memo.appendNote(strLCDMsg2)
        print "Update DHT on LCD"
        print strLCDMsg1
        print strLCDMsg2

        # ------------------------------------------------------------------------
        # Read LUX
        # ------------------------------------------------------------------------
        lux1 = "000"

        ch0,ch1 = TSL2561.LUX29()        
        # Output data to screen
        print "Full Spectrum(IR + Visible) :%d lux" %ch0
        print "Infrared Value :%d lux" %ch1
        print "Visible Value :%d lux" %(ch0 - ch1)
        
        ch0,ch1 = TSL2561.LUX39()        
        # Output data to screen
        print "Full Spectrum(IR + Visible) :%d lux" %ch0
        print "Infrared Value :%d lux" %ch1
        print "Visible Value :%d lux" %(ch0 - ch1)
        lux1 = ch0
        
        ch0,ch1 = TSL2561.LUX49()        
        # Output data to screen
        print "Full Spectrum(IR + Visible) :%d lux" %ch0
        print "Infrared Value :%d lux" %ch1
        print "Visible Value :%d lux" %(ch0 - ch1)

        ilux1 = int(lux1)
        
        strLCDMsg3 = "LUX1:%d, CO2 = %d  " % (ilux1, dCO2)
        

        # ------------------------------------------------------------------------
        # Update LCD by TIMERY
        # ------------------------------------------------------------------------
        mylcd.lcd_display_string_pos(strLCDMsg3, 3, 0)
        #memo.appendNote("Update LUX on LCD\n")
        #memo.appendNote(strLCDMsg3)
        print "\r\nUpdate LUX on LCD"
        print strLCDMsg3
        print "\r\n"
                            
        print "\r\nLCD TEXT"
        print strLCDMsg1
        print strLCDMsg2
        print strLCDMsg3
        print "\r\n"

        # ------------------------------------------------------------------------
        # LOOP SLEEP and NEXT LOOP
        # Use without KEYPAD
        # ------------------------------------------------------------------------
        # sleep(1)
        
        # ------------------------------------------------------------------------
        # HTTP
        # ------------------------------------------------------------------------
        wwwMsg = '<p>\r\n'
        wwwMsg = wwwMsg + "Humidity-5 = %2.1f %%RH     Temperature-5 = %2.1f degC<br>\r\n" % (dh5,dt5)
        wwwMsg = wwwMsg + "Humidity-6 = %2.1f %%RH     Temperature-6 = %2.1f degC<br>\r\n" % (dh6,dt6)
        wwwMsg = wwwMsg + "Humidity-7 = %2.1f %%RH     Temperature-7 = %2.1f degC<br>\r\n" % (dh7,dt7)
        wwwMsg = wwwMsg + "Humidity-8 = %2.1f %%RH     Temperature-8 = %2.1f degC<br>\r\n" % (dh8,dt8)
        wwwMsg = wwwMsg + "Humidity-1 = %2.1f %%RH     Temperature-1 = %2.1f degC<br>\r\n" % (dh1,dt1)
        wwwMsg = wwwMsg + "Humidity-2 = %2.1f %%RH     Temperature-2 = %2.1f degC<br>\r\n" % (dh2,dt2)
        wwwMsg = wwwMsg + "Humidity-3 = %2.1f %%RH     Temperature-3 = %2.1f degC<br>\r\n" % (dh3,dt3)
        wwwMsg = wwwMsg + "Humidity-4 = %2.1f %%RH     Temperature-4 = %2.1f degC<br>\r\n" % (dh4,dt4)
        wwwMsg = wwwMsg + "LUX = %d lux<br>\r\n" % (ilux1) 
        wwwMsg = wwwMsg + "CO2 = %d ppm<br>\r\n" % (dCO2)
        wwwMsg = wwwMsg + '</p>\r\n'
        data_store.writeState(wwwMsg)
        print "\r\nHTTP server:"
        print wwwMsg
        print "\r\n"
        
        # -----------
        # Pull state online
        # -----------
        if serviceState!=0:
            try:
                cl = Client('http://farmboxwebhop.dyndns.org:8080/api/Control.asmx?WSDL', timeout=10)
                print 'Service success\n'
                memo.appendNote('Service success\n');
                serviceState = 0;
                
            except Exception as ex:
                print repr(ex)
                print 'Service failed\n'
                memo.appendNote('Service failed\n');
                serviceState = -2;
                        
        try:
            print "\r\n REMOTE PULLING"
            ret = cl.service.RemotePull("0010")
            print ret
            memo.appendNote(ret + '\r\n')
            serviceState = 0;
            
            #-----------------------------
            # check ret
            #-----------------------------
            todos = json.loads(ret)
            print todos["Message"]
            print todos["Code"]
            if todos["Code"]=="00":
                print todos["Data"]
                iimax = len(todos["Data"]) 
                print  iimax
                for ii in range(iimax): # Data loop
                    txheader = todos["Data"][ii]["TRANSACTION_HEADER"]
                    messagedata = todos["Data"][ii]["MESSAGE_DATA"]
                    print txheader
                    print messagedata
                    
                    #---------------------------
                    # Process transaction
                    #---------------------------
                    if txheader=="0100": # light off
                        fo = open("/home/multiply/app/light.dat","w")                          
                        fo.write("off");
                        fo.close() 
                        print "Write remote command. Light off"
                        
                    #---------------------------
                    if txheader=="0101": # light on
                        fo = open("/home/multiply/app/light.dat","w")                          
                        fo.write("on");
                        fo.close() 
                        print "Write remote command. Light on"
                        
                    #---------------------------
                    if txheader=="0200": # Air1 off
                        try:
                            tempfile = "/home/multiply/app/air_off.txt"
                            print tempfile
                            fo = open(tempfile,"r")
                            airtxt = fo.read()
                            fo.close()
                            print airtxt
                            air1.write(airtxt);
                            print "Air 1 off."
                        except Exception as ex:
                            print repr(ex)                        

                    #---------------------------
                    if txheader=="0201": # Air1 on
                        try:
                            tempfile = "/home/multiply/app/air_on.txt"
                            print tempfile
                            fo = open(tempfile,"r")
                            airtxt = fo.read()
                            fo.close()
                            print airtxt
                            air1.write(airtxt);
                            print "Air 1 on."
                        except Exception as ex:
                            print repr(ex)                        
                        
                    #---------------------------
                    if txheader=="0300": # Air2 off
                        try:
                            tempfile = "/home/multiply/app/air_off.txt"
                            print tempfile
                            fo = open(tempfile,"r")
                            airtxt = fo.read()
                            fo.close()
                            print airtxt
                            air2.write(airtxt);
                            print "Air 2 off."
                        except Exception as ex:
                            print repr(ex)                        

                    #---------------------------
                    if txheader=="0301": # Air2 on
                        try:
                            tempfile = "/home/multiply/app/air_on.txt"
                            print tempfile
                            fo = open(tempfile,"r")
                            airtxt = fo.read()
                            fo.close()
                            print airtxt
                            air2.write(airtxt);
                            print "Air 2 on."
                        except Exception as ex:
                            print repr(ex)                        

                    #---------------------------
                    if txheader=="0400": # Air1 off
                        try:
                            tempfile = "/home/multiply/app/temp_%s.txt" % messagedata
                            print tempfile
                            fo = open(tempfile,"r")
                            airtxt = fo.read()
                            fo.close()
                            print airtxt
                            air1.write(airtxt);
                            air2.write(airtxt);
                            print "Temp. set."
                        except Exception as ex:
                            print repr(ex)    
                        
                                
        except Exception as ex:
            print repr(ex)
            print 'Service failed\n'
            memo.appendNote('Service failed\n');
            serviceState = -2;
        
        # ----------
        # Light check
        # ----------
        print "Light check"
        try:
            fo = open("/home/multiply/app/light.dat","r")
            lighttxt = fo.read()
            fo.close()
            print lighttxt
            if lighttxt=="off":                    
                thegpio.offPin(ryPin[0])
                print "Light off"
            if lighttxt=="on":                    
                thegpio.onPin(ryPin[0])
                print "Light on"
                
        except Exception as ex:
            print repr(ex)    
            thegpio.setupGPIO()
            for idx in range(8):
                thegpio.setAsOutput(ryPin[idx])

            try:
                fo = open("/home/multiply/app/light.dat","r")
                lighttxt = fo.read()
                fo.close()
                print lighttxt
                if lighttxt=="off":                    
                    thegpio.offPin(ryPin[0])
                    print "Light off"
                if lighttxt=="on":                    
                    thegpio.onPin(ryPin[0])
                    print "Light on"

            except Exception as ex:
                print repr(ex)    
                
        
        
        # ----------
        # Loop sleep
        # ----------
        sleep(2)
        
        # ----------
        # Long tick loop
        # ----------
        loop += 1                
        if loop>=7:
            loop = 0
            print "\r\nUpdate data file."
            strDHTMsg = "%2.1f,%2.1f,%2.1f,%2.1f,%2.1f,%2.1f,%2.1f,%2.1f,%d,%2.1f,%2.1f,%2.1f,%2.1f,%2.1f,%2.1f,%d" % (dh5,dt5,dh1,dt1,dh2,dt2,dh3,dt3,ilux1, dh6,dt6 ,dh7,dt7 ,dh8,dt8, dCO2)
            mylcd.lcd_display_string_pos(datetime.datetime.now().strftime("%d %b %H:%M         "), 4, 0)
            data_store.appendNote(strDHTMsg + '\r\n')            
            print strDHTMsg + "\r\n"

            # -----------
            # Push state online
            # -----------
            #datetime.datetime.now().strftime("%a %d %b %Y %H:%M:%S.%f, ")
            strDHTMsg = datetime.datetime.now().strftime("%a %d %b %Y %H:%M:%S.%f, ") + strDHTMsg
            cid = 10            
            if serviceState!=0:
                try:
                    cl = Client('http://farmboxwebhop.dyndns.org:8080/api/Control.asmx?WSDL', timeout=10)
                    print 'Service success\n'
                    memo.appendNote('Service success\n');
                    serviceState = 0;
                    
                except Exception as ex:
                    print 'Service failed\n'
                    memo.appendNote('Service failed\n');
                    serviceState = -2;
            
            try:
                ret = cl.service.Push(cid , strDHTMsg)
                print ret
                memo.appendNote(ret + '\r\n')
                serviceState = 0;
                
            except Exception as ex:
                print 'Service failed\n'
                memo.appendNote('Service failed\n');
                serviceState = -2;
            
            #-------------------------------------------------------------------
            # UPLOAD 
            #-------------------------------------------------------------------
            #print "********Upload last log file**********"            
            #_dropbox.uploadLastLog()      
            #memo.appendNote("********Upload last log file**********\n")
                  
            
        print "Next..."
        
        
        
    #*****************************************************************************
    # SYSTEM CATCH
    #*****************************************************************************
    except Exception as ex:
        thegpio.clean()
        print repr(ex)
        memo.appendNote(repr(ex) + '\r\n')
        Running = True # True / False
    

sleep(1)
thegpio.clean()
mylcd.backlight(0)
print "\nEND PROGRAM"

#--------------------------------------------------------------------------------
if __name__ == '__main__':
    pass
