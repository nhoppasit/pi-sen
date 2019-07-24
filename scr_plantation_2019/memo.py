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
file_log_target_1 = "/home/multiply/memo/target_1_"
file_log_target_2 = "/home/multiply/memo/target_2_"

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
        file_log_target_1 = "/home/multiply/memo/target_" + idtext + "_" + datetext + ".log"
        if not os.path.isfile(file_log_target_1):            
            fo = open(file_log_target_1, "w+")
            fo.close()
            logtext = "Create %s file OK." % file_log_target_1 
            print logtext
            appendNote(logtext + '\n')
    except Exception as ex:
        print repr(ex)
    



def checkmemo2():
    global file_log_target_2
    idtext = "2"
    checkNoteFolder()    
    try:
        datetext = datetime.datetime.now().strftime("%Y%b%d")
        file_log_target_2 = "/home/multiply/memo/target_" + idtext + "_" + datetext + ".log"
        if not os.path.isfile(file_log_target_2):
            fo = open(file_log_target_2, "w+")
            fo.close()
            logtext = "Create %s file OK." % file_log_target_2 
            print logtext
            appendNote(logtext + '\n')
    except Exception as ex:
        print repr(ex)
    
checkMemoFolder = {1: checkmemo1,
                   2: checkmemo2}

# .................................................

def memo1(text):
    return
    fo = open(file_log_target_1, "a")
    fo.write(datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S.%f : "))
    fo.write(text)
    fo.close()

def memo2(text):
    return
    fo = open(file_log_target_2, "a")
    fo.write(datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S.%f : "))
    fo.write(text)
    fo.close()

TargetMemo = {1: memo1,
           2: memo2}    
    


# .................................................

#-----------------------------------------------------------
# Log system
#-----------------------------------------------------------

system_note_file = "/home/multiply/memo/note_"

def checkSystemNote():
    global system_note_file    
    checkNoteFolder()    
    try:
        datetext = datetime.datetime.now().strftime("%Y%b%d")
        system_note_file = "/home/multiply/memo/note_" + datetext + ".log"
        if not os.path.isfile(system_note_file):
            fo = open(system_note_file, "w+")
            fo.close()
            logtext = "Create %s file OK." % system_note_file 
            print logtext
            appendNote(logtext + '\n')
    except Exception as ex:
        print repr(ex)


    
    
def appendNote(text):
    #return
    fo = open(system_note_file, "a")
    fo.write(datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S.%f : "))
    fo.write(text)
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
        
        
