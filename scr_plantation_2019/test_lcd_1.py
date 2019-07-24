# MAIN.PY

# Include  -------------------------------------------------------------------------
import RPi_I2C_driver
from time import *
import serial
import RPi.GPIO as GPIO  # <--- RPi

# Members  -------------------------------------------------------------------------
mylcd = RPi_I2C_driver.lcd(0x27)
# port_def = "/dev/ttyUSB0"
port_def = "/dev/ttyAMA0"
serial_port = serial.Serial()
# Now let's define some more custom characters
fontdata2 = [
        # Char 0 - left arrow
        [ 0x1,0x3,0x7,0xf,0xf,0x7,0x3,0x1 ],
        # Char 1 - left one bar 
        [ 0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x10 ],
        # Char 2 - left two bars
        [ 0x18,0x18,0x18,0x18,0x18,0x18,0x18,0x18 ],
        # Char 3 - left 3 bars
        [ 0x1c,0x1c,0x1c,0x1c,0x1c,0x1c,0x1c,0x1c ],
        # Char 4 - left 4 bars
        [ 0x1e,0x1e,0x1e,0x1e,0x1e,0x1e,0x1e,0x1e ],
        # Char 5 - left start
        [ 0x0,0x1,0x3,0x7,0xf,0x1f,0x1f,0x1f ],
        # Char 6 - 
        # [ ],
]

# DEF -------------------------------------------------------------------------
def setupGPIO():
    GPIO.setmode(GPIO.BCM)  # <--- RPi
    GPIO.setup(23, GPIO.OUT)
    GPIO.output(23, GPIO.HIGH)
    print "Setup GPIO..."

def setupSerial():
    try:
        serial_port = serial.Serial(port_def, baudrate=9600, timeout=0)
        time.sleep(1)
        logtext = "Initial serial port of %s..." % port_def
        print logtext    
    except:
        logtext = "ERROR: initial serial port..." 
        print logtext

def dispBar():    
    mylcd.lcd_load_custom_chars(fontdata2)    
    block = chr(255) # block character, built-in    
    mylcd.lcd_display_string_pos(block * 2,1,4)    
    pauza = 0.000001 # define duration of sleep(x)
    pos = 6
    mylcd.lcd_display_string_pos(unichr(1),1,6)
    sleep(pauza)
    
    mylcd.lcd_display_string_pos(unichr(2),1,pos)
    sleep(pauza)
    
    mylcd.lcd_display_string_pos(unichr(3),1,pos)
    sleep(pauza)
    
    mylcd.lcd_display_string_pos(unichr(4),1,pos)
    sleep(pauza)
    
    mylcd.lcd_display_string_pos(block,1,pos)
    sleep(pauza)
    
    # and another one, same as above, 1 char-space to the right
    pos = pos +1 # increase column by one
    
    mylcd.lcd_display_string_pos(unichr(1),1,pos)
    sleep(pauza)
    mylcd.lcd_display_string_pos(unichr(2),1,pos)
    sleep(pauza)
    mylcd.lcd_display_string_pos(unichr(3),1,pos)
    sleep(pauza)
    mylcd.lcd_display_string_pos(unichr(4),1,pos)
    sleep(pauza)
    mylcd.lcd_display_string_pos(block,1,pos)
    sleep(pauza)
    
    
# Setup  -------------------------------------------------------------------------
setupGPIO()
setupSerial()
Running = True
loop = 0

# Loop  -------------------------------------------------------------------------
while Running:
    try:
        print "\nLOOP: " + str(loop)        
        
        if loop > 100:
            Running = False
        
        mylcd.lcd_display_string_pos("Testing",1,1)
        mylcd.lcd_display_string_pos("Testing",2,3)
        sleep(1)
        mylcd.lcd_clear()
        
        dispBar()
        mylcd.lcd_clear()
        
        #sleep(0.1)
        loop += 1
        
        
        
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
