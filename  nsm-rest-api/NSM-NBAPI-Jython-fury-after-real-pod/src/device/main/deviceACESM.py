'''
Created on Sep 25, 2012

@author: huhe
'''

from device.main import DeviceDefine
from device.main.deviceElement import DeviceElement


class DeviceACESM(DeviceElement):
    '''
    classdocs
    '''


    def __init__(self, host, usr, pwd):
        '''
        use vss since ace login issue
        '''
        DeviceElement.__init__(self, host, usr, pwd, 'cmd-ace-sm.json')
        
