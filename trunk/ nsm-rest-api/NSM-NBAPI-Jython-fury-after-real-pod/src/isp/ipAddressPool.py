'''
Created on Jul 15, 2012

@author: huhe
'''

from lib import Util, HttpUtil
from isp import Define, XPath
from isp.nsmUtil import NsmUtil
from isp.element import Element
from isp.ipReservation import IpReservation

class IpAddressPool(Element):
            
    def __init__(self, ipAddressPoolUid, name, parentName, category):
        self.logger = Util.getLogger(self.__class__.__name__)
        
        self.logger.info('')
        self.logger.info('')
        self.logger.info('======================>>>>>> class name: ' + self.__class__.__name__ + ' <<<<<<<======================')
        self.logger.info('')
        self.logger.info('')
        
        self.isOffLine = False
        
        self.ipAddressPoolUid = ipAddressPoolUid
        self.parentName = parentName
        self.category = category
        
        self.createName = name
        self.catalogXml = None
        self.relLinkDictionary = {}
        
        
    def setOffLine(self):
        self.isOffLine = True
        
        
    def setOnLine(self):
        self.isOffLine = False
        
        
    def parseCatalog(self):
        for relKey in IpReservation._linkRelKeys:
            evalXpath = XPath._LinkIpReservation
            evalXpath = evalXpath.replace('${rel}', relKey)
            link = Util.getXpathValue(self.catalogXml, evalXpath)
            self.logger.info('Link of ' + relKey + ': ' + link)
            self.relLinkDictionary[relKey] = link
            
        
    def getDetail(self, testCaseId):
        
        NsmUtil.printHeadLine2('START: get detail test case ' + testCaseId)
        
        fileName = 'My Default IP Address Pool ' + self.parentName + ' ' + self.category
        nameDash = fileName.replace(' ', '-')
        debugGatalogFilePath = Define._PathResponseCreateDefault + '/' + nameDash + '-detail-' + testCaseId + '.xml'
        
        if (self.isOffLine):
            self.logger.debug('get detail from file: ' + debugGatalogFilePath)
            self.catalogXml = Util.readFile(debugGatalogFilePath)
        else:    
            self.catalogXml = HttpUtil.doGet(self.ipAddressPoolUid, Define._credential)
            self.logger.debug('write detail to file: ' + debugGatalogFilePath)
            Util.writeFile(debugGatalogFilePath, self.catalogXml)
        self.parseCatalog()
        
        NsmUtil.printHeadLine2('END: get detail test case ' + testCaseId)
        
        return self.catalogXml
    
