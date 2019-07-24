import RPi.GPIO as GPIO  # <--- RPi
import time
from time import *

MATRIX = [ [1, 2, 3, 4],
           [5, 6, 7, 8],
           [9, 0, 'A', 'B'],
           ['C', 'D', 'E', 'F'] ]

ROW = [12, 16, 20, 21]
#COL = [6,  13, 19, 26]
COL = [26, 19, 13, 6]

def setupGPIO():
    GPIO.setmode(GPIO.BCM)  # <--- RPi

def clean():
    GPIO.cleanup()

def setAsOutput(pin):
    GPIO.setup(pin, GPIO.OUT)        

def onPin(pin):
    GPIO.output(pin, 0)

def offPin(pin):    
    GPIO.output(pin, 1)
        
def trackKey(lcd,text1,text2,text3,text4,iline,ipos,wait):   
    now = time()
    elap = now + 10
    elap2 = now + 1    
    buffKey = ""
    pos = 0
    
    if wait:
        lcd.lcd_clear()
        if not text1=="":
            lcd.lcd_display_string_pos(text1, 1, 0)
        if not text2=="":
            lcd.lcd_display_string_pos(text2, 2, 0)
        if not text3=="":
            lcd.lcd_display_string_pos(text3, 3, 0)
        if not text4=="":
            lcd.lcd_display_string_pos(text4, 4, 0)        
        pos = ipos
        print "Wait for key..."                    


    for j in range(4):
        GPIO.setup(COL[j], GPIO.OUT)
        GPIO.output(COL[j], 1)
        
    for i in range(4):
        GPIO.setup(ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    try:        
        while True:                               
            if wait and (time() > elap):
                lcd.lcd_clear()
                if not text1=="":
                    lcd.lcd_display_string_pos(text1, 1, 0)
                if not text2=="":
                    lcd.lcd_display_string_pos(text2, 2, 0)
                if not text3=="":
                    lcd.lcd_display_string_pos(text3, 3, 0)
                if not text4=="":
                    lcd.lcd_display_string_pos(text4, 4, 0)                            
                lcd.lcd_display_string_pos("Time out", iline, ipos)
                print "Time out."
                sleep(3)
                lcd.lcd_clear()
                return ""
            
            if (not wait) and (time() > elap2):
                return "" 
                        
            for j in range(4):
                GPIO.output(COL[j], 0)                
                for i in range(4):
                    if GPIO.input(ROW[i]) == 0:                                               
                        now = time()
                        elap = now + 10                                                                                             
                        if pos == 0:
                            lcd.lcd_clear()
                            if not text1=="":
                                lcd.lcd_display_string_pos(text1, 1, 0)
                            if not text2=="":
                                lcd.lcd_display_string_pos(text2, 2, 0)
                            if not text3=="":
                                lcd.lcd_display_string_pos(text3, 3, 0)
                            if not text4=="":
                                lcd.lcd_display_string_pos(text4, 4, 0)                            
                            pos = ipos
                            print "Wait for key..." 
                                                                 
                                   
                        print MATRIX[i][j] #echo
                        
                        if MATRIX[i][j] == 'A':
                            pos = pos - 1
                            lcd.lcd_display_string_pos(' ', iline, pos)
                            buffKey = buffKey[:-1]
                            wait = True
                            print buffKey
                        elif MATRIX[i][j] == 'B':
                            pos = pos - 1
                            lcd.lcd_display_string_pos(' ', iline, pos)
                            buffKey = buffKey[:-1]
                            wait = True
                            print buffKey
                        elif MATRIX[i][j] == 'C':
                            while GPIO.input(ROW[i]) == 0:
                                pass
                            print "Cancel"
                            lcd.lcd_clear()
                            return ""
                        elif MATRIX[i][j] == 'D':
                            while GPIO.input(ROW[i]) == 0:
                                pass
                            print "Done"
                            return buffKey
                        elif MATRIX[i][j] == 'E':
                            while GPIO.input(ROW[i]) == 0:
                                pass
                            print "Done"
                            return buffKey
                        elif MATRIX[i][j] == 'F':
                            while GPIO.input(ROW[i]) == 0:
                                pass
                            print "Done"
                            return buffKey
                        else:
                            lcd.lcd_display_string_pos(str(MATRIX[i][j]), iline, pos)
                            buffKey = buffKey + str(MATRIX[i][j])
                            wait = True
                            pos = pos + 1
                            print buffKey                           

                        while GPIO.input(ROW[i]) == 0:
                            pass
                        
                    sleep(0.001000)
                
                GPIO.output(COL[j], 1)                
        
    except KeyboardInterrupt:
        GPIO.cleanup()
        return ""
    

        