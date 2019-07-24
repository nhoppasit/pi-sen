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

port_def = "/dev/ttyAMA0"  # <----Rpi
lux_port_def = "/dev/ttyACM0"  # <----Rpi

#===============================================================================
# MAIN SETUP
#===============================================================================

# LCD
mylcd = RPi_I2C_driver.lcd(0x3F)

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
mylcd.lcd_display_string_pos(datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S.%f [OPEN]"), 1, 0)

#---------------------------------------------
# Setup GPIO
#---------------------------------------------
thegpio.setupGPIO()

#---------------------------------------------
# Serial port name
#---------------------------------------------
serial_port = serial.Serial()
lux_port = serial.Serial()

try:
    serial_port = serial.Serial(port_def, baudrate=9600, timeout=0)
    sleep(1)
    
    logtext = "Initial serial port of %s..." % port_def
    print logtext
    memo.appendNote(logtext + '\n')
    
    lux_port = serial.Serial(lux_port_def, baudrate=9600, timeout=0)
    sleep(1)

    logtext = "Initial serial port of %s..." % lux_port_def
    print logtext
    memo.appendNote(logtext + '\n')

except:
    logtext = "ERROR: initial serial port..." 
    print logtext
    memo.appendNote(logtext + '\n')
    

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
        h1 = "000"
        t1 = "000"
        h2 = "000"
        t2 = "000"
        h3 = "000"
        t3 = "000"
        h4 = "000"
        t4 = "000"
        (h1, t1, h2, t2, h3, t3, h4, t4) = temp_ctrl_lib.getState(serial_port)
        
        dh1 = float(h1)/10.0
        dh2 = float(h2)/10.0
        dh3 = float(h3)/10.0
        dh4 = float(h4)/10.0
        dt1 = float(t1)/10.0
        dt2 = float(t2)/10.0
        dt3 = float(t3)/10.0
        dt4 = float(t4)/10.0
        
        strLCDMsg1 = "%2.1f,%2.1f|%2.1f,%2.1f " % (dh1,dt1,dh2,dt2)
        strLCDMsg2 = "%2.1f,%2.1f|%2.1f,%2.1f " % (dh3,dt3,dh4,dt4)
        

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
        (lux1) = lux_lib.getState(lux_port)
        
        ilux1 = int(lux1)
        
        strLCDMsg3 = "LUX1:%d            " % (ilux1)
        

        # ------------------------------------------------------------------------
        # Update LCD by TIMERY
        # ------------------------------------------------------------------------
        mylcd.lcd_display_string_pos(strLCDMsg3, 3, 0)
        #memo.appendNote("Update LUX on LCD\n")
        #memo.appendNote(strLCDMsg3)
        print "Update LUX on LCD"
        print strLCDMsg3
                
        # ------------------------------------------------------------------------
        # Display program by key
        # ------------------------------------------------------------------------
        print "Scan keys"
        key = thegpio.trackKey(mylcd,
                               "    THE PROFILER",
                               "",
                               "PROGRAMS",
                               "KEY: "
                               ,4,5,False) # 1.0 Sec scanning

        
        # ------------------------------------------------------------------------
        # LOOP SLEEP and NEXT LOOP
        # Use without KEYPAD
        # ------------------------------------------------------------------------
        # sleep(1)
        
        # ------------------------------------------------------------------------
        # HTTP
        # ------------------------------------------------------------------------
        wwwMsg = '<p>\r\n'
        wwwMsg = wwwMsg + "Humidity-1 = %2.1f %%RH     Temperature-1 = %2.1f degC<br>\r\n" % (dh1,dt1)
        wwwMsg = wwwMsg + "Humidity-2 = %2.1f %%RH     Temperature-2 = %2.1f degC<br>\r\n" % (dh2,dt2)
        wwwMsg = wwwMsg + "Humidity-3 = %2.1f %%RH     Temperature-3 = %2.1f degC<br>\r\n" % (dh3,dt3)
        wwwMsg = wwwMsg + "Humidity-4 = %2.1f %%RH     Temperature-4 = %2.1f degC<br>\r\n" % (dh4,dt4)
        wwwMsg = wwwMsg + "LUX = %d\r\n" % (ilux1)
        wwwMsg = wwwMsg + '</p>\r\n'
        data_store.writeState(wwwMsg)
        
        loop += 1                
        if loop>=(60/1.5):
            print "Update data file."
            strDHTMsg = "%2.1f,%2.1f,%2.1f,%2.1f,%2.1f,%2.1f,%2.1f,%2.1f,%d" % (dh1,dt1,dh2,dt2,dh3,dt3,dh4,dt4,ilux1)
            mylcd.lcd_display_string_pos(datetime.datetime.now().strftime("%d %b %H:%M         "), 4, 0)
            data_store.appendNote(strDHTMsg + '\r\n')            
            
            
            #-------------------------------------------------------------------
            # UPLOAD 
            #-------------------------------------------------------------------
            #print "********Upload last log file**********"            
            #_dropbox.uploadLastLog()      
            #memo.appendNote("********Upload last log file**********\n")
                  
            loop = 0
            
        print "Next..."
        
        
        
    #*****************************************************************************
    # SYSTEM CATCH
    #*****************************************************************************
    except Exception as ex:
        print repr(ex)
        Running = True # True / False
    

sleep(1)
mylcd.backlight(0)
print "\nEND PROGRAM"


#--------------------------------------------------------------------------------
if __name__ == '__main__':
    pass
