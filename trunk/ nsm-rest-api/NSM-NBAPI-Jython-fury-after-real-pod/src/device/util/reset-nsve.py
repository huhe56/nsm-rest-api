'''
Created on Sep 25, 2012

@author: huhe
'''

from device.main import DeviceDefine
from device.main.deviceUtil import DeviceUtil

    
if __name__ == '__main__':
      
    action = DeviceDefine._DeviceActionReset
    for deviceType in DeviceDefine._NSVETypeList:
        DeviceUtil.action(deviceType, action)
    

    