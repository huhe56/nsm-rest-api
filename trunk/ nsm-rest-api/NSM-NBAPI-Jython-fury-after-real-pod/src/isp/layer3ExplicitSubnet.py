'''
Created on Jul 15, 2012

@author: huhe
'''

import ipaddr
from lib import Util
from isp import XPath, Define
from lib import Util
from nsmUtil import NsmUtil
from isp.element import Element
from isp.layer3AccessVlan import Layer3AccessVlan

class Layer3ExplicitSubnet(Layer3AccessVlan):
    
    _catalogServiceOfferingType = 'networksegment'
    _catalogServiceOfferingName = 'Layer 3 VLAN Explicit Subnet'
    _catalogLinkTitle = 'Layer 3 VLAN Explicit Subnet'
    
    
    def __init__(self, catalog, name=None, description=None, requestFileName='default-layer3-explicit-subnet.xml', requestParams=None):
        self.logger = Util.getLogger(self.__class__.__name__)
        Element.__init__(self)
        Element.setCatalogMatchParameter(self, Layer3ExplicitSubnet._catalogServiceOfferingType, Layer3ExplicitSubnet._catalogServiceOfferingName, Layer3ExplicitSubnet._catalogLinkTitle)
        Element.setCreateParameter(self, name, description, requestFileName, requestParams)        
        Element.parseCatalog(self, catalog)

        
    def getSubPoolUid(self):
        ipAddressPool = Util.getXpathValue(self.detailXml, XPath._LinkExternalAccessLayer3VlanSubPool1)
        self.logger.info('layer 3 explicit subnet ip address sub pool 1: ' + ipAddressPool)
        return ipAddressPool
    
