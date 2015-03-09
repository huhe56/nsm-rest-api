'''
Created on Sep 25, 2012

@author: huhe
'''

import re, time

from lib import Util
from isp import Define
from isp.nsmUtil import NsmUtil

from device.main import DeviceDefine
from device.main.myExpect import Expect


class DeviceElement():
    '''
    classdocs
    '''


    def __init__(self, host, usr, pwd, cmdFileName):
        
        self._subClassName = self.__class__.__name__
        self._logger = Util.getLogger(self._subClassName)
                
        self._cmdFileName = cmdFileName
        self._cmdFilePath = self._cmdFilePath = Define._PathDeviceCmd + '/' + self._cmdFileName
        
        self._cmdMap = Util.getJsonData(self._cmdFilePath)
        
        self._host = host
        self._usr  = usr
        self._pwd  = pwd
        
        if host in DeviceDefine._ACESMandVSSMap.keys():
            host = DeviceDefine._ACESMandVSSMap[host]
            '''
            also need to find VSS usr/pwd in the future
            '''
        
        self._expect = Expect(self._logger, host, usr, pwd)
        
        self._output = None
        
        
    @staticmethod
    def evaluate(cmdList, evalMap):
        cmdListNew = []
        for oneCmdSet in cmdList:
            cmdStr = oneCmdSet['cmd']
            if cmdStr.find('${') >= 0:
                for key, value in evalMap.items():
                    cmdStr = cmdStr.replace(key, value)
            oneCmdSet['cmd'] = cmdStr
            cmdListNew.append(oneCmdSet)
        return cmdListNew
        
    
    def copy(self):
        evalMap = {
            '${tftp-server-host}': DeviceDefine._TFTPHost, 
            '${host-name}': self._host,
        }
        copyCmdList = self._cmdMap['copy']
        copyCmdList = DeviceElement.evaluate(copyCmdList, evalMap)
        NsmUtil.printHeadLine2('copy running config to tftp server')
        return self.processCmdList(copyCmdList)
    
    
    def reset(self):
        evalMap = {
            '${tftp-server-host}': DeviceDefine._TFTPHost,
        }
        resetCmdList = self._cmdMap['reset']
        resetCmdList = DeviceElement.evaluate(resetCmdList, evalMap)
        NsmUtil.printHeadLine2('reset device to base line config')
        return self.processCmdList(resetCmdList)
    
    
    def action(self, actionType):
        copyCmdList = self._cmdMap[actionType]
        NsmUtil.printHeadLine2(actionType)
        return self.processCmdList(copyCmdList)
    
    
    def processCmdList(self, cmdList):
        status = True
        for oneCmdSet in cmdList:
            cmdStr = oneCmdSet['cmd']
            expectPattern = oneCmdSet['expect'] if 'expect' in oneCmdSet.keys() else None
            sleep = oneCmdSet['sleep'] if 'sleep' in oneCmdSet.keys() else None
            
            self._expect.sendIt(cmdStr)
            
            '''
            if sleep:
                self._logger.info('sleep:  ' + sleep + ' seconds ...')
                time.sleep(int(sleep))
            '''
            
            if sleep: 
                self._expect.setDefaultTimeout(int(sleep)*1000)
                self._logger.info('timeout is set to ' + sleep + ' seconds')
            if expectPattern: 
                self._expect.expectIt(expectPattern)
                self._output = self._expect._output
                if re.search(expectPattern, self._output):
                    NsmUtil.printStatusHeadLine('Passed: pattern found: ' + expectPattern)
                else:
                    NsmUtil.printStatusHeadLine('Failed: pattern not found: ' + expectPattern)
                    status = False
            else:
                self._expect.expectAll()
            if sleep: self._expect.setDefaultTimeout(30*1000)
            
        return status
            
    
    def close(self):
        self._expect.logout()
        
        