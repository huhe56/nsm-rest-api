'''
Created on Sep 24, 2012

@author: huhe
'''


_TFTPHost  = '171.69.75.167'

_DeviceTypeNexus    = 'Nexus'
_DeviceTypeIOS      = 'IOS'
_DeviceTypeUCS      = 'UCS'
_DeviceTypeN1K      = 'N1K'
_DeviceTypeACESM    = 'ACE-SM'
_DeviceTypeASASM    = 'ASA-SM'
_DeviceTypeLinux    = 'Linux'
_DeviceTypeNSVE     = 'NSVE'
_DeviceTypeDSC      = 'DSC'

_DeviceActionReset      = 'reset'
_DeviceActionCopy       = 'copy'
_DeviceActionStart      = 'start'
_DeviceActionConfigure  = 'configure'


#_DeviceTypeResetList   = [_DeviceTypeLinux, _DeviceTypeACESM, _DeviceTypeASASM, ]
_DeviceTypeResetList   = [_DeviceTypeLinux, _DeviceTypeASASM, _DeviceTypeUCS, _DeviceTypeNexus, _DeviceTypeN1K]
_DeviceTypeCopyList    = [_DeviceTypeASASM, _DeviceTypeUCS, _DeviceTypeNexus, _DeviceTypeN1K]

#_DeviceTypeASASM

_NSMTypeList    = [_DeviceTypeNSVE, _DeviceTypeDSC]

_NSVETypeList  = [_DeviceTypeNSVE]
_DSCTypeList   = [_DeviceTypeDSC]


_NSVEDeviceList = {
    'od-c3-nsve': {'usr': 'admin', 'pwd': 'Cnh123'}
}

_DSCDeviceList = {
    'od-c3-dsc': {'usr': 'admin', 'pwd': 'Cnh123'}
}


_LinuxDeviceList = {
    'huhe-ubuntu': {'usr': 'huhe', 'pwd': 'huanhe'}
}

_NexusDeviceList = {
    'od-c3-n7k-a': None,
    'od-c3-n7k-b': None,
    #'od-c3-n5k-a': None,
    #'od-c3-n5k-b': None,
}

_IOSDeviceList = {
    'od-c3-asr-a': None,
    'od-c3-asr-b': None,
    'od-c3-vss': None,
    #'192.168.66.169': None,
    #'192.168.66.250': None
 }

_UCSDeviceList = {
    'od-c3-ucs': None
    }

_N1KDeviceList = {
    'od-c3-n1kv': None
}

_ACESMDeviceList = {
    'od-c3-ace': None
}


_ACESMandVSSMap = {
    'od-c3-ace': 'od-c3-vss'
}


_ASASMDeviceList = {
    'od-c3-asa-a': None,
    'od-c3-asa-b': None,
    #'od-c3-fwsm-a': None,
    #'od-c3-fwsm-b': None,
}

_DefaultUsr = 'admin'
_DefaultPwd = 'cisco123'


_ArchiveNameMap = {
    'od-c3-asr-a':  'bootflash:huan-baseline-config-Oct-18-23-12-44.527-0',
    'od-c3-asr-b':  'bootflash:huan-baseline-config-Oct-18-23-13-17.025-0',
    'od-c3-vss':        'disk0:huan-baseline-config-Nov-14-23-25-32.191-2',
    '192.168.66.169':   'disk0:huan-baseline-config-Nov-20-00-56-34.756-5',
    '192.168.66.250':   'disk0:huan-baseline-config-Nov-20-00-58-29.626-4'
}


