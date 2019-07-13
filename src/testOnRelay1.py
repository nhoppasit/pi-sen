'''
Created on Jul 3, 2018

@author: Nhoppasit-PC2
'''

import memo

import thegpio
from time import sleep

import datetime
        
thegpio.setupGPIO()

ryPin = [4,17,18,27,22,23,24,25]

for idx in range(8):
    thegpio.setAsOutput(ryPin[idx])
    thegpio.offPin(ryPin[idx])

memo.checkSystemNote()
memo.checkNoteFolder()
memo.checkMemoFolder[1]()

memo.appendNote("***************************************************************\n")
memo.appendNote(" RELAY 01\n")
memo.appendNote("***************************************************************\n")

try:
    idx = 0
    while(True):
        try:
            now = datetime.datetime.now()
            todayOnTime = now.replace(hour=7, minute=0, second=0, microsecond=0)
            todayOffTime = now.replace(hour=18, minute=0, second=0, microsecond=0)
            if todayOnTime<now and now<todayOffTime:            
                thegpio.onPin(ryPin[idx])
                #print "ON\n"
                print "ON-RY%d {GPIO%d}\n" % (idx+1, ryPin[idx])
                memo.appendNote("ON-RY%d {GPIO%d}\n" % (idx+1, ryPin[idx]))
            else:
                thegpio.offPin(ryPin[idx])        
                #print "OFF\n"
                #print "OFF-%d\n" % ryPin[idx]
                print "OFF-RY%d {GPIO%d}\n" % (idx+1, ryPin[idx])
                memo.appendNote("OFF-RY%d {GPIO%d}\n" % (idx+1, ryPin[idx]))
            
            sleep(60);
        
        except Exception as ex:
            print repr(ex)
            memo.appendNote(repr(ex) + '\r\n')
          
except KeyboardInterrupt:
    thegpio.clean()
    print "END\n"
    memo.appendNote("RELAY 01 END\n")  
    
            
            