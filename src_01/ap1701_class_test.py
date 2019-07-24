'''
Test of ap1701_mod class

'''

import ap1701_mod

ap1701_ports = ["COM1", "COM17", "COM16", "COM13", "COM17"]
ap1701_addr = ["09","10","11"]

ap1701 = ap1701_mod.ap1701()

try:
    ap1701.auto_init(ap1701_ports, ap1701_addr[0])

    for addr in ap1701_addr:
        [a,b] = ap1701.read_once(addr)

except Exception as ex:
    print repr(ex) + "\n"
    pass
