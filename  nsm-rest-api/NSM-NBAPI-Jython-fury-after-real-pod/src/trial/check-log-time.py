'''
Created on Jan 10, 2013

@author: huhe
'''

import re
from datetime import datetime
from datetime import timedelta
from time import mktime

if __name__ == '__main__':
    
    patternClassName = '>>> class name: <<<'
    patternCreateStart = 'START: create test case'
    patternCreateEnd = 'END: create test case'
    
    filePath = '/Users/huhe/Temp/tt3.txt'
    
    f = open(filePath)
    lines = f.readlines()
    f.close()
    
    total = 0
    count = 0
    switchStart = True;
    timeStart = None
    timeEnd   = None
    
    while count < len(lines):
        
        line = lines[count]
        
        
        timeStr = re.findall(r'\d{4}\-\d{2}\-\d{2} \d{2}:\d{2}:\d{2}', line)
        if switchStart:
            timeStart = timeStr[0]
            switchStart = False
            print 'start: ' + timeStart
        else:
            timeEnd = timeStr[0]
            switchStart = True
            print 'end:  ' + timeEnd
            
            
            
            tStart = datetime.strptime(timeStart, '%Y-%m-%d %H:%M:%S')
            tEnd   = datetime.strptime(timeEnd, '%Y-%m-%d %H:%M:%S')
            
            diffs = tEnd - tStart
            print diffs
            print diffs.seconds
            total += diffs.seconds
            
            count += 1
            
            #diff = mktime(tEnd) - mktime(tStart)
            #print diff
            
    print 'total count: ' + str(count)
    print 'total second: ' + str(total)
            
        