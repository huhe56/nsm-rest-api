'''
Created on Jul 16, 2012

@author: huhe
'''

import time
from lib import Util, HttpUtil
from isp import Define, XPath 


class Task(object):
    '''
    classdocs
    '''
    
    _loopInterval  = 5
    

    def __init__(self, taskXml):
        '''
        Constructor
        '''
        self.logger = Util.getLogger(self.__class__.__name__)
        self._loopCount = 10
        self.taskXml = taskXml
        
        
    def checkResult(self):
        while self.taskXml and self._loopCount > 0:
            #if (self._loopCount == 10):
            #    self.logger.debug('task link self xpath: ' + XPath._TaskLinkSelf) 
            #    self.logger.debug('task status xpath: ' + XPath._TaskTaskStatus)

            selfUrl = Util.getXpathValue(self.taskXml, XPath._TaskLinkSelf)
            status = Util.getXpathValue(self.taskXml, XPath._TaskTaskStatus)
            taskResponseCode = Util.getXpathValue(self.taskXml, XPath._TaskResponseCode)
            self.logger.info('')
            self.logger.info('task status [' + str(self._loopCount) + ']: ------------------------------------->>> ' + taskResponseCode + ': ' + status)
            self.logger.info('')
            if status == 'success':
                return True
            elif status == 'failure':
                taskFaultType = Util.getXpathValue(self.taskXml, XPath._TaskFaultType)
                taskFaultMessag = Util.getXpathValue(self.taskXml, XPath._TaskFaultMessag)
                taskFaultArguments = Util.getXpathValue(self.taskXml, XPath._TaskFaultArguments)
                self.logger.info('')
                self.logger.info('')
                self.logger.info('---------------->>> Task result is FAILURE <<<--------------------')
                self.logger.info('')
                self.logger.info('fault type: ' + taskFaultType)
                self.logger.info('fault message: ' + taskFaultMessag)
                self.logger.info('fault arguments: ' + taskFaultArguments)
                self.logger.info('------------------------------------------------------------------')
                self.logger.info('')
                return False
            self._loopCount = self._loopCount - 1
            time.sleep(Task._loopInterval)
            self.taskXml = HttpUtil.doGet(selfUrl, Define._credential)
            
        return False
            
        