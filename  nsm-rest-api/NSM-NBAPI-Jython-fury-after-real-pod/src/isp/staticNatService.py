'''
Created on Jul 15, 2012

@author: huhe
'''

from lib import Util
from isp.element import Element

class StaticNatService(Element):
    
    _catalogServiceOfferingType = 'servicepolicy'
    _catalogServiceOfferingName = 'Static NAT one-to-one Service'
    _catalogLinkTitle = 'Static NAT one-to-one Service'
    
    
    def __init__(self, catalog, name=None, description=None, requestFileName='default-static-nat-service.xml', requestParams=None):
        self.logger = Util.getLogger(self.__class__.__name__)
        Element.__init__(self)
        Element.setCatalogMatchParameter(self, StaticNatService._catalogServiceOfferingType, StaticNatService._catalogServiceOfferingName, StaticNatService._catalogLinkTitle)
        Element.setCreateParameter(self, name, description, requestFileName, requestParams)        
        Element.parseCatalog(self, catalog)
        
        
   
    
