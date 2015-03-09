'''
Created on Sep 25, 2012

@author: huhe
'''

import re

from device.main.deviceElement import DeviceElement


class DeviceN1K(DeviceElement):
    '''
    classdocs
    '''


    def __init__(self, host, usr, pwd):
        DeviceElement.__init__(self, host, usr, pwd, 'cmd-n1k.json')
        
        
    def reset(self):
        DeviceElement.reset(self)
        #print self._output
        lines = self._output.split('\r')
        #print lines
        userVlanList = []
        for line in lines:
            line = line.strip()
            #self._logger.info(line)
            if re.search(r'^vlan 2[0-5][0-9]{2}$', line):
                items = line.split(' ')
                userVlanList.append(items[1])
                self._logger.info('found and delete ' + line)
                self._expect.sendIt('config terminal')
                self._expect.expectIt('#')
                self._expect.sendIt('no vlan ' + items[1]) 
                self._expect.expectIt('#')
            elif re.search(r'^port-profile type vethernet 2[0-5][0-9]{2}$', line):
                items = line.split(' ')
                self._logger.info('found and delete port-profile type vethernet ' + items[3])
                self._expect.sendIt('config terminal')
                self._expect.expectIt('#')
                self._expect.sendIt('no port-profile type vethernet ' + items[3]) 
                self._expect.expectIt('#')
                
        if len(userVlanList) > 0:
            userVlansStr = ','.join(userVlanList)
            self._logger.info('delete allowed user vlans in port-profile type vethernet n1kv-uplink0')
            self._expect.sendIt('config terminal')
            self._expect.expectIt('#')
            self._expect.sendIt('port-profile type ethernet n1kv-uplink0') 
            self._expect.expectIt('#')
            self._expect.sendIt('switchport trunk allowed vlan remove ' + userVlansStr) 
            self._expect.expectIt('#')
                
                