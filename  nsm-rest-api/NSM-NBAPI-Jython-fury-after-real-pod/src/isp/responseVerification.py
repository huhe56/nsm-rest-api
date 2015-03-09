'''
Created on Sep 7, 2012

@author: huhe
'''

import re, os
from lib import Util

class ResponseVerification(object):
    '''
    classdocs
    '''

    __logger = Util.getLogger(Util.getFileNameWithoutSuffix(__file__))
    
    def __init__(self):
        '''
        Constructor
        '''
        
    @staticmethod
    def formalize(xmlStr):
        #xmlStr = re.sub(r'[0-9A-Fa-f]{32}', 'uid', xmlStr)
        #print Util.prettfyXmlByString(str)
        #xmlStr = re.sub(r'[T0-9:\-\s\.]{29}', 'time', xmlStr)
        #xmlStr = re.sub(r'[T0-9:\-\s\.]{25}', 'time', xmlStr)
        #print Util.prettfyXmlByString(str)
        
        #print xmlStr
        p = re.compile('(<properties>.*</properties>)')
        m = p.search(xmlStr)
        print m.group(1)
        return m.group(1)
    
        
    @staticmethod
    def verifyCreate(goldenFilePath, currentFilePath):
        goldenStr  = Util.readFile(goldenFilePath)
        currentStr = Util.readFile(currentFilePath)
        
        goldenStr  = ResponseVerification.formalize(goldenStr)
        currentStr = ResponseVerification.formalize(currentStr)
        
        if goldenStr == currentStr:
            ResponseVerification.__logger.info('Response Verification test result: PASSED')
            return True
        else:
            ResponseVerification.__logger.info('golden:  ' + goldenStr)
            ResponseVerification.__logger.info('current: ' + currentStr)
            ResponseVerification.__logger.info('Response Verification test result: FAILED')
            return False
        
        
        
        