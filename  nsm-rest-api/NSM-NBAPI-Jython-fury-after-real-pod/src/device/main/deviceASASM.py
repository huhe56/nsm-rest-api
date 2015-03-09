'''
Created on Sep 25, 2012

@author: huhe
'''

import re

from device.main.deviceElement import DeviceElement


class DeviceASASM(DeviceElement):
    '''
    classdocs
    '''


    def __init__(self, host, usr, pwd):
        DeviceElement.__init__(self, host, usr, pwd, 'cmd-asa-sm.json')
        


    def reset(self):
        DeviceElement.reset(self)
        #print self._output
        lines = self._output.split('\r')
        #print lines
        userContextFound = False
        currentUserContextName = None
        for line in lines:
            line = line.strip()
            #self._logger.info(line)
            if re.search(r'context [0-9a-fA-F]{32}', line):
                self._logger.info('found one context start')
                items = line.split(' ')
                currentUserContextName = items[1]
                self._logger.info('found context: ' + items[1])
                userContextFound = True
            elif userContextFound and line == '!':
                self._logger.info('delete context: ' + currentUserContextName)
                self._expect.sendIt('config terminal')
                self._expect.expectIt('#')
                self._expect.sendIt('no context ' + currentUserContextName)
                self._expect.expectIt('confirm\]')
                self._expect.sendIt('')
                self._expect.expectIt('#')
                self._expect.sendIt('wr mem')
                self._logger.info('found one context end')
                self._expect.expectIt('#')
                userContextFound = False
                currentUserContextName = None
            elif userContextFound and re.search(r'allocate\-interface Vlan2[0-5][0-9]{2}', line):
                items = line.split(' ')
                self._logger.info('found allocate interface and delete it: ' + items[1])
                self._expect.sendIt('config terminal')
                self._expect.sendIt('no interface ' + items[1])
            elif not currentUserContextName:
                if re.search(r'interface Vlan2[0-5][0-9]{2}', line):
                    self._logger.info('found and delete ' + line)
                    self._expect.sendIt('config terminal')
                    self._expect.expectIt('#')
                    self._expect.sendIt('no ' + line)
                    self._expect.expectIt('#')
                    
                
                
                
                
        