import RPi.GPIO as GPIO  # <--- RPi


# DEF -------------------------------------------------------------------------
def setupGPIO():
    GPIO.setmode(GPIO.BCM)  # <--- RPi
    GPIO.setup(23, GPIO.OUT)
    GPIO.output(23, GPIO.HIGH)
    print "Setup GPIO..."

    
# Setup  -------------------------------------------------------------------------
setupGPIO()

MATRIX = [ [1, 2, 3, 4],
           [5, 6, 7, 8],
           [9, 0, 'A', 'B'],
           ['C', 'D', 'E', 'F'] ]

ROW = [12, 16, 20, 21]
#COL = [6,  13, 19, 26]
COL = [26, 19, 13, 6]

for j in range(4):
    GPIO.setup(COL[j], GPIO.OUT)
    GPIO.output(COL[j], 1)
    
for i in range(4):
    GPIO.setup(ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
try:
    while True:
        for j in range(4):
            GPIO.output(COL[j], 0)
            
            for i in range(4):
                if GPIO.input(ROW[i]) == 0:
                    print MATRIX[i][j]
                    
                    while GPIO.input(ROW[i]) == 0:
                        pass
            
            GPIO.output(COL[j], 1)
        
        
except KeyboardInterrupt:
    GPIO.cleanup()
    
