'''
Created on Jul 15, 2012

@author: huhe
'''

from lib import Util
from isp.element import Element
from isp.edgeZone import EdgeZone


class PrivateEdgeZone(EdgeZone):
    
    _catalogServiceOfferingType = 'zone'
    _catalogServiceOfferingName = 'Private Edge'
    _catalogLinkTitle = 'Private Edge'
    
    
    def __init__(self, catalog, name=None, description=None, requestFileName='default-private-edge-zone.xml', requestParams=None):
        self.logger = Util.getLogger(self.__class__.__name__)
        Element.__init__(self)
        Element.setCatalogMatchParameter(self, PrivateEdgeZone._catalogServiceOfferingType, PrivateEdgeZone._catalogServiceOfferingName, PrivateEdgeZone._catalogLinkTitle)
        Element.setCreateParameter(self, name, description, requestFileName, requestParams)        
        Element.parseCatalog(self, catalog)
        