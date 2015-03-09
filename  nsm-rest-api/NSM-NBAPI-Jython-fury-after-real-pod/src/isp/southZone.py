'''
Created on Jul 15, 2012

@author: huhe
'''

from lib import Util
from isp.element import Element
from isp.nsmUtil import NsmUtil
from isp.edgeZone import EdgeZone


class SouthZone(EdgeZone):
    
    _catalogServiceOfferingType = 'zone'
    _catalogServiceOfferingName = 'South Zone'
    _catalogLinkTitle = 'South Zone'
    
    
    def __init__(self, catalog, name=None, description=None, requestFileName='default-south-zone.xml', requestParams=None):
        self.logger = Util.getLogger(self.__class__.__name__)
        Element.__init__(self)
        Element.setCatalogMatchParameter(self, SouthZone._catalogServiceOfferingType, SouthZone._catalogServiceOfferingName, SouthZone._catalogLinkTitle)
        Element.setCreateParameter(self, name, description, requestFileName, requestParams)        
        Element.parseCatalog(self, catalog)
        
    
