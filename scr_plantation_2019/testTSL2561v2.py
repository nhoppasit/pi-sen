import TSL2561

ch0,ch1 = TSL2561.LUX29()

# Output data to screen
print "Full Spectrum(IR + Visible) :%d lux" %ch0
print "Infrared Value :%d lux" %ch1
print "Visible Value :%d lux" %(ch0 - ch1)

ch0,ch1 = TSL2561.LUX39()

# Output data to screen
print "Full Spectrum(IR + Visible) :%d lux" %ch0
print "Infrared Value :%d lux" %ch1
print "Visible Value :%d lux" %(ch0 - ch1)

ch0,ch1 = TSL2561.LUX49()

# Output data to screen
print "Full Spectrum(IR + Visible) :%d lux" %ch0
print "Infrared Value :%d lux" %ch1
print "Visible Value :%d lux" %(ch0 - ch1)
