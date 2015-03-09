'''
Created on Jul 15, 2012

@author: huhe
'''

from lib import Util
from isp.element import Element
from isp.nsmUtil import NsmUtil
from isp.edgeZone import EdgeZone


class NorthZone(EdgeZone):
    
    _catalogServiceOfferingType = 'zone'
    _catalogServiceOfferingName = 'North Zone'
    _catalogLinkTitle = 'North Zone'
    
    
    def __init__(self, catalog, name=None, description=None, requestFileName='default-north-zone.xml', requestParams=None):
        self.logger = Util.getLogger(self.__class__.__name__)
        Element.__init__(self)
        Element.setCatalogMatchParameter(self, NorthZone._catalogServiceOfferingType, NorthZone._catalogServiceOfferingName, NorthZone._catalogLinkTitle)
        Element.setCreateParameter(self, name, description, requestFileName, requestParams)        
        Element.parseCatalog(self, catalog)
        
    
