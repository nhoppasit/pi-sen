# MAIN.PY

# Include  -------------------------------------------------------------------------
import RPi_I2C_driver
from time import *
import thegpio
import thread


# Setup  -------------------------------------------------------------------------
thegpio.setupGPIO()
print "Setup GPIO...\n"

# Members  -------------------------------------------------------------------------
mylcd = RPi_I2C_driver.lcd(0x3F)
mylcd.lcd_clear()
mylcd.backlight(1)        

# Loop  -------------------------------------------------------------------------
def pulling():
    Running = True
    loop = 0

    while Running:
        try:
            print "\nLOOP: " + str(loop)        
            
            if loop > 100:
                Running = False        
            
            mylcd.lcd_clear()
            #mylcd.dispBar()
            
            mylcd.lcd_clear()
            mylcd.lcd_display_string_pos("~ BIG DIGIT ~", 2, 1)
            mylcd.lcd_display_string_pos("Menu, press any key", 3, 1)
            
            print "Introduce...\n"
                    
            key = thegpio.trackKey(mylcd)
            print "Key is %s." % key
            
            if key == "":           
                print "Empty..."        
                mylcd.lcd_clear()
                mylcd.lcd_display_string_pos("~ BIG DIGIT ~", 2, 1)
                mylcd.lcd_display_string_pos("Menu, press any key", 3, 1)
            else:
                print "Check key..."
                mylcd.lcd_clear()
                mylcd.lcd_display_string_pos("Check key...",2 , 4)
                sleep(1)
                #door = locker_request.reqA(myled, mylcd, key)              
                if 1 > 0:
                    mylcd.lcd_clear()
                    mylcd.lcd_display_string_pos("Door [%d]" %  4, 1, 1)
                    mylcd.lcd_display_string_pos("Shut the door.", 2, 1)
                    
                mylcd.lcd_clear()
                mylcd.lcd_display_string_pos("SMART LOCKER", 1, 1)
                mylcd.lcd_display_string_pos("Loading...", 2, 1)
            
            print "Next..."
            loop += 1
            sleep(0.1)       
            
            
        #*****************************************************************************
        # SYSTEM CATCH
        #*****************************************************************************
        except Exception as ex:
            print repr(ex)
            thegpio.clean()
            mylcd.lcd_clear()
            Running = False 
        
    
    # END PROGRAM"   
    
    mylcd.lcd_clear()
    mylcd.backlight(0)
    print "\nEND PROGRAM"


thread.start_new_thread(pulling(), [])
#thread.start_new_thread(led_state(), [])


#--------------------------------------------------------------------------------
if __name__ == '__main__':
    pass
