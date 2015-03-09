'''
Created on Jul 15, 2012

@author: huhe
'''

from lib import Util
from isp.element import Element

class TenantNetworkContainer(Element):
    
    _catalogServiceOfferingType = 'tenantnetworkcontainer'
    _catalogServiceOfferingName = 'Tenant Network Container'
    _catalogLinkTitle = 'Tenant Network Container'
    
    
    def __init__(self, catalog, name=None, description=None, requestFileName='default-tenant-network-container.xml', requestParams=None):
        self.logger = Util.getLogger(self.__class__.__name__)
        Element.__init__(self)
        Element.setCatalogMatchParameter(self, TenantNetworkContainer._catalogServiceOfferingType, TenantNetworkContainer._catalogServiceOfferingName, TenantNetworkContainer._catalogLinkTitle)
        Element.setCreateParameter(self, name, description, requestFileName, requestParams)        
        Element.parseCatalog(self, catalog)
        
        
    
    
