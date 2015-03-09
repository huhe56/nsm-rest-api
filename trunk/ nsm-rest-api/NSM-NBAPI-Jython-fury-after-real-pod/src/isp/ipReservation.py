'''
Created on Jul 15, 2012

@author: huhe
'''
from isp import Define
from lib import Util
from isp import XPath
from isp.element import Element
from isp.nsmUtil import NsmUtil

class IpReservation(Element):
    
    _linkRelKeys = ['self', 'nsmr:ipreservations', 'nsmr:ipavailable', 'nsmr:ipallocated', 'nsmr:create']
    
    def __init__(self, catalog, name, description, requestFileName, requestParams=None):
        self.logger = Util.getLogger(self.__class__.__name__)
        Element.__init__(self)
        Element.setCreateParameter(self, name, description, requestFileName, requestParams)  
        self.relLinkDictionary = {}
        IpReservation.parseCatalog(self, catalog)
        
    
    def parseCatalog(self, catalog):
        for relKey in IpReservation._linkRelKeys:
            evalXpath = XPath._LinkIpReservation
            evalXpath = evalXpath.replace('${rel}', relKey)
            link = Util.getXpathValue(catalog, evalXpath)
            self.logger.info('Link of ' + relKey + ': ' + link)
            self.relLinkDictionary[relKey] = link
        
    
    def create(self, testCaseId):
        self.catalogCreateUrl = self.relLinkDictionary['nsmr:create']
        status = Element.create(self, testCaseId)
        return status
    
            
    def getDetail(self, testCaseId):
        tmp = XPath._TaskElementUid
        XPath._TaskElementUid = XPath._TaskElementIpReservationUid
        detail = Element.getDetail(self, testCaseId)
        XPath._TaskElementUid = tmp
        return detail
        
    
        
    
        