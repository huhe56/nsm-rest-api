'''
Created on Jul 15, 2012

@author: huhe
'''

from lib import Util
from isp.element import Element
from isp.nsmUtil import NsmUtil
from isp.edgeZone import EdgeZone


class InternetEdgeZone(EdgeZone):
    
    _catalogServiceOfferingType = 'zone'
    _catalogServiceOfferingName = 'Internet Edge'
    _catalogLinkTitle = 'Internet Edge'
    
    
    def __init__(self, catalog, name=None, description=None, requestFileName='default-internet-edge-zone.xml', requestParams=None):
        self.logger = Util.getLogger(self.__class__.__name__)
        Element.__init__(self)
        Element.setCatalogMatchParameter(self, InternetEdgeZone._catalogServiceOfferingType, InternetEdgeZone._catalogServiceOfferingName, InternetEdgeZone._catalogLinkTitle)
        Element.setCreateParameter(self, name, description, requestFileName, requestParams)        
        Element.parseCatalog(self, catalog)
        
    
