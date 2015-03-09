'''
Created on Oct 12, 2012

@author: huhe
'''

from device.main import DeviceDefine
from device.main.deviceUtil import DeviceUtil

class Reset(object):
    
    @staticmethod
    def setDSCLogDebug():
        for deviceType in DeviceDefine._DSCTypeList:
            DeviceUtil.action(deviceType, 'set-log-debug')
            

    @staticmethod
    def resetDeviceAndCopyCleanRunningConfig():
        Reset.resetDevice()
        Reset.copyRunningConfigToTFTPServer()
        Reset.copyRunningConfigToTemp('copy-to-tmp-clean')
        
        
        
    @staticmethod
    def diffCleanClean():
        DeviceUtil.action(DeviceDefine._DeviceTypeLinux, 'diff-config-clean-clean')
        
    
    @staticmethod
    def diffCleanDelete():
        DeviceUtil.action(DeviceDefine._DeviceTypeLinux, 'diff-config-clean-delete')
        
        
    @staticmethod
    def diffCleanCreate():
        DeviceUtil.action(DeviceDefine._DeviceTypeLinux, 'diff-config-clean-create')
        
    
        
    @staticmethod
    def copyCreateRunningConfig():
        Reset.copyRunningConfigToTFTPServer()
        Reset.copyRunningConfigToTemp('copy-to-tmp-create')
        

    @staticmethod
    def resetNSMandDevice():
        action = DeviceDefine._DeviceActionReset
        for deviceType in DeviceDefine._DSCTypeList:
            DeviceUtil.action(deviceType, action)
        for deviceType in DeviceDefine._NSVETypeList:
            DeviceUtil.action(deviceType, action)
        for deviceType in DeviceDefine._DeviceTypeResetList:
            DeviceUtil.action(deviceType, action)
        
        
    @staticmethod
    def resetNSM():
        Reset.resetDSC()
        Reset.resetNSVE()
        
        
    @staticmethod
    def resetNSVE():
        action = DeviceDefine._DeviceActionReset
        for deviceType in DeviceDefine._NSVETypeList:
            DeviceUtil.action(deviceType, action)
            
            
    @staticmethod
    def resetDSC():
        action = DeviceDefine._DeviceActionReset
        for deviceType in DeviceDefine._DSCTypeList:
            DeviceUtil.action(deviceType, action)
            
            
    @staticmethod
    def resetDevice():
        action = DeviceDefine._DeviceActionReset
        for deviceType in DeviceDefine._DeviceTypeResetList:
            DeviceUtil.action(deviceType, action)
            
            
    @staticmethod
    def copyRunningConfigToTemp(action):
        DeviceUtil.action(DeviceDefine._DeviceTypeLinux, action)
        
        
    @staticmethod
    def copyRunningConfigToTFTPServer():
        action = DeviceDefine._DeviceActionCopy
        for deviceType in DeviceDefine._DeviceTypeCopyList:
            DeviceUtil.action(deviceType, action)
        
    
    @staticmethod
    def startController():
        action = DeviceDefine._DeviceActionConfigure
        for deviceType in DeviceDefine._DSCTypeList:
            DeviceUtil.action(deviceType, action)
            

    @staticmethod
    def saveNSMLog():
        for deviceType in DeviceDefine._NSMTypeList:
            DeviceUtil.action(deviceType, 'save-log')