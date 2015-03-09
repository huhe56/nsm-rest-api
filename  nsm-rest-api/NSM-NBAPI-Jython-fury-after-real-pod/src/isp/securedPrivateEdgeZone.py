'''
Created on Jul 15, 2012

@author: huhe
'''

from lib import Util
from isp.element import Element
from isp.edgeZone import EdgeZone


class SecuredPrivateEdgeZone(EdgeZone):
    
    _catalogServiceOfferingType = 'zone'
    _catalogServiceOfferingName = 'Secured Private Edge'
    _catalogLinkTitle = 'Secured Private Edge'
    
    
    def __init__(self, catalog, name=None, description=None, requestFileName='default-secured-private-edge-zone.xml', requestParams=None):
        self.logger = Util.getLogger(self.__class__.__name__)
        Element.__init__(self)
        Element.setCatalogMatchParameter(self, SecuredPrivateEdgeZone._catalogServiceOfferingType, SecuredPrivateEdgeZone._catalogServiceOfferingName, SecuredPrivateEdgeZone._catalogLinkTitle)
        Element.setCreateParameter(self, name, description, requestFileName, requestParams)        
        Element.parseCatalog(self, catalog)
        
        
   
    
