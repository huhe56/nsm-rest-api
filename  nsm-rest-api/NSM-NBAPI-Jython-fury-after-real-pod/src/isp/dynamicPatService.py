'''
Created on Jul 15, 2012

@author: huhe
'''

from lib import Util
from isp.element import Element

class DynamicPatService(Element):
    
    _catalogServiceOfferingType = 'servicepolicy'
    _catalogServiceOfferingName = 'Dynamic PAT Service'
    _catalogLinkTitle = 'Dynamic PAT Service'
    
    
    def __init__(self, catalog, name=None, description=None, requestFileName='default-dynamic-pat-service.xml', requestParams=None):
        self.logger = Util.getLogger(self.__class__.__name__)
        Element.__init__(self)
        Element.setCatalogMatchParameter(self, DynamicPatService._catalogServiceOfferingType, DynamicPatService._catalogServiceOfferingName, DynamicPatService._catalogLinkTitle)
        Element.setCreateParameter(self, name, description, requestFileName, requestParams)        
        Element.parseCatalog(self, catalog)
        
        
   
    
