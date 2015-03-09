'''
Created on Aug 9, 2012

@author: huhe
'''
import time, sys, traceback
from expect4j import ExpectUtils
from expect4j.matches import RegExpMatch
from device.main.myClosure import MyClosure
from java.util import Hashtable
from com.jcraft.jsch import JSch
from com.jcraft.jsch import Session
from expect4j import Expect4j


class Expect(object):
    '''
    classdocs
    '''
    
    __cmdSetNoMore = 'terminal length 0'


    def __init__(self, logger, hostname, usr, pwd):
        '''
        Constructor
        '''
        self._logger = logger
        self._output = None
        self._hostPrompt = hostname + '#'
        self._allPattern = '.*' + self._hostPrompt
        
        #self._expect = ExpectUtils.SSH(hostname, usr, pwd, 22)
        self._expect = Expect.ssh(hostname, usr, pwd, 30)
        self._expect.setDefaultTimeout(30*1000)
        #self._expect.expect(self._allPattern)
        self.expectAll()
        
        
    @staticmethod
    def ssh(host, usr, pwd, timeout):
        jsch = JSch()
        session = jsch.getSession(usr, host, 22)
        session.setPassword(pwd)
        config = Hashtable()
        config.put('StrictHostKeyChecking', 'no')
        session.setConfig(config)
        session.setDaemonThread(True)
        ''' connect timeout '''
        session.connect(timeout*1000)
        
        channel = session.openChannel('shell')
        channel.setPtyType('vt102')
        
        env = Hashtable()
        channel.setEnv(env)
        
        expect4j = Expect4j(channel.getInputStream(), channel.getOutputStream())
        
        ''' expect return timeout '''
        channel.connect(timeout*1000)
        
        return expect4j
        
        
    def setDefaultTimeout(self, timeout):
        self._expect.setDefaultTimeout(timeout)
        
        
    def sendIt(self, cmd):
        self._logger.info("send:   " + cmd)
        self._expect.send(cmd + "\n")
        time.sleep(1)
        
        
    def expectIt(self, pattern):
        try:
            self._logger.info("expect: " + pattern)
            self._expect.expect(pattern)
            self._output = self.printGetOutput()
        except:
            self._output = self.printGetOutput()
            errorType = sys.exc_info()[0]
            errorValue = sys.exc_info()[1]
            errorTraceBack = traceback.extract_tb(sys.exc_info()[2])
            self._logger.error('Error Type: ' + str(errorType))
            self._logger.error('Error Value: ' + str(errorValue))
            self._logger.error('Traceback: ')
            for oneStack in errorTraceBack:
                self._logger.error(oneStack)

    
    def expectAll(self):
        return self.expectRegex('^.*$')
    
    
    def expectRegex(self, pattern):
        closure = MyClosure()
        match = RegExpMatch(pattern, closure)
        matchList = []
        matchList.append(match)
        return self._expect.expect(matchList)
    
    
    def getOutput(self):
        return self._expect.getLastState().getBuffer()
    
    
    def getMatch(self):
        return self._expect.getLastState().getMatch()
    
    
    def printOutput(self, output):
        if output:
            self._logger.info('\n\n' + '-'*40 + ' begin: output ' + '-'*40 + '\n' + output + '\n' + '-'*40 + ' end: output ' + '-'*40 + '\n\n')
        
    
    def printGetOutput(self):
        output = self._expect.getLastState().getBuffer()
        self.printOutput(output)
        return output
    
    
    def printGetMatch(self):
        output = self._expect.getLastState().getMatch()
        self.printOutput(output)
        return output
    
    
    def logout(self):
        self._logger.info('close session')
        self._expect.close()
        
        