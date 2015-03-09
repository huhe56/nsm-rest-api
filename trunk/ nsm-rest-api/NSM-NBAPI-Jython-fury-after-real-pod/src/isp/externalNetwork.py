'''
Created on Jul 15, 2012

@author: huhe
'''

from lib import Util
from isp.element import Element

class ExternalNetwork(Element):
    
    _catalogServiceOfferingType = 'externalnetwork'
    _catalogServiceOfferingName = 'External Network'
    _catalogLinkTitle = 'External Network'
    
    
    def __init__(self, catalog, name=None, description=None, requestFileName='default-external-network.xml', requestParams=None):
        self.logger = Util.getLogger(self.__class__.__name__)
        Element.__init__(self)
        Element.setCatalogMatchParameter(self, ExternalNetwork._catalogServiceOfferingType, ExternalNetwork._catalogServiceOfferingName, ExternalNetwork._catalogLinkTitle)
        Element.setCreateParameter(self, name, description, requestFileName, requestParams)        
        Element.parseCatalog(self, catalog)
        
        
