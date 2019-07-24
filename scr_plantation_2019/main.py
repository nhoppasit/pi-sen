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

port_def = "/dev/ttyAMA0"  # <----Rpi

#===============================================================================
# MAIN SETUP
#===============================================================================

# LCD
#mylcd = RPi_I2C_driver.lcd(0x3F)
mylcd = RPi_I2C_driver.lcd(0x27)

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
        
        # ----------
        sleep(2)
        
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
