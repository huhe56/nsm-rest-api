'''
Created on Oct 2, 2012

@author: huhe
'''


from device.main import DeviceDefine
from device.main.deviceNexus import DeviceNexus
from device.main.deviceN1K import DeviceN1K
from device.main.deviceIOS import DeviceIOS
from device.main.deviceUCS import DeviceUCS
from device.main.deviceACESM import DeviceACESM
from device.main.deviceASASM import DeviceASASM
from device.main.deviceLunix import DeviceLinux
from device.main.deviceNSVE import DeviceNSVE
from device.main.deviceDSC import DeviceDSC
from isp.nsmUtil import NsmUtil


class DeviceUtil(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        
    @staticmethod
    def action(deviceType, action):
    
        deviceList = None
        if   deviceType == DeviceDefine._DeviceTypeACESM:  deviceList = DeviceDefine._ACESMDeviceList
        elif deviceType == DeviceDefine._DeviceTypeASASM:  deviceList = DeviceDefine._ASASMDeviceList
        elif deviceType == DeviceDefine._DeviceTypeIOS:    deviceList = DeviceDefine._IOSDeviceList
        elif deviceType == DeviceDefine._DeviceTypeN1K:    deviceList = DeviceDefine._N1KDeviceList
        elif deviceType == DeviceDefine._DeviceTypeNexus:  deviceList = DeviceDefine._NexusDeviceList
        elif deviceType == DeviceDefine._DeviceTypeUCS:    deviceList = DeviceDefine._UCSDeviceList
        elif deviceType == DeviceDefine._DeviceTypeLinux:  deviceList = DeviceDefine._LinuxDeviceList
        elif deviceType == DeviceDefine._DeviceTypeNSVE:   deviceList = DeviceDefine._NSVEDeviceList
        elif deviceType == DeviceDefine._DeviceTypeDSC:    deviceList = DeviceDefine._DSCDeviceList
        
        for hostname, credentials in deviceList.items():
            NsmUtil.printHeadLine1('BEGIN: ' + hostname)
            device = None
            if not credentials:
                if   deviceType == DeviceDefine._DeviceTypeACESM:  device = DeviceACESM(hostname, DeviceDefine._DefaultUsr, DeviceDefine._DefaultPwd)
                elif deviceType == DeviceDefine._DeviceTypeASASM:  device = DeviceASASM(hostname, DeviceDefine._DefaultUsr, DeviceDefine._DefaultPwd)
                elif deviceType == DeviceDefine._DeviceTypeIOS:    device = DeviceIOS(hostname, DeviceDefine._DefaultUsr, DeviceDefine._DefaultPwd)
                elif deviceType == DeviceDefine._DeviceTypeN1K:    device = DeviceN1K(hostname, DeviceDefine._DefaultUsr, DeviceDefine._DefaultPwd)
                elif deviceType == DeviceDefine._DeviceTypeNexus:  device = DeviceNexus(hostname, DeviceDefine._DefaultUsr, DeviceDefine._DefaultPwd)
                elif deviceType == DeviceDefine._DeviceTypeUCS:    device = DeviceUCS(hostname, DeviceDefine._DefaultUsr, DeviceDefine._DefaultPwd)
            else:
                usr = credentials['usr']
                pwd = credentials['pwd']
                if   deviceType == DeviceDefine._DeviceTypeLinux:  device = DeviceLinux(hostname, usr, pwd)
                elif deviceType == DeviceDefine._DeviceTypeNSVE:   device = DeviceNSVE(hostname, usr, pwd)
                elif deviceType == DeviceDefine._DeviceTypeDSC:    device = DeviceDSC(hostname, usr, pwd)
            
            if action == DeviceDefine._DeviceActionReset:
                if deviceType == DeviceDefine._DeviceTypeIOS:
                    archiveName = DeviceDefine._ArchiveNameMap[hostname]
                    device.reset(archiveName)
                else:
                    device.reset()
            elif action == DeviceDefine._DeviceActionCopy:
                device.copy()
            else:
                device.action(action)
                
            device.close()
            NsmUtil.printHeadLine1('END: ' + hostname)