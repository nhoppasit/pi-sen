from time import *
import serial  # <----Rpi
import memo
import uart
import RPi_I2C_driver
import timery
import thegpio
from unittest import case

port_def = "/dev/ttyAMA0"  # <----Rpi

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

#---------------------------------------------
# Setup GPIO
#---------------------------------------------
thegpio.setupGPIO()

#---------------------------------------------
# Serial port name
#---------------------------------------------
serial_port = serial.Serial()

try:
    serial_port = serial.Serial(port_def, baudrate=9600, timeout=0)
    sleep(1)

    logtext = "Initial serial port of %s..." % port_def
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
        # Read RTC
        # ------------------------------------------------------------------------
        strYear = "0000"
        strMonth = "00"
        strDay = "00"
        strHour = "00"
        strMinute = "00"
        strSecond = "00"
        iTimeryRelayState = 0 
        (strYear, strMonth, strDay, strHour, strMinute, strSecond, iTimeryRelayState) = timery.getTime(serial_port)
        strTimeMsg = "%s/%s/%s %s:%s:%s" % (strYear, strMonth, strDay,strHour,strMinute,strSecond)
        strTimeryRelayState = format(iTimeryRelayState, 'b')

        # ------------------------------------------------------------------------
        # Update LCD by TIMERY
        # ------------------------------------------------------------------------
        mylcd.lcd_display_string_pos(strTimeMsg, 1, 0)
        mylcd.lcd_display_string_pos("Relay: ", 2, 0)
        mylcd.lcd_display_string_pos(strTimeryRelayState, 2, 7)
        memo.appendNote("Update TIME on LCD\n")
        print "Update TIME on LCD"
        
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
        # Set date & time
        # ------------------------------------------------------------------------
        timery.setDateTime(serial_port, mylcd, key) # if key is not empty
        
        
        # ------------------------------------------------------------------------
        # LOOP SLEEP and NEXT LOOP
        # Use without KEYPAD
        # ------------------------------------------------------------------------
        # sleep(1)
        loop += 1
        print "Next..."
        
        
        
    #*****************************************************************************
    # SYSTEM CATCH
    #*****************************************************************************
    except Exception as ex:
        print repr(ex)
        Running = False
    

sleep(1)
mylcd.backlight(0)
print "\nEND PROGRAM"


#--------------------------------------------------------------------------------
if __name__ == '__main__':
    pass
