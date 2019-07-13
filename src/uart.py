import time

ACK = '*'
NAK = '!'
ETX = '\r'



#---------------------------------------------
# READ: Serial port routine of slot communication
#---------------------------------------------

def readlineCR(serial_port):    
    i = 0
    rv = []
    ACK_Byte = False

    print "readlineCR"
    while True:
        time.sleep(0.01)
        ch = serial_port.read()
        i += 1        
                
        if ch == ACK or ch == NAK:
            ACK_Byte = True
            print "ACK/NAK come."  # <--- RPi
            
        if ACK_Byte and '\x20' <= ch and ch <= '\x7e':
            rv.append(ch);

        if ACK_Byte and (ch == ETX or ch == NAK):
            print ch
            return rv

        if i > 43:  
            print "OVERFLOW"          
            return rv

