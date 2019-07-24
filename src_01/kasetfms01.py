import json
import datetime
import uart
from time import *
import serial  # <----Rpi
import memo
import data_store
import data_store_forward
from suds.client import Client

#--------------------------------------------------------------
# Check logging...
# Start new log file a day.
#--------------------------------------------------------------

memo.checkSystemNote()
memo.checkNoteFolder()
memo.checkMemoFolder[1]()

data_store.checkSystemNote()
data_store.checkNoteFolder()

data_store_forward.checkSystemNote()
data_store_forward.checkNoteFolder()

#---------------------------------------------
# Program header
#---------------------------------------------

print "\n\n\n"
print "***************************************************************"
print " KASET FMS"
print " (c)2018, Designed by RED LASER"
print "***************************************************************"
memo.appendNote("***************************************************************\n")
memo.appendNote(" KASET FMS\n")
memo.appendNote("***************************************************************\n")

urlPush = 'http://api.kasetfms.com/Onfield.asmx?WSDL';

#===============================================================================
# MAIN SETUP
#===============================================================================

serviceState = -2;
try:
    cl = Client(urlPush, timeout=10)
    print 'Service success\n'
    memo.appendNote('Service success\n');
    serviceState = 0;
    
except Exception as ex:
    print 'Service failed\n'
    memo.appendNote('Service failed\n');    

#---------------------------------------------
# port detection
#---------------------------------------------
port_def = "/dev/ttyS0"  # <----Rpi

sensor = serial.Serial(port_def);
sensor.baudrate = 9600;
sleep(1);

# address
adds = ['23','23','23','23','23','23','23','23','23']
idx = 0;

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
        print len(adds)
        
        for idx in range(len(adds)):        
            try:
                idx = idx + 1;
                if idx>9:
                    idx = 0;
             
                sensor.write(':13%s00051000|#' % adds[idx]);
                sleep(1)
                aptext = sensor.read(sensor.inWaiting());
                print aptext
                
                sensor.write(':13%s00152000|#' % adds[idx]);
                sleep(1)
                aptext = sensor.read(sensor.inWaiting());
                print aptext
                            
            except Exception as exap:
                aptext = repr(exap);
            
            message = datetime.datetime.now().strftime("%a %d %b %Y %H:%M:%S.%f, ") + aptext
            print message
                    
            # ----------
            # Store & Push 
            # ----------
            print "Updating data file."        
            data_store.appendNote(message + '}\r\n')            
            data_store_forward.appendNote(message + '}')            
            rtxt = data_store_forward.read() 
            print rtxt

            # forward loop
            artxt = rtxt.split("}")
            print len(artxt)
            print artxt
                                   
            # delete forward file
            try:
                sleep(1)
                data_store_forward.renew()()
            except Exception as exap:
                print repr(exap);
            
            # -----------
            # Push state online
            # -----------                    
            for sfi in range(len(artxt)-1):                
                if 10<sfi:
                    break;                
                print "Forwarding..."                   
                print artxt[sfi]                 
                if serviceState!=0:
                    try:
                        cl = Client(urlPush, timeout=10)
                        print 'Service success\n'
                        memo.appendNote('Service success\n');
                        serviceState = 0;
                        
                    except Exception as ex:
                        print 'Service failed\n'
                        memo.appendNote('Service failed\n');
                        serviceState = -2;
                
                try:
                    message = artxt[sfi]
                    ret = cl.service.Push(adds[idx] , 'push', message)
                    print ret
                    memo.appendNote(ret + '\r\n')
                    serviceState = 0; 
                    
                    if ret!="OK":
                        data_store_forward.appendNote(message+"}")                   
                    
                except Exception as ex:
                    print 'Service failed\n'
                    memo.appendNote('Service failed\n');
                    serviceState = -2;
                    data_store_forward.appendNote(message+"}")
                
                sleep(1)
            
            # ------------------------------------------------------------------------
            # LOOP SLEEP and NEXT LOOP
            # Use without KEYPAD
            # ------------------------------------------------------------------------
            # ----------
            # Loop sleep
            # ----------
            print "Next..."
            sleep(1)
        
        # end of for adds
        
    #*****************************************************************************
    # SYSTEM CATCH
    #*****************************************************************************
    except Exception as ex:
        print repr(ex)
        memo.appendNote(repr(ex) + '\r\n')
        Running = True # True / False
        sleep(2)
    

sleep(1)
print "\nEND PROGRAM"

#--------------------------------------------------------------------------------
if __name__ == '__main__':
    pass
