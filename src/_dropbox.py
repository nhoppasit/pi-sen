import os
import datetime
import time
import hashlib
import subprocess
import memo

# arch_name_template = "{0}.7z"
# arch_cmd_template = ['7z', 'a', '-mx1', '-l' ,'-p{password}', '{filename}', '{backup}']
# arch_cmd_template = ['rar', 'a', '-p{password}', '{filename}', '{backup}']
# arch_cmd_template = ['tar',  '-vczf', '{filename}', '{backup}']
# arch_cmd_template = ['tar', '-vcjf', '{filename}', '{backup}']
# upload_cmd = ['/home/multiply/Dropbox-Uploader/dropbox_uploader.sh' , '-f/home/multiply/.dropbox_uploader', 'upload']
upload_cmd = ['/home/multiply/Dropbox-Uploader/dropbox_uploader.sh' , 'upload']
delete_cmd = ['/home/multiply/Dropbox-Uploader/dropbox_uploader.sh' , 'delete']
#zip_name = '/home/jia/log/ziplog.gz'
#delete_cmd = ['rm', '/home/jia/log/ziplog.gz']
log_path = "/home/multiply/memo"

def uploadLastLog():
    try:
        # local log file.
        datetext = (datetime.datetime.now()).strftime("%Y%b%d")                
        dbxFileName = "data_%s.csv" % (datetext)
        dbxFullFileName = '/%s/%s' % ('test', dbxFileName)# dropbox path and file.
        
        localFileName = "data_%s.csv" % (datetext)
        localFullFileName = "%s/%s" % (log_path, localFileName)          
            
        try:                        
            print 'Uploading...\n'          
            memo.appendNote("Uploading")
            
            upload_cmd = ['/home/multiply/Dropbox-Uploader/dropbox_uploader.sh' , 'upload']
            delete_cmd = ['/home/multiply/Dropbox-Uploader/dropbox_uploader.sh' , 'delete']

            upload_cmd.append(localFullFileName)
            upload_cmd.append(dbxFullFileName)
            
            delete_cmd.append(dbxFullFileName)
            
            print "%s\n" % (delete_cmd)
            print "%s\n" % (upload_cmd)
            
           
            
            print "%s\n" % (upload_cmd)
            memo.appendNote(upload_cmd)
            
            out = subprocess.check_output(upload_cmd) # Upload
            #print out        
            #memo.appendNote(out)        
        
                        
        except Exception as err:
            print repr(err)
    
    except Exception as ex:
        print repr(ex)


if __name__ == '__main__':
    uploadLastLog()
