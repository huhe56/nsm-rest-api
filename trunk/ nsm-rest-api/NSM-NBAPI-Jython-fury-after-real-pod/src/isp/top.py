'''
Created on Jul 14, 2012

@author: huhe
'''

from lib import Util
from isp.element import Element
from isp import XPath


class Top(Element):
    '''
    classdocs
    '''

    def __init__(self, catalog, name=None, description=None, requestBodyFileName=None, requestParams=None):
        '''
        Constructor
        '''        
        Element.__init__(self)
        self.createName = name
        self.getCatalogUrl = Util.getXpathValue(catalog, XPath._TopIndexCatalogLinkHref)
        self.getProviderListUrl = Util.getXpathValue(catalog, XPath._TopIndexListProviderLinkHref)
        
        
    def create(self, testCaseId):
        return True

    
    def verifyCreate(self):
        return True
    
    
    def verifyUpdate(self):
        return True
    
        
    
        