'''
Created on May 1, 2017

@author: Red file
'''

import os
import datetime
import subprocess

#---------------------------------------------
# LOG FILE
#---------------------------------------------

#***Log file name should has date text.

log_path = "/home/multiply/memo"
file_log_target_1 = "/home/multiply/memo/data_"
delete_cmd = ['rm']

def checkNoteFolder():
    try:
        if not os.path.isdir(log_path):        
            os.mkdir(log_path)
    except Exception as ex:
        print repr(ex)




def checkmemo1():
    global file_log_target_1
    idtext = "1"
    checkNoteFolder()    
    try:
        datetext = datetime.datetime.now().strftime("%Y%b%d")
        file_log_target_1 = "/home/multiply/memo/data_" + datetext + ".csv"
        if not os.path.isfile(file_log_target_1):            
            fo = open(file_log_target_1, "w+")
            fo.close()
            logtext = "Create %s file OK." % file_log_target_1 
            print logtext
            
    except Exception as ex:
        print repr(ex)
    

checkMemoFolder = {1: checkmemo1}

# .................................................

def memo1(text):
    fo = open(file_log_target_1, "a")
    fo.write(datetime.datetime.now().strftime("%a, %d %b %Y, %H:%M:%S.%f, "))
    fo.write(text)
    fo.close()

TargetMemo = {1: memo1}    
    


# .................................................

#-----------------------------------------------------------
# Log system
#-----------------------------------------------------------

system_note_file = "/home/multiply/memo/data_"

def checkSystemNote():
    global system_note_file    
    checkNoteFolder()    
    try:
        datetext = datetime.datetime.now().strftime("%Y%b%d")
        system_note_file = "/home/multiply/memo/data_" + datetext + ".csv"
        if not os.path.isfile(system_note_file):
            fo = open(system_note_file, "w+")
            fo.close()
            logtext = "Create %s file OK." % system_note_file 
            print logtext
            
    except Exception as ex:
        print repr(ex)


    
    
def appendNote(text):
    fo = open(system_note_file, "a")
    fo.write(text)
    fo.close()

def writeState(text):
    fo = open("/home/multiply/memo/current state.html", "w")
    fo.write("<!DOCTYPE html>" + '\r\n')
    fo.write("<html>" + '\r\n')
    fo.write("<head>" + '\r\n')
    fo.write('<meta charset="UTF-8">' + '\r\n')
    fo.write("<title>Farm Box Demo Station</title>" + '\r\n')
    fo.write("</head>" + '\r\n')
    fo.write("<body>" + '\r\n')
    fo.write("<h1>Farm Box Demostrate Station</h1>" + '\r\n')
    fo.write(datetime.datetime.now().strftime("%a, %d %b %Y, %H:%M:%S "))
    fo.write(text)
    fo.write("</body>" + '\r\n')
    fo.write("</html>")
    fo.close()


def deleteOldNote():
    
    try:        
        try:        
            cmd = delete_cmd
            oldFileName = "/home/multiply/memo/*.*"
            cmd.append(oldFileName)
            out = subprocess.check_output(cmd)
            print out                    
        except:
            pass
        
    except Exception as ex:
        print repr(ex)
        
        
   
