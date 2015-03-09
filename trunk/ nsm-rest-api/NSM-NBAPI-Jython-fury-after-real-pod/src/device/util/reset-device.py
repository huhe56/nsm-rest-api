'''
Created on Sep 25, 2012

@author: huhe
'''


from device.main import DeviceDefine
from device.main.deviceUtil import DeviceUtil

    
if __name__ == '__main__':
    
    '''
    must put ucs-backup-all.xml in /tftpboot
    '''
    action = DeviceDefine._DeviceActionReset
    for deviceType in DeviceDefine._DeviceTypeResetList:
        DeviceUtil.action(deviceType, action)
    
    
    ''' ace often has connection time out problem'''
    #DeviceUtil.action(DeviceDefine._DeviceTypeUCS, DeviceDefine._DeviceActionReset)
    

    
    
    
    
    