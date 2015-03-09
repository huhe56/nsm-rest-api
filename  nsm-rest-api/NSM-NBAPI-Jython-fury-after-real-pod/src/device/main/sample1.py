'''
Created on Oct 19, 2012

@author: huhe
'''
import time
from device.main.myClosure import MyClosure
from device.main.myExpect import Expect
from lib import Util

if __name__ == '__main__':
    logger = Util.getLogger('sample1.py')
    expect = Expect(logger, 'od-c3-asr-a', 'admin', 'cisco123')
    expect.expectIt('#')
    expect.sendIt('terminal length 0')
    i = expect.expectIt('#')
    expect.sendIt('show run')
    i = expect.expectIt('#')
    expect.sendIt('show run')
    i = expect.expectRegex('ntp source GigabitEthernet0')
    strbuffer = expect.printGetMatch()
    print 'i = ' + str(i)
    
    