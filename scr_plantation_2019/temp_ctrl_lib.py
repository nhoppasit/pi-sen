from time import *
import memo
import uart
import thegpio

nTARGET = 1

TARGET_NBR = '~'

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
        
        if len(rcv)==42 and ''.join(rcv[0:3])=="*~?":                
            serial_port.write(uart.ACK)
            
            # Check return message
            h1 = ''.join(rcv[3:6])
            t1 = ''.join(rcv[7:10])
            h2 = ''.join(rcv[11:14]) 
            t2 = ''.join(rcv[15:18])
            h3 = ''.join(rcv[19:22])
            t3 = ''.join(rcv[23:26])
            h4 = ''.join(rcv[27:30])
            t4 = ''.join(rcv[31:34])
            return h1, t1, h2, t2, h3, t3, h4, t4
        
        else:
            serial_port.write(uart.NAK)      
            return rcv
        
    except Exception as ex:
        print repr(ex)
        memo.appendNote(repr(ex) + '\n')        
        raise ex  
    