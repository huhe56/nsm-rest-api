'''
Created on Jul 15, 2012

@author: huhe
'''

from lib import Util
from isp.element import Element
from isp.layer3AccessVlan import Layer3AccessVlan


class Layer3PrivateAccessVlan(Layer3AccessVlan):
    
    _catalogServiceOfferingType = 'networksegment'
    _catalogServiceOfferingName = 'Layer 3 Private Access VLAN'
    _catalogLinkTitle = 'Layer 3 Private Access VLAN'
    
    
    def __init__(self, catalog, name=None, description=None, requestFileName='default-layer3-private-access-vlan.xml', requestParams=None):
        self.logger = Util.getLogger(self.__class__.__name__)
        Element.__init__(self)
        Element.setCatalogMatchParameter(self, Layer3PrivateAccessVlan._catalogServiceOfferingType, Layer3PrivateAccessVlan._catalogServiceOfferingName, Layer3PrivateAccessVlan._catalogLinkTitle)
        Element.setCreateParameter(self, name, description, requestFileName, requestParams)        
        Element.parseCatalog(self, catalog)
        
        
    
    
