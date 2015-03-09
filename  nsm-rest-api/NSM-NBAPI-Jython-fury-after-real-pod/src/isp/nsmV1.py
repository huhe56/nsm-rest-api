'''
Created on Jul 14, 2012

@author: huhe
'''

import Define, XPath
from lib import Util
from isp.element import Element


class NsmV1(Element):
    '''
    classdocs
    '''    

    def __init__(self, catalog, name=None, description=None, requestBodyFileName=None, requestParams=None):
        '''
        Constructor
        '''        
        Element.__init__(self)
        self.createName = name
        url = Define._UrlApiRoot
        self.getCatalogUrl = url

    
    def create(self, testCaseId):
        return True
    
    
    def getProviderList(self, testCaseId):
        providerListUrl = Util.getXpathValue(self.catalogXml, XPath._TopIndexListProviderLinkHref)
        return self.getList(providerListUrl, 'provider', testCaseId)
        
    
    def verifyCreate(self):
        return True
    
    
    def verifyUpdate(self):
        return True
        
    
        