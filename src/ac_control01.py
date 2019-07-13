from time import *
import memo
import uart
import thegpio

nTARGET = 1

TARGET_NBR = ':'

TIME_SUF = "?0]\r"

# rtc.adjust(DateTime(2016, 12, 29, 19, 23, 00));
SET_YEAR_CMD = "[51"
SET_MONTH_CMD = "[32"
SET_DAY_CMD = "[33"
SET_HOUR_CMD = "[34"
SET_MINUTE_CMD = "[35"
SET_SECOND_CMD = "[36"

ETX_SUF = "]\r"


def getTime(serial_port):
    try:
        
        MSG = TARGET_NBR + TIME_SUF
        logtext = "...........Read .........." 
        print logtext
        memo.appendNote(logtext + '\n') 
    
        print "<< " + MSG
        memo.TargetMemo[nTARGET]("<< " + MSG + '\n')        
        serial_port.write(MSG)
        rcv = uart.readlineCR(serial_port)
        memo.TargetMemo[nTARGET](">> " + ''.join(rcv) + '\n')
        print ">> " + ''.join(rcv)
    
        # print rcv
        # print len(rcv)
        memo.appendNote(''.join(rcv) + '\n')
        
        # incomming pattern
        # [ 0         2    3              6         8              11            14             17             20             23                
        # ['*', ':', '?', '2', '0', '1', '7', '|', '0', '6', '|', '1', '1', '|', '1', '5', '|', '0', '3', '|', '3', '9', '|', '0', '3', '6']
        # Length = 26
        
        if len(rcv)==26 and ''.join(rcv[0:3])=="*:?":                
            serial_port.write(uart.ACK)
            
            # Check return message
            strYear   = ''.join(rcv[3:7])
            strMonth  = ''.join(rcv[8:10])
            strDay    = ''.join(rcv[11:13]) 
            strHour   = ''.join(rcv[14:16])
            strMinute = ''.join(rcv[17:19])
            strSecond = ''.join(rcv[20:22])
            iRelayState = int(''.join(rcv[23:26]))            
            return strYear, strMonth, strDay, strHour, strMinute, strSecond, iRelayState
        
        else:
            serial_port.write(uart.NAK)      
            return rcv
        
    except Exception as ex:
        print repr(ex)
        memo.appendNote(repr(ex) + '\n')        
        raise ex  
    
def setYear(serial_port,valText):
    try:
        
        MSG = TARGET_NBR + SET_YEAR_CMD + valText + ETX_SUF
        logtext = "........... SET YEAR to TIMERRY..........." 
        print logtext
        memo.appendNote(logtext + '\n') 
    
        print "<< " + MSG
        memo.TargetMemo[nTARGET]("<< " + MSG + '\n')        
        serial_port.write(MSG)
        rcv = uart.readlineCR(serial_port)
        memo.TargetMemo[nTARGET](">> " + ''.join(rcv) + '\n')
        print ">> " + ''.join(rcv)
    
        print rcv
        print len(rcv)
        memo.appendNote(''.join(rcv) + '\n')
        
        # incomming pattern
        # *:[2017*
        # Length = 8
        
        if len(rcv)==8 and ''.join(rcv[0:3])=="*:[":                
            serial_port.write(uart.ACK)   
            print "Send ACK"                 
            return True
        
        else:
            print "Send NAK"
            serial_port.write(uart.NAK)      
            return False
        
    except Exception as ex:
        print repr(ex)
        memo.appendNote(repr(ex) + '\n')        
        raise ex  
    
def setMonth(serial_port,valText):
    try:        
        MSG = TARGET_NBR + SET_MONTH_CMD + valText + ETX_SUF
        logtext = "........... SET MONTH to TIMERRY..........." 
        print logtext
        memo.appendNote(logtext + '\n') 
    
        print "<< " + MSG
        memo.TargetMemo[nTARGET]("<< " + MSG + '\n')        
        serial_port.write(MSG)
        rcv = uart.readlineCR(serial_port)
        memo.TargetMemo[nTARGET](">> " + ''.join(rcv) + '\n')
        print ">> " + ''.join(rcv)
    
        print rcv
        print len(rcv)
        memo.appendNote(''.join(rcv) + '\n')
        
        # incomming pattern
        # *:[5*, *:[11*
        # Length = 5,6
        
        if (len(rcv)==5 or len(rcv)==6) and ''.join(rcv[0:3])=="*:[":                
            serial_port.write(uart.ACK)   
            print "Send ACK"                 
            return True
        
        else:
            print "Send NAK"
            serial_port.write(uart.NAK)      
            return False
        
    except Exception as ex:
        print repr(ex)
        memo.appendNote(repr(ex) + '\n')        
        raise ex  
        
