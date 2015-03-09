'''
Created on Jan 14, 2013

@author: huhe
'''

from datetime import datetime
from time import strftime
from pprint import pprint
import os


class Performance(object):
    
    _logFilePath = '/Users/huhe/Install/workspace/NSM-NBAPI-Jython/log/performance-data.txt'
    
    def __init__(self):
        '''
        Constructor
        '''
        #if os.path.exists(Performance._logFilePath):
        #    os.remove(Performance._logFilePath)
        self._allTenant = []
        self._currentPerfTenant = None
        
        
    def addCurrentTenant(self, perfTenant):
        if (self._currentPerfTenant):
            self._allTenant.append(self._currentPerfTenant)
            
        self._currentPerfTenant = perfTenant
        
        
    def setCurrentTenantName(self, tenantName):
        self._currentPerfTenant.setTenantName(tenantName)
        
    
    def setCurrentTenantStartTime(self, timeStart):
        self._currentPerfTenant.setTenantStartTime(timeStart)
        
        
    def setCurrentTenantEndTime(self, timeEnd, tenantIndex):
        self._currentPerfTenant.setTenantEndTime(timeEnd, tenantIndex)
        
        
    def setCurrentTenantClassLog(self, className, objectName, action, startTime, endTime):
        self._currentPerfTenant.logClass(className, objectName, action, startTime, endTime)
        
        
    @staticmethod
    def writeFile(filename, content): 
        fh = open(filename, 'a')
        fh.write(content)
        fh.flush()
        fh.close()
    
    
    def debug(self):
        self._currentPerfTenant.debug()
        

class PerfTenant(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self._data = []
        self._tenantName = None
        self._tenantTimeStart = None
        self._tenantTimeEnd = None
        self._totalCreateTime = 0
        
    
    def setTenantName(self, tenantName):
        self._tenantName = tenantName
        #Performance.writeFile(Performance._logFilePath, '\n\n')
        Performance.writeFile(Performance._logFilePath, 'Tenant: ' + self._tenantName + '\n')
        Performance.writeFile(Performance._logFilePath, '\tStart time: ' + self._tenantTimeStart.strftime('%Y-%m-%d %H:%M:%S') + '\n')
        
        
    def setTenantStartTime(self, timeStart):
        self._tenantTimeStart = timeStart
        
        
    def setTenantEndTime(self, timeEnd, tenantIndex):
        self._tenantTimeEnd = timeEnd
        diff = self._tenantTimeEnd - self._tenantTimeStart
        Performance.writeFile(Performance._logFilePath, '\tTotal tenant ' + str(tenantIndex) + ' create API seconds: ' + str(self._totalCreateTime) + '\n')
        Performance.writeFile(Performance._logFilePath, '\tTotal tenant ' + str(tenantIndex) + ' seconds: ' + str(diff.seconds) + '\n')
        Performance.writeFile(Performance._logFilePath, '\tEnd time: ' + self._tenantTimeEnd.strftime('%Y-%m-%d %H:%M:%S') + '\n')
        
        
    def logClass(self, className, objectName, action, startTime, endTime):
        oneAPIData = {}
        oneAPIData[className] = {}
        oneAPIData[className][action] = {}
        oneAPIData[className][action][objectName] = {}
        oneAPIData[className][action][objectName]['start'] = startTime
        oneAPIData[className][action][objectName]['end'] = endTime
        diff = endTime - startTime
        oneAPIData[className][action][objectName]['diff'] = diff.seconds
        self._data.append(oneAPIData)
        
        self._totalCreateTime += diff.seconds
        
        Performance.writeFile(Performance._logFilePath, '\t' + className + ': ' + objectName + ': ' + action + ': ' + str(diff.seconds) + '\n')
        
        
    def debug(self):
        print self._tenantName
        pprint(self._data)
        
        
        
        