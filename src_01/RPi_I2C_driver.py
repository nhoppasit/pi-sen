# -*- coding: utf-8 -*-
"""
Compiled, mashed and generally mutilated 2014-2015 by Denis Pleic
Made available under GNU GENERAL PUBLIC LICENSE

# Modified Python I2C library for Raspberry Pi
# as found on http://www.recantha.co.uk/blog/?p=4849
# Joined existing 'i2c_lib.py' and 'lcddriver.py' into a single library
# added bits and pieces from various sources
# By DenisFromHR (Denis Pleic)
# 2015-02-10, ver 0.1

"""
#
import i2c
#
from time import *


# LCD Address
# ADDRESS = 0x27

# commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

# flags for backlight control
LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00

En = 0b00000100 # Enable bit
Rw = 0b00000010 # Read/Write bit
Rs = 0b00000001 # Register select bit

fontdata2 = [
        # Char 0 - left arrow
        [ 0x1,0x3,0x7,0xf,0xf,0x7,0x3,0x1 ],
        # Char 1 - left one bar 
        [ 0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x10 ],
        # Char 2 - left two bars
        [ 0x18,0x18,0x18,0x18,0x18,0x18,0x18,0x18 ],
        # Char 3 - left 3 bars
        [ 0x1c,0x1c,0x1c,0x1c,0x1c,0x1c,0x1c,0x1c ],
        # Char 4 - left 4 bars
        [ 0x1e,0x1e,0x1e,0x1e,0x1e,0x1e,0x1e,0x1e ],
        # Char 5 - left start
        [ 0x0,0x1,0x3,0x7,0xf,0x1f,0x1f,0x1f ],
        # Char 6 - 
        # [ ],
        ]

class lcd:
    #initializes objects and lcd
    def __init__(self, ADDRESS):
        self.lcd_device = i2c.i2c_device(ADDRESS)
        
        self.lcd_write(0x03)
        self.lcd_write(0x03)
        self.lcd_write(0x03)
        self.lcd_write(0x02)
        
        self.lcd_write(LCD_FUNCTIONSET | LCD_2LINE | LCD_5x8DOTS | LCD_4BITMODE)
        self.lcd_write(LCD_DISPLAYCONTROL | LCD_DISPLAYON)
        self.lcd_write(LCD_CLEARDISPLAY)
        self.lcd_write(LCD_ENTRYMODESET | LCD_ENTRYLEFT)
        sleep(0.2)
        
    # clocks EN to latch command
    def lcd_strobe(self, data):
        self.lcd_device.write_cmd(data | En | LCD_BACKLIGHT)
        sleep(.0005)
        self.lcd_device.write_cmd(((data & ~En) | LCD_BACKLIGHT))
        sleep(.0001)
    
    def lcd_write_four_bits(self, data):
        self.lcd_device.write_cmd(data | LCD_BACKLIGHT)
        self.lcd_strobe(data)
    
    # write a command to lcd
    def lcd_write(self, cmd, mode=0):
        self.lcd_write_four_bits(mode | (cmd & 0xF0))
        self.lcd_write_four_bits(mode | ((cmd << 4) & 0xF0))
    
    # write a character to lcd (or character rom) 0x09: backlight | RS=DR<
    # works!
    def lcd_write_char(self, charvalue, mode=1):
        self.lcd_write_four_bits(mode | (charvalue & 0xF0))
        self.lcd_write_four_bits(mode | ((charvalue << 4) & 0xF0))
        
    # put string function
    def lcd_display_string(self, string, line):
        if line == 1:
            self.lcd_write(0x80)
        if line == 2:
            self.lcd_write(0xC0)
        if line == 3:
            self.lcd_write(0x94)
        if line == 4:
            self.lcd_write(0xD4)
    
        for char in string:
            self.lcd_write(ord(char), Rs)
            
    # clear lcd and set to home
    def lcd_clear(self):
        self.lcd_write(LCD_CLEARDISPLAY)
        self.lcd_write(LCD_RETURNHOME)
        
    # define backlight on/off (lcd.backlight(1); off= lcd.backlight(0)
    def backlight(self, state): # for state, 1 = on, 0 = off
        if state == 1:
            self.lcd_device.write_cmd(LCD_BACKLIGHT)
        elif state == 0:
            self.lcd_device.write_cmd(LCD_NOBACKLIGHT)
            
    # add custom characters (0 - 7)
    def lcd_load_custom_chars(self, fontdata):
        self.lcd_write(0x40);
        for char in fontdata:
            for line in char:
                self.lcd_write_char(line)
                
    # define precise positioning (addition from the forum)
    def lcd_display_string_pos(self, string, line, pos):
        if line == 1:
            pos_new = pos
        elif line == 2:
            pos_new = 0x40 + pos
        elif line == 3:
            pos_new = 0x14 + pos
        elif line == 4:
            pos_new = 0x54 + pos
            
        self.lcd_write(0x80 + pos_new)
        
        for char in string:
            self.lcd_write(ord(char), Rs)

    def dispBar(self):    
        self.lcd_load_custom_chars(fontdata2)    
        block = chr(255) # block character, built-in    
        self.lcd_display_string_pos(block * 2,1,4)    
        pauza = 0.07 # define duration of sleep(x)
        pos = 6
        self.lcd_display_string_pos(unichr(1),1,6)
        sleep(pauza)
        
        self.lcd_display_string_pos(unichr(2),1,pos)
        sleep(pauza)
        
        self.lcd_display_string_pos(unichr(3),1,pos)
        sleep(pauza)
        
        self.lcd_display_string_pos(unichr(4),1,pos)
        sleep(pauza)
        
        self.lcd_display_string_pos(block,1,pos)
        sleep(pauza)
        
        # and another one, same as above, 1 char-space to the right
        pos = pos +1 # increase column by one
        
        self.lcd_display_string_pos(unichr(1),1,pos)
        sleep(pauza)
        self.lcd_display_string_pos(unichr(2),1,pos)
        sleep(pauza)
        self.lcd_display_string_pos(unichr(3),1,pos)
        sleep(pauza)
        self.lcd_display_string_pos(unichr(4),1,pos)
        sleep(pauza)
        self.lcd_display_string_pos(block,1,pos)
        sleep(pauza)