def setDay(serial_port,valText):
    try:        
        MSG = TARGET_NBR + SET_DAY_CMD + valText + ETX_SUF
        logtext = "........... SET DAY to TIMERRY..........." 
        print logtext
        memo.appendNote(logtext + '\n') 
    
        print "<< " + MSG
        memo.TargetMemo[nTARGET]("<< " + MSG + '\n')        
        serial_port.write(MSG)
        rcv = uart.readlineCR(serial_port)
        memo.TargetMemo[nTARGET](">> " + ''.join(rcv) + '\n')
        print ">> " + ''.join(rcv)
    
        print rcv
        print len(rcv)
        memo.appendNote(''.join(rcv) + '\n')
        
        # incomming pattern
        # *:[5*, *:20*
        # Length = 5,6
        
        if (len(rcv)==5 or len(rcv)==6) and ''.join(rcv[0:3])=="*:[":                
            serial_port.write(uart.ACK)   
            print "Send ACK"                 
            return True
        
        else:
            print "Send NAK"
            serial_port.write(uart.NAK)      
            return False
        
    except Exception as ex:
        print repr(ex)
        memo.appendNote(repr(ex) + '\n')        
        raise ex  

def setHour(serial_port,valText):
    try:        
        MSG = TARGET_NBR + SET_HOUR_CMD+ valText + ETX_SUF
        logtext = "........... SET HOUR to TIMERRY..........." 
        print logtext
        memo.appendNote(logtext + '\n') 
    
        print "<< " + MSG
        memo.TargetMemo[nTARGET]("<< " + MSG + '\n')        
        serial_port.write(MSG)
        rcv = uart.readlineCR(serial_port)
        memo.TargetMemo[nTARGET](">> " + ''.join(rcv) + '\n')
        print ">> " + ''.join(rcv)
    
        print rcv
        print len(rcv)
        memo.appendNote(''.join(rcv) + '\n')
        
        # incomming pattern
        # *:[5*, *:20*
        # Length = 5,6
        
        if (len(rcv)==5 or len(rcv)==6) and ''.join(rcv[0:3])=="*:[":                
            serial_port.write(uart.ACK)   
            print "Send ACK"                 
            return True
        
        else:
            print "Send NAK"
            serial_port.write(uart.NAK)      
            return False
        
    except Exception as ex:
        print repr(ex)
        memo.appendNote(repr(ex) + '\n')        
        raise ex  

def setMinute(serial_port,valText):
    try:        
        MSG = TARGET_NBR + SET_MINUTE_CMD + valText + ETX_SUF
        logtext = "........... SET MINUTE to TIMERRY..........." 
        print logtext
        memo.appendNote(logtext + '\n') 
    
        print "<< " + MSG
        memo.TargetMemo[nTARGET]("<< " + MSG + '\n')        
        serial_port.write(MSG)
        rcv = uart.readlineCR(serial_port)
        memo.TargetMemo[nTARGET](">> " + ''.join(rcv) + '\n')
        print ">> " + ''.join(rcv)
    
        print rcv
        print len(rcv)
        memo.appendNote(''.join(rcv) + '\n')
        
        # incomming pattern
        # *:[5*, *:20*
        # Length = 5,6
        
        if (len(rcv)==5 or len(rcv)==6) and ''.join(rcv[0:3])=="*:[":                
            serial_port.write(uart.ACK)   
            print "Send ACK"                 
            return True
        
        else:
            print "Send NAK"
            serial_port.write(uart.NAK)      
            return False
        
    except Exception as ex:
        print repr(ex)
        memo.appendNote(repr(ex) + '\n')        
        raise ex  
                                              
