'''
Created on Sep 25, 2012

@author: huhe
'''


from device.main import DeviceDefine
from device.main.deviceUtil import DeviceUtil
from device.main.mainReset import Reset

    
if __name__ == '__main__':
    
    '''
    must put ucs-backup-all.xml in /tftpboot
    '''
    '''
    action = DeviceDefine._DeviceActionReset
    for deviceType in DeviceDefine._DeviceTypeResetList:
        DeviceUtil.action(deviceType, action)
    '''
    
    ''' ace often has connection time out problem'''
    #DeviceUtil.action(DeviceDefine._DeviceTypeNexus, 'copy')
    
    
    #action = 'copy-to-tmp-clean'
    #DeviceUtil.action(DeviceDefine._DeviceTypeLinux, action)
    
    
    
    action = 'reset'
    DeviceUtil.action(DeviceDefine._DeviceTypeUCS, action)
    
    
    #Reset.copyRunningConfigToTemp('copy-to-tmp-create')
    
    #Reset.saveNSMLog()
    
    #Reset.setDSCLogDebug()
    
    