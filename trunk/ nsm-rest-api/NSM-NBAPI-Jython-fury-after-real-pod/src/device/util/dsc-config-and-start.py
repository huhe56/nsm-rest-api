'''
Created on Sep 25, 2012

@author: huhe
'''

from device.main import DeviceDefine
from device.main.deviceUtil import DeviceUtil

    
if __name__ == '__main__':
      
    action = DeviceDefine._DeviceActionConfigure
    for deviceType in DeviceDefine._DSCTypeList:
        DeviceUtil.action(deviceType, action)
    

    