def setSecond(serial_port,valText):
    try:        
        MSG = TARGET_NBR + SET_SECOND_CMD + valText + ETX_SUF
        logtext = "........... SET SECOND to TIMERRY..........." 
        print logtext
        memo.appendNote(logtext + '\n') 
    
        print "<< " + MSG
        memo.TargetMemo[nTARGET]("<< " + MSG + '\n')        
        serial_port.write(MSG)
        rcv = uart.readlineCR(serial_port)
        memo.TargetMemo[nTARGET](">> " + ''.join(rcv) + '\n')
        print ">> " + ''.join(rcv)
    
        print rcv
        print len(rcv)
        memo.appendNote(''.join(rcv) + '\n')
        
        # incomming pattern
        # *:[5*, *:20*
        # Length = 5,6
        
        if (len(rcv)==5 or len(rcv)==6) and ''.join(rcv[0:3])=="*:[":                
            serial_port.write(uart.ACK)   
            print "Send ACK"                 
            return True
        
        else:
            print "Send NAK"
            serial_port.write(uart.NAK)      
            return False
        
    except Exception as ex:
        print repr(ex)
        memo.appendNote(repr(ex) + '\n')        
        raise ex  


               
def setDateTime(serial_port,lcd,key):
    iProg = 0        
    if not (key == ""):
        lcd.lcd_display_string_pos("Check key...     ",4,4)
        print "Check key..."                    
        memo.appendNote("Check key...\n")                       
        try:
            iProg = int(key)
        except Exception as ex:
            print repr(ex)                
            iProg = 0                
        
        if iProg>0:            
            textLog = "Program is %d." % iProg
            print textLog
            memo.appendNote(textLog + '\n')
            
            # ------------ 1. SET YEAR ------------------
            if iProg == 1:
                print "SET YEAR..."
                memo.appendNote("SET YEAR...\n")                    
                key = thegpio.trackKey(lcd,
                                       "    THE PROFILER",
                                       "",
                                       "SET YEAR: ",
                                       "",
                                       3,10,True) # 1.0 Sec scanning
                iVal = 0
                if not(key==""):
                    textLog = "Check year number..."
                    print textLog
                    memo.appendNote(textLog + '\n')
                    try:
                        iVal = int(key)
                    except Exception as ex:
                        print repr(ex)
                        iVal=0
                    if 2016<iVal and iVal<=9999:
                        lcd.lcd_display_string_pos("Setting...",4,10)
                        if setYear(serial_port, "%04d" % iVal):
                            lcd.lcd_display_string_pos("                Done",4,0)
                        else:
                            lcd.lcd_display_string_pos("Fail!     ",4,11)
                        sleep(2)
                            
                    else:
                        lcd.lcd_display_string_pos("Invalid!",4,11)
                        sleep(2)
                
            # ------------ 2. SET MONTH ------------------
            if iProg == 2:
                print "SET MONTH..."
                memo.appendNote("SET MONTH...\n")                    
                key = thegpio.trackKey(lcd,
                                       "    THE PROFILER",
                                       "",
                                       "SET MONTH: ",
                                       "",
                                       3,11,True) # 1.0 Sec scanning
                iVal = 0
                if not(key==""):
                    textLog = "Check month number..."
                    print textLog
                    memo.appendNote(textLog + '\n')
                    try:
                        iVal = int(key)
                    except Exception as ex:
                        print repr(ex)
                        iVal=0
                    if 1<=iVal and iVal<=12:
                        lcd.lcd_display_string_pos("Setting...",4,10)
                        if setMonth(serial_port, "%02d" % iVal):
                            lcd.lcd_display_string_pos("                Done",4,0)
                        else:
                            lcd.lcd_display_string_pos("Fail!     ",4,11)
                        sleep(2)
                            
                    else:
                        lcd.lcd_display_string_pos("Invalid!",4,11)
                        sleep(2)

            # ------------ 3. SET DAY ------------------
            if iProg == 3:
                print "SET DAY..."
                memo.appendNote("SET DAY...\n")                    
                key = thegpio.trackKey(lcd,
                                       "    THE PROFILER",
                                       "",
                                       "SET DAY: ",
                                       "",
                                       3,9,True) # 1.0 Sec scanning
                iVal = 0
                if not(key==""):
                    textLog = "Check day number..."
                    print textLog
                    memo.appendNote(textLog + '\n')
                    try:
                        iVal = int(key)
                    except Exception as ex:
                        print repr(ex)
                        iVal=0
                    if 1<=iVal and iVal<=31:
                        lcd.lcd_display_string_pos("Setting...",4,10)
                        if setDay(serial_port, "%02d" % iVal):
                            lcd.lcd_display_string_pos("                Done",4,0)
                        else:
                            lcd.lcd_display_string_pos("Fail!     ",4,11)
                        sleep(2)
                            
                    else:
                        lcd.lcd_display_string_pos("Invalid!",4,11)
                        sleep(2)
                                    
            # ------------ 4. SET HOUR ------------------
            if iProg == 4:
                print "SET HOUR..."
                memo.appendNote("SET HOUR...\n")                    
                key = thegpio.trackKey(lcd,
                                       "    THE PROFILER",
                                       "",
                                       "SET HOUR: ",
                                       "",
                                       3,10,True) # 1.0 Sec scanning
                iVal = 0
                if not(key==""):
                    textLog = "Check hour number..."
                    print textLog
                    memo.appendNote(textLog + '\n')
                    try:
                        iVal = int(key)
                    except Exception as ex:
                        print repr(ex)
                        iVal=0
                    if 0<=iVal and iVal<=23:
                        lcd.lcd_display_string_pos("Setting...",4,10)
                        if setHour(serial_port, "%02d" % iVal):
                            lcd.lcd_display_string_pos("                Done",4,0)
                        else:
                            lcd.lcd_display_string_pos("Fail!     ",4,11)
                        sleep(2)
                            
                    else:
                        lcd.lcd_display_string_pos("Invalid!",4,11)
                        sleep(2)
                                   
            # ------------ 5. SET MINUTE ------------------
            if iProg == 5:
                print "SET MINUTE..."
                memo.appendNote("SET MINUTE...\n")                    
                key = thegpio.trackKey(lcd,
                                       "    THE PROFILER",
                                       "",
                                       "SET MINUTE: ",
                                       "",
                                       3,12,True) # 1.0 Sec scanning
                iVal = 0
                if not(key==""):
                    textLog = "Check minute number..."
                    print textLog
                    memo.appendNote(textLog + '\n')
                    try:
                        iVal = int(key)
                    except Exception as ex:
                        print repr(ex)
                        iVal=0
                    if 0<=iVal and iVal<=59:
                        lcd.lcd_display_string_pos("Setting...",4,10)
                        if setMinute(serial_port, "%02d" % iVal):
                            lcd.lcd_display_string_pos("                Done",4,0)
                        else:
                            lcd.lcd_display_string_pos("Fail!     ",4,11)
                        sleep(2)
                            
                    else:
                        lcd.lcd_display_string_pos("Invalid!",4,11)
                        sleep(2)
                                   
            # ------------ 6. SET SECOND ------------------
            if iProg == 6:
                print "SET SECOND..."
                memo.appendNote("SET SECOND...\n")                    
                key = thegpio.trackKey(lcd,
                                       "    THE PROFILER",
                                       "",
                                       "SET SECOND: ",
                                       "",
                                       3,12,True) # 1.0 Sec scanning
                iVal = 0
                if not(key==""):
                    textLog = "Check second number..."
                    print textLog
                    memo.appendNote(textLog + '\n')
                    try:
                        iVal = int(key)
                    except Exception as ex:
                        print repr(ex)
                        iVal=0
                    if 0<=iVal and iVal<=59:
                        lcd.lcd_display_string_pos("Setting...",4,10)
                        if setSecond(serial_port, "%02d" % iVal):
                            lcd.lcd_display_string_pos("                Done",4,0)
                        else:
                            lcd.lcd_display_string_pos("Fail!     ",4,11)
                        sleep(2)
                            
                    else:
                        lcd.lcd_display_string_pos("Invalid!",4,11)
                        sleep(2)
                                   
                                                  
                                                                              
        # Clear lcd once
        lcd.lcd_clear()                            
        