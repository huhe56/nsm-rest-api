'''
Created on Sep 25, 2012

@author: huhe
'''

from device.main.deviceElement import DeviceElement


class DeviceUCS(DeviceElement):
    '''
    classdocs
    '''


    def __init__(self, host, usr, pwd):
        DeviceElement.__init__(self, host, usr, pwd, 'cmd-ucs.json')
        
