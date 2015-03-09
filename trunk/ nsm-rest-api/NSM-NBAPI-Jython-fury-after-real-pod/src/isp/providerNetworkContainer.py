'''
Created on Jul 15, 2012

@author: huhe
'''

from lib import Util
from isp.element import Element

class ProviderNetworkContainer(Element):
    
    _catalogServiceOfferingType = 'providernetworkcontainer'
    _catalogServiceOfferingName = 'Provider Network Container'
    _catalogLinkTitle = 'Provider Network Container'
    
    
    def __init__(self, catalog, name=None, description=None, requestFileName='default-provider-network-container.xml', requestParams=None):
        self.logger = Util.getLogger(self.__class__.__name__)
        Element.__init__(self)
        Element.setCatalogMatchParameter(self, ProviderNetworkContainer._catalogServiceOfferingType, ProviderNetworkContainer._catalogServiceOfferingName, ProviderNetworkContainer._catalogLinkTitle)
        Element.setCreateParameter(self, name, description, requestFileName, requestParams)        
        Element.parseCatalog(self, catalog)
        
        
    
    
