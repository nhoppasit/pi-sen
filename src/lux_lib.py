from time import *
import memo
import uart

nTARGET = 1

TARGET_NBR = '+'

QUERY_SUF = "?0]\r"

# rtc.adjust(DateTime(2016, 12, 29, 19, 23, 00));

ETX_SUF = "]\r"


def getState(serial_port):
    try:
        
        MSG = TARGET_NBR + QUERY_SUF
        logtext = "...........Read DHTs .........." 
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
        # [ 0         2    3              6         8              11            14             17             20             23                
        # ['*', ':', '?', '2', '0', '1', '7', '|', '0', '6', '|', '1', '1', '|', '1', '5', '|', '0', '3', '|', '3', '9', '|', '0', '3', '6']
        # Length = 26
        
        if ''.join(rcv[0:3])=="*+?":                
            serial_port.write(uart.ACK)
            
            # Check return message
            if(4<=len(rcv) and len(rcv)<=6):                
                if(len(rcv)==4):
                    lx = ''.join(rcv[3:4])
                    return lx
    
                if(len(rcv)==5):
                    lx = ''.join(rcv[3:5])
                    return lx
    
                if(len(rcv)==6):
                    lx = ''.join(rcv[3:6])
                    return lx
            else:
                return '0'
            
        else:
            serial_port.write(uart.NAK)      
            return rcv
        
    except Exception as ex:
        print repr(ex)
        memo.appendNote(repr(ex) + '\n')        
        raise ex  
    