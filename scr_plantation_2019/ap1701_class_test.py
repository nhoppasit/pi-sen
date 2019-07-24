'''
Test of ap1701_mod class

'''

import ap1701_mod

ap1701_ports = ["/dev/ttyUSB3", "/dev/ttyUSB4"]
ap1701_addr = ["09","10","11"]

ap1701 = ap1701_mod.ap1701()

try:
    p = ap1701.auto_init(ap1701_ports, ap1701_addr[0])
    print repr(p) + "\n"

    for addr in ap1701_addr:
        [a,b] = ap1701.read_once(addr)
        print "[%f C, %f %sRH]\r\n" % (a, b, "%")

except Exception as ex:
    print repr(ex) + "\n"
    pass
