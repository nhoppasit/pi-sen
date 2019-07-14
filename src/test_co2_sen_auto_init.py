'''
Created on Jul 14, 2019

@author: think
'''

def co2_chk_sum(databuf):
    print "CO2 sensor check sum."
    sum = 0;
    for i in range(1,8):
        print repr(i);
        sum = sum + databuf[i];
        print "Sum = " + str(sum);
    cal_sum = (sum & 0xFF);
    cal_sum = ((~cal_sum) + 1);
    print "Sum = " + str(cal_sum);
    
def main():

    print "\n======================================================================="
    print "Test CO2 sensor auto initialization."
    print "======================================================================="

    co2_chk_sum([0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79]);
    
if __name__ == '__main__':
    main();
    pass