'''
Created on Sep 25, 2012

@author: huhe
'''

from device.main.deviceElement import DeviceElement


class DeviceIOS(DeviceElement):
    '''
    classdocs
    '''


    def __init__(self, host, usr, pwd):
        DeviceElement.__init__(self, host, usr, pwd, 'cmd-ios.json')
        
        
    def reset(self, archiveName):
        resetCmdListNew = []
        resetCmdList = self._cmdMap['reset']
        for oneCmdSet in resetCmdList:
            cmdStr = oneCmdSet['cmd']
            cmdStr = cmdStr.replace('${archive-name}', archiveName)
            oneCmdSet['cmd'] = cmdStr
            resetCmdListNew.append(oneCmdSet)
        DeviceElement.processCmdList(self, resetCmdListNew)
        
        
        clearLineCmdList = []
        for i in range(2, 10):
            oneCmdSet = {}
            oneCmdSet['cmd'] = 'clear line ' + str(i)
            oneCmdSet['expect'] = 'confirm]'
            clearLineCmdList.append(oneCmdSet)
            oneCmdSet = {}
            oneCmdSet['cmd'] = '' 
            oneCmdSet['expect'] = '#'
            clearLineCmdList.append(oneCmdSet)
            
        try:
            DeviceElement.processCmdList(self, clearLineCmdList)
        except:
            self._logger.info('my vty line is cleared ...')
        
