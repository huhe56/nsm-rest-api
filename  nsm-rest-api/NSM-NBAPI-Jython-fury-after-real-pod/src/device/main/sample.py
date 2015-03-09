'''
Created on Aug 9, 2012

@author: huhe
'''

import time

from expect4j import ExpectUtils

hostname = 'od-c3-n7k-a'
prompt = hostname + '# '

expect = ExpectUtils.SSH(hostname, 'admin', 'cisco123', 22)
expect.expect(prompt)
output = expect.getLastState().getBuffer()
print output
expect.send('terminal length 0' + "\n")
expect.expect(prompt)
output = expect.getLastState().getBuffer()
print output
expect.send('show int bri' + "\n")


#time.sleep(2)

#i = expect.expect('.+')

#i = expect.expect(prompt)

#print 'i: ' + str(i)


output = expect.getLastState().getMatch()
print '---------> match: ' + output
output = expect.getLastState().getBuffer()
print '=========> bufffer: ' + output

expect.send('exit' + "\n")

if __name__ == '__main__':
    pass