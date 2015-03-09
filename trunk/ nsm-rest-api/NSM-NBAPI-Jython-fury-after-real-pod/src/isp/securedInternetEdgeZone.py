'''
Created on Jul 15, 2012

@author: huhe
'''

from lib import Util
from isp.element import Element
from isp.nsmUtil import NsmUtil
from isp.edgeZone import EdgeZone


class SecuredInternetEdgeZone(EdgeZone):
    
    _catalogServiceOfferingType = 'zone'
    _catalogServiceOfferingName = 'Secured Internet Edge'
    _catalogLinkTitle = 'Secured Internet Edge'
    
    
    def __init__(self, catalog, name=None, description=None, requestFileName='default-secured-internet-edge-zone.xml', requestParams=None):
        self.logger = Util.getLogger(self.__class__.__name__)
        Element.__init__(self)
        Element.setCatalogMatchParameter(self, SecuredInternetEdgeZone._catalogServiceOfferingType, SecuredInternetEdgeZone._catalogServiceOfferingName, SecuredInternetEdgeZone._catalogLinkTitle)
        Element.setCreateParameter(self, name, description, requestFileName, requestParams)        
        Element.parseCatalog(self, catalog)
        
    
