'''
Created on Jul 3, 2018

@author: Nhoppasit-PC2
'''
import thegpio
from time import sleep

thegpio.setupGPIO()

ryPin = [4,17,18,27,22,23,24,25]

for idx in range(8):
    thegpio.setAsOutput(ryPin[idx])
    thegpio.offPin(ryPin[idx])

try:
    idx = 0
    while True:
        thegpio.onPin(ryPin[idx])
        #print "ON\n"
        print "ON-RY%d {GPIO%d}\n" % (idx+1, ryPin[idx])
        sleep(5)
        
        thegpio.offPin(ryPin[idx])        
        #print "OFF\n"
        #print "OFF-%d\n" % ryPin[idx]
        print "OFF-RY%d {GPIO%d}\n" % (idx+1, ryPin[idx])
        sleep(5)
        
        idx = idx+1
        #print "Update idx.\n"
        if 2<idx:
            idx=0
          
except KeyboardInterrupt:
    thegpio.clean()
    print "END\n"          
            
